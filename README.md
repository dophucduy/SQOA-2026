# Fermi-Hubbard VQE - Mô phỏng Lượng tử

Dự án mô phỏng mô hình Fermi-Hubbard 3-site sử dụng thuật toán VQE (Variational Quantum Eigensolver) với Qiskit.

## Cấu trúc thư mục

```
.
├── introduction_basic/          # Tài liệu học tập cơ bản về Qiskit (không liên quan trực tiếp đến dự án chính)
│   ├── first_qiskit.program.py
│   └── qiskit_gates_demo.ipynb
│
├── fermi_hubbard_vqe.ipynb      # Notebook chính - Mô phỏng Fermi-Hubbard VQE
├── fermi_hubbard_helpers.py     # Module hỗ trợ (Hamiltonian, VQE, sweep)
├── test_hamiltonian_basic.py    # Unit tests
│
├── task2_solution.md            # Tài liệu giải pháp
├── presentDiscuss.jpg           # Hình ảnh thuyết trình
└── q1.6.jpg                     # Hình ảnh câu hỏi
```

## Bắt đầu nhanh

1. **Chạy notebook chính:**
   ```bash
   jupyter notebook fermi_hubbard_vqe.ipynb
   ```

2. **Chạy tests:**
   ```bash
   pytest test_hamiltonian_basic.py
   ```

## Nội dung chính

- **Xây dựng Hamiltonian** cho mô hình Fermi-Hubbard 3-site (6 qubits)
- **Exact Diagonalization** để tính năng lượng trạng thái cơ bản chính xác
- **VQE** với ansatz EfficientSU2 và optimizer SLSQP
- **Nghiên cứu hội tụ** khi thay đổi tham số J (hopping) và U (tương tác)

## Yêu cầu

- Python 3.10+
- Qiskit >= 1.x
- qiskit-aer
- qiskit_algorithms
- numpy, matplotlib

## Ghi chú

Thư mục `introduction_basic/` chứa các file học tập cơ bản về Qiskit, không liên quan trực tiếp đến dự án Fermi-Hubbard VQE.
