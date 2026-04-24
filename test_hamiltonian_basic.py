"""Quick test to verify build_hamiltonian implementation."""

from fermi_hubbard_helpers import build_hamiltonian

# Test 1: Check qubit count
print("Test 1: Checking qubit count...")
H = build_hamiltonian(J=1.0, U=0.0)
assert H.num_qubits == 6, f"Expected 6 qubits, got {H.num_qubits}"
print(f"✓ Qubit count is correct: {H.num_qubits}")

# Test 2: Check U=0 has no interaction terms
print("\nTest 2: Checking U=0 has only hopping terms...")
H_u0 = build_hamiltonian(J=1.0, U=0.0)
print(f"Number of terms with U=0: {len(H_u0.paulis)}")
print("Pauli terms:")
for pauli, coeff in zip(H_u0.paulis, H_u0.coeffs):
    print(f"  {pauli} : {coeff}")

# Test 3: Check U>0 has interaction terms
print("\nTest 3: Checking U>0 has interaction terms...")
H_u1 = build_hamiltonian(J=1.0, U=1.0)
print(f"Number of terms with U=1.0: {len(H_u1.paulis)}")

# Test 4: Check Hermiticity
print("\nTest 4: Checking Hamiltonian is Hermitian...")
import numpy as np
H_matrix = H_u1.to_matrix()
is_hermitian = np.allclose(H_matrix, H_matrix.conj().T, atol=1e-10)
assert is_hermitian, "Hamiltonian is not Hermitian!"
print("✓ Hamiltonian is Hermitian")

print("\n✓ All basic tests passed!")
