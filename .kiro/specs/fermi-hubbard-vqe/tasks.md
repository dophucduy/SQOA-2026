# Tasks

## Task List

- [x] 1. Set up notebook structure and helper module
  - [x] 1.1 Create `fermi_hubbard_vqe.ipynb` in the workspace root with section skeleton (markdown cells for Introduction, Hamiltonian, Exact Diagonalization, VQE, J-sweep, optional U-sweep, Summary)
  - [x] 1.2 Create `fermi_hubbard_helpers.py` in the workspace root containing importable functions: `build_hamiltonian`, `exact_ground_energy`, `run_vqe`, `make_ansatz`, `sweep_J`, `sweep_U`, `compute_error_flag`

- [-] 2. Implement Hamiltonian construction
  - [x] 2.1 Implement `build_hamiltonian(J, U)` in `fermi_hubbard_helpers.py` using `SparsePauliOp.from_list` with the 6-qubit Pauli strings from the requirements formula (hopping terms scaled by -J/2, interaction terms scaled by U/4), accounting for Qiskit's little-endian qubit ordering
  - [x] 2.2 Add a notebook code cell that calls `build_hamiltonian(J=1.0, U=0)`, prints the Pauli terms and coefficients, and verifies the qubit count is 6

- [x] 3. Implement exact diagonalization
  - [x] 3.1 Implement `exact_ground_energy(hamiltonian)` using `hamiltonian.to_matrix()` and `numpy.linalg.eigvalsh`, returning the minimum eigenvalue
  - [x] 3.2 Add a notebook code cell that computes and displays the exact ground state energy for J=1.0, U=0

- [x] 4. Implement VQE runner and ansatz
  - [x] 4.1 Implement `make_ansatz(num_qubits=6, reps=2)` returning `EfficientSU2` with `entanglement='linear'`
  - [x] 4.2 Implement `run_vqe(hamiltonian, ansatz, optimizer, seed=42)` wrapping `qiskit_algorithms.VQE` with `StatevectorEstimator`; include non-convergence detection and warning print
  - [x] 4.3 Add notebook code cells for a single VQE run at J=1.0, U=0; display optimized energy and comparison to exact value

- [x] 5. Implement J-sweep convergence study
  - [x] 5.1 Implement `sweep_J(J_values, U=0.0)` iterating over J values, calling `build_hamiltonian`, `exact_ground_energy`, and `run_vqe`, returning a `SweepResult`
  - [x] 5.2 Implement `compute_error_flag(exact, vqe)` returning True when relative error > 1%
  - [x] 5.3 Add notebook code cell running `sweep_J` for 5 uniformly spaced J values in [1.0, 5.0]
  - [x] 5.4 Add notebook code cell plotting VQE vs exact energy versus J, highlighting points where relative error > 1%

- [ ] 6. (Optional) Implement U-sweep convergence study
  - [ ] 6.1 Implement `sweep_U(U_values, J=1.0)` mirroring `sweep_J`
  - [ ] 6.2 Add notebook code cells running `sweep_U` for U ∈ {0, 0.5, 1.0} and plotting results

- [x] 7. Add presentation markdown cells
  - [x] 7.1 Write markdown cell explaining the physical meaning of the Fermi-Hubbard Hamiltonian and its hopping/interaction terms
  - [x] 7.2 Write markdown cell explaining the `EfficientSU2` ansatz choice and its suitability for particle-number-approximate problems
  - [x] 7.3 Write markdown cell explaining the SLSQP optimizer and the VQE optimization procedure
  - [x] 7.4 Write markdown cell summarizing final results and conclusions

- [ ] 8. Write tests
  - [ ] 8.1 Create `tests/test_fermi_hubbard_vqe.py` with unit tests: `test_hamiltonian_u0_exact_energy`, `test_hamiltonian_terms_u0`, `test_hamiltonian_terms_u_positive`, `test_vqe_single_run`, `test_sweep_j_length`, `test_relative_error_flag`
  - [ ] 8.2 Create `tests/test_fermi_hubbard_vqe_pbt.py` with Hypothesis property tests for Properties 1, 2, 3, and 5 (each with `max_examples=100`)
