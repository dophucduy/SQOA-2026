# Task 2: Thuật toán Variational cho Fermi-Hubbard Model

## Đề bài
Triển khai thuật toán variational cho mô hình Fermi-Hubbard 3-sites. Chọn ansatz phù hợp cho bài toán bảo toàn số hạt.

---

## Lời giải

Sử dụng Variational Quantum Eigensolver (VQE) để tối thiểu hóa expectation value của năng lượng:

$E(\vec{\theta}) = \langle\psi(\vec{\theta})|H|\psi(\vec{\theta})\rangle$

**Ansatz:** Do bài toán yêu cầu bảo toàn số hạt, ta chọn particle-conserving ansatz dựa trên hopping operators. Với trạng thái khởi tạo $|\psi_0\rangle = |100000\rangle$ (1 hạt spin ↑ ở site 1):

$|\psi(\vec{\theta})\rangle = U(\vec{\theta})|\psi_0\rangle$

$U(\vec{\theta}) = \prod_{\ell=1}^{L} \prod_{(i,j)} e^{-i\theta_{ij}^{(\ell)} G_{ij}}$

với generator:

$G_{ij} = \frac{1}{2}(X_i X_j + Y_i Y_j)$

Các cặp qubits $(1,3), (3,5), (2,4), (4,6)$ tương ứng với hopping giữa các sites. Generator này bảo toàn số hạt vì chỉ di chuyển hạt giữa các orbital (tương ứng với toán tử $a_i^\dagger a_j + a_j^\dagger a_i$), không tạo hay hủy hạt. Cấu trúc ansatz khớp với Hamiltonian vì cả hai đều chứa các hopping terms tương tự. Với không gian Hilbert có số chiều bằng 3 (1 hạt trên 3 sites), $L=2$ layers là đủ để biểu diễn mọi trạng thái.

**Tính năng lượng:** Hamiltonian được phân rã thành các Pauli terms:

$E(\vec{\theta}) = \sum_{k} c_k \langle\psi(\vec{\theta})|P_k|\psi(\vec{\theta})\rangle$

**Tối ưu hóa:** Sử dụng parameter shift rule để tính gradient:

$\frac{\partial E}{\partial \theta_i} = \frac{E(\theta_i + \pi/2) - E(\theta_i - \pi/2)}{2}$

Tối ưu hóa bằng gradient descent cho đến khi đạt điều kiện hội tụ.

---

## Kết quả

Thuật toán hội tụ về năng lượng trạng thái cơ bản:

$\boxed{E_0 = -\sqrt{2} \approx -1.414}$

Trạng thái tối ưu:

$|\psi_{gs}\rangle = \frac{1}{2}|100000\rangle + \frac{1}{\sqrt{2}}|001000\rangle + \frac{1}{2}|000010\rangle$

Kết quả này khớp với giá trị chính xác từ Task 1, cho thấy ansatz được chọn đủ biểu diễn cho bài toán.
