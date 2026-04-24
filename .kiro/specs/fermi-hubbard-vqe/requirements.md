# Requirements Document

## Introduction

This feature implements a simulation of the Fermi-Hubbard model on a 3-site lattice using Qiskit.
The Fermi-Hubbard model describes on-site interaction and hopping dynamics of fermions in a lattice.
The implementation uses the Variational Quantum Eigensolver (VQE) algorithm to find the ground state
energy, and is delivered as a Jupyter notebook for presentation purposes.

The full Hamiltonian for a 3-site lattice is:

```
H = -(J/2) * [(X1X3 + Y1Y3)Z2 + (X3X5 + Y3Y5)Z4 + (X2X4 + Y2Y4)Z3 + (X4X6 + Y4Y6)Z5]
    + (U/4) * [(I - Z1 - Z2 + Z1Z2) + (I - Z3 - Z4 + Z3Z4) + (I - Z5 - Z6 + Z5Z6)]
```

Where:
- J is the hopping parameter (default J = 1.0)
- U is the on-site interaction strength

## Glossary

- **Hamiltonian**: The operator representing the total energy of the quantum system, expressed as a sum of Pauli operators.
- **VQE (Variational Quantum Eigensolver)**: A hybrid quantum-classical algorithm that uses a parameterized quantum circuit (ansatz) and a classical optimizer to find the minimum eigenvalue of a Hamiltonian.
- **Ansatz**: A parameterized quantum circuit whose parameters are optimized to minimize the expectation value of the Hamiltonian.
- **Ground State Energy**: The lowest eigenvalue of the Hamiltonian, representing the minimum energy of the system.
- **Exact Diagonalization**: A classical numerical method to compute the exact eigenvalues of a Hamiltonian matrix.
- **Hopping Parameter (J)**: Controls the kinetic energy term; governs how fermions tunnel between adjacent lattice sites.
- **On-site Interaction (U)**: Controls the potential energy term; governs the interaction energy when two fermions occupy the same site.
- **Particle-Number Conservation**: A symmetry of the Fermi-Hubbard model where the total number of fermions is preserved.
- **Notebook**: The Jupyter notebook (`fermi_hubbard_vqe.ipynb`) that contains the full implementation and presentation.
- **Simulator**: The Qiskit Aer statevector simulator used to evaluate quantum circuits.
- **SparsePauliOp**: Qiskit's representation of a Hamiltonian as a sparse sum of Pauli strings.
- **Optimizer**: The classical optimization routine (e.g., SLSQP or COBYLA) used by VQE to update ansatz parameters.

---

## Requirements

### Requirement 1: Hamiltonian Construction

**User Story:** As a student, I want to construct the Fermi-Hubbard Hamiltonian as a Qiskit operator, so that I can use it as input to VQE and exact diagonalization.

#### Acceptance Criteria

1. THE Notebook SHALL construct the 3-site Fermi-Hubbard Hamiltonian as a `SparsePauliOp` with 6 qubits, parameterized by J and U.
2. WHEN J = 1.0 and U = 0, THE Notebook SHALL produce a Hamiltonian that contains only hopping terms (no on-site interaction terms).
3. WHEN U > 0, THE Notebook SHALL produce a Hamiltonian that includes both hopping and on-site interaction terms.
4. THE Notebook SHALL display the Hamiltonian terms and their coefficients for verification.

---

### Requirement 2: Exact Ground State Energy (U = 0)

**User Story:** As a student, I want to compute the exact ground state energy when U = 0, so that I have a reference value to validate the VQE results.

#### Acceptance Criteria

1. WHEN U = 0 and J = 1.0, THE Notebook SHALL compute the exact ground state energy using classical exact diagonalization of the Hamiltonian matrix.
2. THE Notebook SHALL display the exact ground state energy value.
3. THE Notebook SHALL use `SparsePauliOp.to_matrix()` or an equivalent method to obtain the full Hamiltonian matrix for diagonalization.

---

### Requirement 3: VQE Implementation with Particle-Number-Conserving Ansatz

**User Story:** As a student, I want to implement VQE with a suitable ansatz, so that the algorithm respects the particle-number conservation symmetry of the Fermi-Hubbard model.

#### Acceptance Criteria

1. THE Notebook SHALL implement VQE using Qiskit's `VQE` class from `qiskit_algorithms`.
2. THE Notebook SHALL use a particle-number-conserving ansatz (e.g., `EfficientSU2` with appropriate entanglement, or a custom fermionic ansatz) and SHALL justify the choice in a markdown cell.
3. THE Notebook SHALL use `StatevectorEstimator` from `qiskit.primitives` as the estimator.
4. THE Notebook SHALL use a classical optimizer (e.g., SLSQP or COBYLA) and SHALL state the choice in a markdown cell.
5. WHEN VQE converges, THE Notebook SHALL display the optimized ground state energy and compare it to the exact value from Requirement 2.
6. IF VQE does not converge within the maximum number of iterations, THEN THE Notebook SHALL display a warning message and the best energy found.

---

### Requirement 4: Convergence Study — Varying J

**User Story:** As a student, I want to vary J in the range [1.0, 5.0] and assess VQE convergence, so that I can understand how the hopping parameter affects the algorithm's performance.

#### Acceptance Criteria

1. THE Notebook SHALL run VQE for at least 5 values of J uniformly sampled from [1.0, 5.0] with U = 0.
2. THE Notebook SHALL plot the VQE ground state energy versus J alongside the exact ground state energy for each J value.
3. THE Notebook SHALL include a markdown cell explaining the observed convergence behavior and any discrepancies between VQE and exact results.
4. WHEN the VQE energy deviates from the exact energy by more than 1% for any J value, THE Notebook SHALL highlight this in the plot or in a printed message.

---

### Requirement 5: (Optional) Convergence Study — Varying U

**User Story:** As a student, I want to vary U in the range [0, 0.5, 1.0] with J = 1.0 and assess VQE convergence, so that I can understand how on-site interaction affects the algorithm.

#### Acceptance Criteria

1. WHERE the optional U-sweep is included, THE Notebook SHALL run VQE for U ∈ {0, 0.5, 1.0} with J = 1.0.
2. WHERE the optional U-sweep is included, THE Notebook SHALL plot the VQE ground state energy versus U alongside the exact ground state energy.
3. WHERE the optional U-sweep is included, THE Notebook SHALL include a markdown cell explaining whether VQE converges for each U value and providing a physical or algorithmic explanation for any failures.

---

### Requirement 6: Presentation Structure

**User Story:** As a student, I want the notebook to be structured for presentation, so that I can clearly explain the Hamiltonian, ansatz, optimization, and results to an audience.

#### Acceptance Criteria

1. THE Notebook SHALL contain a markdown section explaining the physical meaning of the Fermi-Hubbard Hamiltonian and its terms.
2. THE Notebook SHALL contain a markdown section explaining the chosen ansatz and why it is suitable for particle-number-conserving problems.
3. THE Notebook SHALL contain a markdown section explaining the optimization procedure used in VQE.
4. THE Notebook SHALL contain a markdown section summarizing the final results and conclusions.
5. THE Notebook SHALL produce at least one visualization (plot) of the energy results.

---

### Requirement 7: Environment Compatibility

**User Story:** As a developer, I want the notebook to use the same Qiskit stack as the existing workspace files, so that it runs without additional dependency changes.

#### Acceptance Criteria

1. THE Notebook SHALL use `qiskit` (>=1.x), `qiskit-aer`, and `qiskit_algorithms` consistent with the existing workspace.
2. THE Notebook SHALL use `StatevectorEstimator` from `qiskit.primitives` (not the legacy `Estimator`).
3. THE Notebook SHALL be saved as `fermi_hubbard_vqe.ipynb` in the workspace root.
