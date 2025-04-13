from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import numpy as np

# In Aer.py, the CHSH value, S, could exceed Tsirelson's bound.
# This is a natural result of the finite sampling done in Aer.
# This code is a recreation of Aer.Qasm.py, but with the Statevector simulator

def CHSH():
	# This backend works differently than Aer and produces no noise that's seen with shots
    backend = Aer.get_backend('statevector_simulator')
    
    # Measurement angles (same as before)
    angles = {
        'A0': np.pi / 2,   # X-basis measurement
        'A1': 0,           # Z-basis measurement
        'B0': np.pi / 4,   # rotated Z-basis measurement
        'B1': -np.pi / 4   # rotated Z-basis measurement
    }
    
    measurement_settings = [
        ('A0', 'B0'), 
        ('A0', 'B1'),
        ('A1', 'B0'), 
        ('A1', 'B1'),
    ]
    
    S = 0
    for alice, bob in measurement_settings:
        # Initialize circuit with 2 qubits (no classical registers)
        qc = QuantumCircuit(2)
        
        # Create Bell state between Alice and Bob
        qc.h(0)
        qc.cx(0, 1)
        
        # Apply measurement rotations
        qc.ry(-angles[alice], 0)  # Alice's basis
        qc.ry(-angles[bob], 1)    # Bob's basis
        
        # Simulate to get the statevector
        transpiled_qc = transpile(qc, backend)
        result = backend.run(transpiled_qc).result()
        statevector = result.get_statevector()
        
        # Calculate probabilities by squaring the probability amplitude
        probs = np.abs(statevector)**2
        
        # Extract probabilities for each outcome
        # "little-endian" ordering: |q1 q0>
        prob_00 = probs[0]  # |00⟩
        prob_01 = probs[1]  # |01⟩
        prob_10 = probs[2]  # |10⟩
        prob_11 = probs[3]  # |11⟩
        
        # Compute expectation value
        # recall negative and positive correlations
        E = (prob_00 + prob_11) - (prob_01 + prob_10)
        
        # Compute CHSH value
        if alice == 'A0' and bob == 'B1':
            S -= E
        else:
            S += E
        
        print(f"E({alice}{bob}) = {E:.4f}")

    return S

# Run the statevector simulation
S_exact = CHSH()
print(f"\nExact CHSH value S = {S_exact:.4f} ≈ 2√2 ({2*np.sqrt(2):.4f})")
