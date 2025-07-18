from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import numpy as np


#############################
# IBM Quantum Account Setup #
#############################

# Setting up the service to connect to IBM Quantum to submit the job to the queue
token = 'YOUR_TOKEN_HERE'

# Save credentials to disk for future sessions
# Note: overwrite=True ensures previous credentials are replaced
QiskitRuntimeService.save_account(
   token=token,
   channel="ibm_quantum", # Specifies the IBM Quantum channel instead of using IBM Cloud
   overwrite=True  
)

# Initialize service using saved credentials
service = QiskitRuntimeService(channel="ibm_quantum")

# Select backend with these properties:
# simulator=True: Ensures real hardware is used
# operational=True: Only considers online systems
# min_num_qubits=127: Filters for modern "Eagle" processor-based systems
try:
   backend = service.least_busy(simulator=False, operational=True, min_num_qubits=127)
except:
   print("No backend available. Using simulator instead.")
   backend = service.get_backend("ibmq_qasm_simulator")

print(f"Using backend: {backend.name}")


# Create a parameterized rotation angle (LaTeX formatted s.t. it appears as θ in circuit diagrams)
theta = Parameter("$\\theta$")

# creates a quantum circuit with 2 qubits
qc = QuantumCircuit(2)

# Prepares the bell state to entangle the 2 qubits

# apply hadamard gate to qubit 0
qc.h(0)
# apply cnot gate to qubit 0, controlled by qubit 1
qc.cx(0, 1)

# rotates the qubit about the y axis with the parameter theta
qc.ry(theta, 0)


# Spaces out 40 different values between 0 and 2pi (full rotation)
number_of_phases = 20 # Consider this to be the "resolution" of the parameterization
phases = np.linspace(0, 2 * np.pi, number_of_phases)


# Phases need to be expressed as list of lists in order to work (Note: A list of lists is a Pythonic way to express a matrix)
# converts []
individual_phases = [[angle] for angle in phases]


# S = <ZZ> - <ZX> + <XZ> + <XX>
# These are the Pauli X and Z gates tensored together
observable = SparsePauliOp.from_list([
   ("ZZ", 1),  # E(A_0 B_0)
   ("ZX", -1), # - E(A_0 B_1)
   ("XZ", 1),  # E(A_1 B_0)
   ("XX", 1)   # E(A_1 B_1)
])


# This is a critical step and is needed to collect the properties of the specific backend
target = backend.target

# Create transpilation pass manager with:
# optimization_level=3: Aggressive optimizations
# This is neccesarry for mapping qubits to the physical hardware
pm = generate_preset_pass_manager(target=target, optimization_level=3)


# Transpile circuit to Instruction Set Architecture (ISA) format:
# Converts gates to hardware-native basis gates
# Maps virtual qubits to physical qubits
# Adds swaps for connectivity constraints
qc_isa = pm.run(qc) # Creates a hardware-compatable quantum circuit


# print(qc_isa.draw()) 
# Verify qubit mapping and gate decomposition

# Adjust observables to match transpiled circuit's qubit mapping:
# layout contains virtual→physical qubit mapping information
# Required because transpilation may reorder qubits
isa_observable = observable.apply_layout(layout=qc_isa.layout) # Creates a hardware-compatable observable

# Initialize Estimator configured for selected backend to handle job queuing and execution
estimator = Estimator(mode=backend)

# Create "publisher" (pub) object
pub = (
    qc_isa,  # remapped ISA circuit
    [[isa_observable]], # remapped observables
    individual_phases  # Parameter values to test
)

# Submit job to IBM Quantum system
job = estimator.run(pubs=[pub])
result = job.result()

# This is our CHSH value, if it is greater than 2, then the CHSH inequality has been violated
S_values = result[0].data.evs[0] # Expectation values for the observable

print(S_values)

violation = np.any(np.abs(S_values) > 2)
print(f"CHSH violation detected: {violation}")

print(f"Job ID: {job.job_id()}") # Unique identifier for job
print(f"Job status: {job.status()}") # Should be 'DONE' if successful
