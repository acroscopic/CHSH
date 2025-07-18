from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

# This suite of programs uses the IBM Qiskit Software Development Kit (SDK)
# This particular program uses the Aer Statevector simulator

# This is a noiseless backend. 
# It will manipulate qubits in a pure mathematical sense
# While useful, it is not indicative of a real experimental environment
backend = Aer.get_backend('statevector_simulator')
    
# These are the angles at which we're measuring our qubits
angles = {
    # Pure X-basis measurement
    'A0': np.pi / 2,

    # Pure Z-basis measurement
    'A1': 0,

    # X-basis (Rotated 45 degrees)
    'B0': np.pi / 4,

    # Z-basis (Rotated 45 degrees)
    'B1': -np.pi / 4
}
    
# Recall S = E(A0B0) − E(A0B1) + E(A1B0) + E(A1B1)
# This is just setting up the settings so we can loop over them
# We will subtract the E(A0B1) later
measurement_settings = [
    ('A0', 'B0'), # Add
    ('A0', 'B1'), # Subtract
    ('A1', 'B0'), # Add
    ('A1', 'B1'), # Add
]

def CHSH():

    # Initialize the CHSH Parameter
    S = 0

    # Start looping through the measurement settings
    # We need to use both qubits, which we've named Alice and Bob
    for alice, bob in measurement_settings:

        # Note for the Statevector simulator: 
        # We do not need classical bits to hold the results

        # Create a circuit with 2 qubits
        qc = QuantumCircuit(2)
        
        # First, we need to create Bell state between Alice and Bob
        # Put a Hadamard gate on Alice (Qubit 0)
        qc.h(0)    
        # Then, put a CNOT gate on Alice and Bob (Controlled by Alice)  
        qc.cx(0, 1)
        
        # Apply rotations to the qubits to align the measurement basis
        qc.ry(-angles[alice], 0)  # Alice's basis
        qc.ry(-angles[bob], 1)    # Bob's basis
        
        # Simulate to get the statevector
        transpiled_qc = transpile(qc, backend)
        result = backend.run(transpiled_qc).result()
        statevector = result.get_statevector()
        
        # Calculate probabilities by squaring the probability amplitude
        probs = np.abs(statevector)**2
        
        # Extract probabilities for each outcome
        prob_00 = probs[0]  # |00>
        prob_01 = probs[1]  # |01>
        prob_10 = probs[2]  # |10>
        prob_11 = probs[3]  # |11>
        
        # Compute expectation value
        # recall negative and positive correlations
        # (N++) − (N+−) − (N−+) + (N−−)
        E = (prob_00 + prob_11) - (prob_01 + prob_10)
        
        # Compute CHSH value
        if alice == 'A0' and bob == 'B1':
            # We only want to subtract the A0 and B1 values
            S -= E
        else:
            S += E
        
        # output the individual expectation values
        print(f"E({alice}{bob}) = {E:.8f}")

    return S

print("Calculating individual expectation values:")
# Run the statevector simulation
S_exact = CHSH()

print(f"\nCalculating CHSH Value:")
print(f"S = {S_exact:.8f}...")
<<<<<<< Updated upstream
print(f"2√2 = {2*np.sqrt(2):.8f}...")
=======
print(f"2√2 = {2*np.sqrt(2):.8f}...")
>>>>>>> Stashed changes
