from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
import numpy as np


########################################
#   Violation of the CHSH inequality   #
########################################

# The Clauser–Horne–Shimony–Holt (CHSH) inequality is a specific form
# of Bell's inequality which is used to test Bell's theorem.

# Bell's theorem demonstrates that quantum mechanics is incompatible with local hidden-variable theories.

# A hidden-variable theory is a deterministic model of physics which introduces
# additional "hidden" variables that cannot be measured to explain quantum phenomena.

# Local hidden-variable theories satisfy the principle of locality, which requires that distant events cannot
# influence each other faster than the speed of light, and that their outcomes are statistically independent.


#############
#   SETUP   #
#############


# Qubits, or "quantum bits," are quantum representations of information.
# For example, a singular qubit can be represented like this: |Q> = |0> 
# And a 5-qubit system can be represented like this: |Q> = |00110>
# Similarly to classical bits, they can be either 0 or 1, 
# However they can also leverage superposition and be "both" 0 and 1.
# For example: |Q> = 1/√2 * (|0> + |1>)
# Where the square of 1/√2 is the probability of each state, so it's 50% 0 and 50% 1.
# The qubit will stay in this superposition until it is measured, then it will collapse into either 0 or 1.


# Defines qubits as q, and creates 2 of them. They can be called with q[0] or q[1]
# by default, these qubits start in the |0> state.
q = QuantumRegister(2,'q')


# Defines classiacl bits as c, and creates 2 of them. They can be called with c[0] or c[1]
# These bits are used to store the information after the collapse of the qubits. 
c = ClassicalRegister(2,'c')



##################
#   Bell State   #
##################


# This takes the two qubits and entangles them in a Bell state 
# Qubit 0, or q[0] is typically named Alice, and Qubit 1 (q[1]) is typically named Bob 
# This Bell state can be mathematically represented by |Phi^+> = 1/√2 * (|00>+|11>)

# Function to return a quantum circuit with 2 entangled qubits
def bell():
	# Creates a quantum circuit with 2 qubits and 2 classical bits
	qc = QuantumCircuit(q, c)  

	# Places a Hadamard gate on Alice
	qc.h(q[0])
	# H = 1/(sqrt(2)) *[ 1   1 ]
	#                  [ 1  -1 ]    

	# Places a CNOT gate on Bob, controlled by Alice
	qc.cx(q[0], q[1])
	# CNOT = [ 1 0 0 0 ]
	#        [ 0 1 0 0 ]
	#        [ 0 0 0 1 ]
	#        [ 0 0 1 0 ]
	return qc


###################
#   Measurement   #
###################

# The state of a qubit can be represented as a point on the Bloch sphere.
# Quantum gates manipulate this state by rotating around the axes of the sphere.
# By default, Qiskit measures qubits in the Z-basis, which corresponds to the basis states |0> and |1>
# To account for this, the rotation gate RY is applied before measurement.

# Function to measure the qubits after a specific rotation
def measure(qc, angle, qubit, cbit):

	# Having -angle instead of rewriting the angles is a matter of convention
	# The defined angles A_0, A_1, B_0, B_1 are intuitive because they described orientation on the Bloch sphere
	# It's -angle to align with the desired measurement basis on the Z-axis

	# the RY gate is a rotation about the Y-axis of the Bloch sphere
	qc.ry(-angle, qubit)
	# RY(theta) =   [ Cos(θ/2)  -Sin(θ/2) ]
	#               [ Sin(θ/2)   Cos(θ/2) ]

	qc.measure(qubit, cbit)  # Measure the qubit
	return qc

###################
#   Expectation   #
###################

# The expectation value, E(A_i, B_j) = <A_i B_j> is analytically defined by
# E(A_i, B_j) = (N_{++} - N_{+-} - N_{-+} + N_{--})/(N_{total})
# Physically it represents the average correlation between measurement outcomes for 2 entangled particles when measurements are performed
# Individually, A_i and B_j, refer to specific measurement settings, e.g. angles on the Bloch sphere
# For a pair of entangled particles, the measurements are correlated and their measurements either agree or disagree

# Function to experimentally calculate expectation values, <A_i B_j>
def expectation(counts):

	total = sum(counts.values())
	# total -> 1/N for the ensemble average


	# Extract individual counts

	# These cases contribute positively to the correlation because Alice and Bob have the same value.
	# i.e. 00 and 11 contribute positively to the expectation value (Agreement) also represented as ++ or --
	count_00 = counts.get('00', 0)
	count_11 = counts.get('11', 0)
	
	# These cases contribute negatively to the correlation because Alice and Bob have different values.
	# i.e. 01 and 10 contributes negatively to the expectation value (Disgreement) also represented as +- or -+
	count_01 = counts.get('10', 0)
	count_10 = counts.get('01', 0)
	# NOTE: the bitstring 10 corresponds to c[0] = 1 and c[1] = 0
	# Qiskit inherently orders bitstrings like '...,q2,q1,q0'  i.e '0001' is a 1 on qubit 0, 0 elsewhere.
	# This doesn't really change anything for E, but it is technically more correct to express it this way
	# This is why the 01 and 10 are swapped in this context


	# Calculates expectation value
	E = (count_00 + count_11 - count_01 - count_10) / total

	return E


#######################
#   CHSH Experiment   #
#######################


# The CHSH value, S, is calculated by S = E(A_0 B_0) - E(A_0 B_1) + E(A_1 B_0) + E(A_1 B_1)
# The CHSH inequality is |S| ≥ 2, which results from the triangle inequality in the derivation, which will not be shown here.
# The assumtion made is that measurement outcome from Alice does not depend on Bob's measurement and vice versa
# And that the outcomes of measurement are determined by pre-existing properties, or hidden variables, of the particle
# Therefore the violation of the inequality shows that the assumption is false
# Note that due to the absolute value, the bound −2 ≤ S is also valid, but S ≥ 2 is more commonly used


def CHSH():
	backend = Aer.get_backend('qasm_simulator')  # Use the Aer simulator instead of queueing to IBM

	# Initialize the CHSH value, S
	S = 0  

	# Define angles for measurements
	# These angles are derived from the geometry of the Bloch sphere and maximize the violation of the CHSH inequality
	angles = {
		'A0': np.pi / 2,   # A_1 = np.pi / 2  Measure in the X-basis
		'A1': 0,           # A_0 = 0          Measure in the Z-basis 
		'B0': np.pi / 4,   # B_0 = np.pi / 4  Measure at pi/4 from the Z-axis
		'B1': -np.pi / 4   # B_1 = -np.pi / 4 Measure at -pi/4 from the Z-axis
	}
	


	# Define each measurement setting to be looped over
	# This could be with a more compact for i,j loop, but this is easier to see what's happening
	measurement_settings = [
		('A0', 'B0'),    
		('A0', 'B1'),
		('A1', 'B0'),
		('A1', 'B1'),
	]

	# Recall that Alice is A_0, A_1 and Bob is B_0, B_1
	for alice, bob in measurement_settings:

		# Create the Bell state with 2 entangled particles, Alice and Bob
		qc = bell()

		# Apply Alice's A0 and A1 measurements on the 0th qubit and store it in the 0th bit for each measurement setting
		qc = measure(qc, angles[alice], 0, 0)

		# Apply Bob's B0 and B1 measurements on the 1st qubit and store it in the 1st bit for each measurement setting
		qc = measure(qc, angles[bob], 1, 1)

		# Transpile and run the circuit through qiskit and the Aer simulator backend
		transpiled_qc = transpile(qc, backend)
		job = backend.run(transpiled_qc, shots=10000000) 
		# shots=1000000 is for the iterations for the expectation values, higher shots improve statistical significance
		result = job.result()
		counts = result.get_counts()
		# stores each count for the expectation values for each measurement setting

		# Calculate the expectation value for each measurement setting
		E = expectation(counts)

		print(f"E({alice}{bob}) = {E:.4f}, Counts: {counts}")
		# outputs the individual expectation values for each measurement setting

		print(qc.draw())
		# draws the quantum circuits for each expectation value

		# Add or subtract the expectation value based on the CHSH formula
		# S = E(A_0 B_0) - E(A_0 B_1) + E(A_1 B_0) + E(A_1 B_1)
		if alice == 'A0' and bob == 'B1':  
			S -= E # Subtract E(A_0 B_1)
		else:  
			S += E # Add E(A_0 B_0), E(A_1 B_1), E(A_1 B_0)

	return S
	# return the CHSH value
	# The theorhetical maximum violation that can be obtained is S = 2√2 (Tsirelson's bound)
	# When using the Aer simulator on lower shot counts, it will occasionally be slightly over this bound.
	


# Run the experiment
S = CHSH()
print(f"CHSH value S = {S:.4f}")


##################
#   Conclusion   #
##################


# If S ≥ 2, then the CHSH inequality is violated!
# this is confirmation that nature cannot be described with local hidden-variable theories
# The violation of the CHSH inequality demonstrates that local hidden-variable theory cannot reproduce quantum mechanics.
# This shows that nature is fundamentally non-deterministic and that particles can influence each other instantaneously, regardless of distance.
