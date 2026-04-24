from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)
simulator = AerSimulator()
result = simulator.run(qc, shots=1000).result()
counts = result.get_counts()
print("Measurement counts:", counts)
plot_histogram(counts)
plt.show()

import numpy as np
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP
from qiskit.primitives import StatevectorEstimator

hamiltonian=SparsePauliOp.from_list([("ZZ",1.0)])

ansatz=EfficientSU2(num_qubits=2,reps=1, entanglement='linear')

estimator=StatevectorEstimator()
optimizer=SLSQP(maxiter=100)

vqe=VQE(estimator,ansatz,optimizer)
result=vqe.compute_minimum_eigenvalue(operator=hamiltonian)

print(f"VQEEigenvalue:{result.eigenvalue.real:.5f}")
print(f"OptimalParameters:{result.optimal_point}")