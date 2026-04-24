"""
fermi_hubbard_helpers.py
------------------------
Helper functions for the Fermi-Hubbard VQE notebook.

All logic for Hamiltonian construction, exact diagonalization, VQE execution,
and convergence sweeps lives here so the notebook stays clean and testable.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from qiskit import QuantumCircuit
from qiskit.circuit.library import EfficientSU2
from qiskit.primitives import StatevectorEstimator
from qiskit.quantum_info import SparsePauliOp

from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class VQEConfig:
    """Configuration for a single VQE run."""
    J: float = 1.0
    U: float = 0.0
    reps: int = 2           # EfficientSU2 repetitions
    maxiter: int = 500      # optimizer max iterations
    seed: int = 42          # random seed for reproducibility
    optimizer: str = "SLSQP"  # "SLSQP" or "COBYLA"


@dataclass
class SweepResult:
    """Results from a parameter sweep (J or U)."""
    param_values: list[float] = field(default_factory=list)
    exact_energies: list[float] = field(default_factory=list)
    vqe_energies: list[float] = field(default_factory=list)
    converged: list[bool] = field(default_factory=list)       # True if VQE converged within tolerance
    relative_errors: list[float] = field(default_factory=list)  # |vqe - exact| / |exact|


# ---------------------------------------------------------------------------
# Hamiltonian construction
# ---------------------------------------------------------------------------

def build_hamiltonian(J: float, U: float) -> SparsePauliOp:
    """Construct the 6-qubit Fermi-Hubbard Hamiltonian as a SparsePauliOp.

    Qubit layout (Jordan-Wigner, 3 sites × 2 spins, 0-indexed):
        qubit 0: site 1, spin-up
        qubit 1: site 1, spin-down
        qubit 2: site 2, spin-up
        qubit 3: site 2, spin-down
        qubit 4: site 3, spin-up
        qubit 5: site 3, spin-down

    Hopping terms are scaled by -J/2; interaction terms by U/4.
    Qiskit SparsePauliOp strings are little-endian (rightmost char = qubit 0).

    Parameters
    ----------
    J : float
        Hopping parameter.
    U : float
        On-site interaction strength.

    Returns
    -------
    SparsePauliOp
        The 6-qubit Fermi-Hubbard Hamiltonian.
    """
    pauli_list = []
    
    # Hopping terms (kinetic energy, scaled by -J/2)
    # Formula uses 1-based indices, we map to 0-based qubits
    # Qiskit is little-endian: rightmost = qubit 0
    
    # X1X3Z2: qubit 0 (X), qubit 2 (X), qubit 1 (Z) → "IIXZXI" (reading right to left: 0,1,2,3,4,5)
    # Actually: position 0→X, position 1→Z, position 2→X, positions 3,4,5→I
    # String format (right to left): qubit0 qubit1 qubit2 qubit3 qubit4 qubit5
    
    # Spin-up hopping between sites 1 and 2: X1X3Z2, Y1Y3Z2
    # X1X3Z2: X on qubit 0, Z on qubit 1, X on qubit 2 → "IIXZXI" (no, let me recalculate)
    # Little-endian: string[5]=qubit5, string[4]=qubit4, ..., string[0]=qubit0
    # So for X on qubit 0, Z on qubit 1, X on qubit 2: "IIXZXI" means:
    #   position 0 (rightmost) = qubit 0 = X
    #   position 1 = qubit 1 = I
    #   position 2 = qubit 2 = Z
    #   position 3 = qubit 3 = X
    #   position 4 = qubit 4 = I
    #   position 5 = qubit 5 = I
    # Wait, that's not right either. Let me think more carefully.
    
    # In Qiskit little-endian: the string is written left-to-right as qubit_n-1 ... qubit_1 qubit_0
    # For 6 qubits: "543210" where each digit represents the qubit index
    # So "IIXZXI" means: I(qubit5) I(qubit4) X(qubit3) Z(qubit2) X(qubit1) I(qubit0)
    
    # Let me recalculate:
    # X1X3Z2 means X on index 1 (qubit 0), X on index 3 (qubit 2), Z on index 2 (qubit 1)
    # In little-endian string (left to right = qubit 5,4,3,2,1,0):
    # Position 0 (leftmost) = qubit 5 = I
    # Position 1 = qubit 4 = I
    # Position 2 = qubit 3 = I
    # Position 3 = qubit 2 = X
    # Position 4 = qubit 1 = Z
    # Position 5 (rightmost) = qubit 0 = X
    # So: "IIIXZX"
    
    # Spin-up hopping between sites 1 and 2
    pauli_list.append(("IIIXZX", -J/2))  # X1X3Z2
    pauli_list.append(("IIIYZX", -J/2))  # Y1Y3Z2
    
    # Spin-up hopping between sites 2 and 3: X3X5Z4, Y3Y5Z4
    # X3X5Z4: X on index 3 (qubit 2), X on index 5 (qubit 4), Z on index 4 (qubit 3)
    # String (left to right = qubit 5,4,3,2,1,0):
    # qubit 5 = I, qubit 4 = X, qubit 3 = Z, qubit 2 = X, qubit 1 = I, qubit 0 = I
    pauli_list.append(("IXZXII", -J/2))  # X3X5Z4
    pauli_list.append(("IYZXII", -J/2))  # Y3Y5Z4
    
    # Spin-down hopping between sites 1 and 2: X2X4Z3, Y2Y4Z3
    # X2X4Z3: X on index 2 (qubit 1), X on index 4 (qubit 3), Z on index 3 (qubit 2)
    # String (left to right = qubit 5,4,3,2,1,0):
    # qubit 5 = I, qubit 4 = I, qubit 3 = X, qubit 2 = Z, qubit 1 = X, qubit 0 = I
    pauli_list.append(("IIXZXI", -J/2))  # X2X4Z3
    pauli_list.append(("IIYZXI", -J/2))  # Y2Y4Z3
    
    # Spin-down hopping between sites 2 and 3: X4X6Z5, Y4Y6Z5
    # X4X6Z5: X on index 4 (qubit 3), X on index 6 (qubit 5), Z on index 5 (qubit 4)
    # String (left to right = qubit 5,4,3,2,1,0):
    # qubit 5 = X, qubit 4 = Z, qubit 3 = X, qubit 2 = I, qubit 1 = I, qubit 0 = I
    pauli_list.append(("XZXIII", -J/2))  # X4X6Z5
    pauli_list.append(("YZXIII", -J/2))  # Y4Y6Z5
    
    # On-site interaction terms (scaled by U/4)
    # (I - Z1 - Z2 + Z1Z2) for site 1
    # I - Z1 - Z2 + Z1Z2 = I - Z(qubit0) - Z(qubit1) + Z(qubit0)Z(qubit1)
    if U != 0:
        # Site 1: qubits 0 and 1
        pauli_list.append(("IIIIII", U/4))      # I
        pauli_list.append(("IIIIIZ", -U/4))     # -Z1 (Z on qubit 0)
        pauli_list.append(("IIIIZI", -U/4))     # -Z2 (Z on qubit 1)
        pauli_list.append(("IIIIZZ", U/4))      # Z1Z2 (Z on qubits 0 and 1)
        
        # Site 2: qubits 2 and 3
        pauli_list.append(("IIIIII", U/4))      # I
        pauli_list.append(("IIIIZI", -U/4))     # -Z3 (Z on qubit 2)
        pauli_list.append(("IIZIII", -U/4))     # -Z4 (Z on qubit 3)
        pauli_list.append(("IIZIZI", U/4))      # Z3Z4 (Z on qubits 2 and 3)
        
        # Site 3: qubits 4 and 5
        pauli_list.append(("IIIIII", U/4))      # I
        pauli_list.append(("IZIIII", -U/4))     # -Z5 (Z on qubit 4)
        pauli_list.append(("ZIIIII", -U/4))     # -Z6 (Z on qubit 5)
        pauli_list.append(("ZZIIII", U/4))      # Z5Z6 (Z on qubits 4 and 5)
    
    return SparsePauliOp.from_list(pauli_list)


# ---------------------------------------------------------------------------
# Exact diagonalization
# ---------------------------------------------------------------------------

def exact_ground_energy(hamiltonian: SparsePauliOp) -> float:
    """Return the exact ground state energy via classical diagonalization.

    Converts the SparsePauliOp to a dense matrix and uses
    numpy.linalg.eigvalsh (exploits Hermiticity) to find the minimum
    eigenvalue.

    Parameters
    ----------
    hamiltonian : SparsePauliOp
        The Hamiltonian operator.

    Returns
    -------
    float
        The minimum eigenvalue (ground state energy).
    """
    # Convert SparsePauliOp to dense matrix
    matrix = hamiltonian.to_matrix()
    
    # Use eigvalsh for Hermitian matrices (more efficient and numerically stable)
    eigenvalues = np.linalg.eigvalsh(matrix)
    
    # Return the minimum eigenvalue (ground state energy)
    return float(np.min(eigenvalues))


# ---------------------------------------------------------------------------
# Ansatz factory
# ---------------------------------------------------------------------------

def make_ansatz(num_qubits: int = 6, reps: int = 2) -> EfficientSU2:
    """Return an EfficientSU2 ansatz with linear entanglement.

    Linear entanglement mirrors the nearest-neighbor topology of the
    Fermi-Hubbard lattice and keeps the circuit depth manageable.

    Parameters
    ----------
    num_qubits : int
        Number of qubits (default 6 for the 3-site model).
    reps : int
        Number of repetition layers (default 2).

    Returns
    -------
    EfficientSU2
        The parameterized ansatz circuit.
    """
    return EfficientSU2(num_qubits=num_qubits, reps=reps, entanglement='linear')


# ---------------------------------------------------------------------------
# VQE runner
# ---------------------------------------------------------------------------

def run_vqe(
    hamiltonian: SparsePauliOp,
    ansatz: QuantumCircuit,
    optimizer,
    seed: int = 42,
):
    """Run VQE and return the result.

    Uses StatevectorEstimator for exact (shot-noise-free) expectation values.
    Prints a warning if VQE does not converge within the optimizer's iteration
    limit.

    Parameters
    ----------
    hamiltonian : SparsePauliOp
        The Hamiltonian to minimize.
    ansatz : QuantumCircuit
        The parameterized ansatz circuit.
    optimizer : qiskit_algorithms optimizer
        Classical optimizer instance (e.g., SLSQP(maxiter=500)).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    VQEResult
        The full result object; inspect `.eigenvalue` for the ground state
        energy and `.optimal_point` for the optimized parameters.
    """
    # Create the StatevectorEstimator
    estimator = StatevectorEstimator(seed=seed)
    
    # Create and run VQE
    vqe = VQE(estimator=estimator, ansatz=ansatz, optimizer=optimizer)
    result = vqe.compute_minimum_eigenvalue(operator=hamiltonian)
    
    # Check for non-convergence
    # SLSQP and COBYLA store the number of function evaluations in optimizer_result
    if hasattr(result, 'optimizer_result') and hasattr(optimizer, 'maxiter'):
        nfev = result.optimizer_result.get('nfev', 0) if isinstance(result.optimizer_result, dict) else getattr(result.optimizer_result, 'nfev', 0)
        maxiter = optimizer.maxiter
        
        # If we hit the max iterations, warn about non-convergence
        if nfev >= maxiter:
            print(f"Warning: VQE did not converge within {maxiter} iterations. Best energy: {result.eigenvalue:.6f}")
    
    return result


# ---------------------------------------------------------------------------
# Convergence sweeps
# ---------------------------------------------------------------------------

def sweep_J(J_values: list[float], U: float = 0.0) -> SweepResult:
    """Run VQE and exact diagonalization for each J value.

    For each J in J_values, builds H(J, U), computes the exact ground state
    energy, runs VQE, and records the relative error.

    Parameters
    ----------
    J_values : list[float]
        Hopping parameter values to sweep over.
    U : float
        Fixed on-site interaction (default 0.0).

    Returns
    -------
    SweepResult
        Aggregated results for all J values.
    """
    result = SweepResult()
    
    for J in J_values:
        # Build Hamiltonian for this J value
        hamiltonian = build_hamiltonian(J, U)
        
        # Compute exact ground state energy
        exact_energy = exact_ground_energy(hamiltonian)
        
        # Run VQE
        ansatz = make_ansatz(num_qubits=6, reps=2)
        optimizer = SLSQP(maxiter=500)
        vqe_result = run_vqe(hamiltonian, ansatz, optimizer, seed=42)
        vqe_energy = vqe_result.eigenvalue
        
        # Compute relative error
        relative_error = abs(vqe_energy - exact_energy) / abs(exact_energy)
        
        # Check convergence (within 5% tolerance as per design)
        converged = relative_error <= 0.05
        
        # Store results
        result.param_values.append(J)
        result.exact_energies.append(exact_energy)
        result.vqe_energies.append(vqe_energy)
        result.converged.append(converged)
        result.relative_errors.append(relative_error)
    
    return result


def sweep_U(U_values: list[float], J: float = 1.0) -> SweepResult:
    """Run VQE and exact diagonalization for each U value.

    Mirrors sweep_J but varies the on-site interaction U with fixed J.

    Parameters
    ----------
    U_values : list[float]
        On-site interaction values to sweep over.
    J : float
        Fixed hopping parameter (default 1.0).

    Returns
    -------
    SweepResult
        Aggregated results for all U values.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Error utilities
# ---------------------------------------------------------------------------

def compute_error_flag(exact: float, vqe: float) -> bool:
    """Return True if the relative error between vqe and exact exceeds 1%.

    Relative error is defined as |vqe - exact| / |exact|.

    Parameters
    ----------
    exact : float
        Exact ground state energy (must be non-zero).
    vqe : float
        VQE ground state energy estimate.

    Returns
    -------
    bool
        True if relative error > 0.01, False otherwise.
    """
    relative_error = abs(vqe - exact) / abs(exact)
    return relative_error > 0.01
