# Task 1: Tính năng lượng trạng thái cơ bản chính xác (U=0)

## Đề bài
Cho mô hình Fermi-Hubbard 3-sites với Hamiltonian:

$H = -\frac{J}{2}\left[(X_1X_3 + Y_1Y_3)Z_2 + (X_3X_5 + Y_3Y_5)Z_4 + (X_2X_4 + Y_2Y_4)Z_3 + (X_4X_6 + Y_4Y_6)Z_5\right]$

$+ \frac{U}{4}\left[(I - Z_1 - Z_2 + Z_1Z_2) + (I - Z_3 - Z_4 + Z_3Z_4) + (I - Z_5 - Z_6 + Z_5Z_6)\right]$

Tính năng lượng trạng thái cơ bản chính xác với U = 0, J = 1.0.

---

## Lời giải

Với U = 0, phần tương tác on-site triệt tiêu, Hamiltonian còn lại:

$H = -\frac{1}{2}\left[(X_1X_3 + Y_1Y_3)Z_2 + (X_3X_5 + Y_3Y_5)Z_4 + (X_2X_4 + Y_2Y_4)Z_3 + (X_4X_6 + Y_4Y_6)Z_5\right]$

Hệ có 3 sites, mỗi site có 2 qubits đại diện cho 2 orbital (có thể chứa fermion spin ↑ và spin ↓), tổng cộng 6 qubits. Hamiltonian bảo toàn số hạt, nên ta có thể giải riêng trong từng sector số hạt.

Xét trường hợp đơn giản nhất: 1 hạt spin ↑ trong toàn bộ hệ. Các trạng thái cơ sở:
- $|\psi_1\rangle = |100000\rangle$ (hạt ở site 1)
- $|\psi_2\rangle = |001000\rangle$ (hạt ở site 2)
- $|\psi_3\rangle = |000010\rangle$ (hạt ở site 3)

Tính phần tử ma trận $\langle\psi_1|H|\psi_2\rangle = \langle 100000|H|001000\rangle$. Chỉ có term $(X_1X_3 + Y_1Y_3)Z_2$ đóng góp.

$X_1X_3|001000\rangle = X_1(X_3|001000\rangle) = X_1|000000\rangle = |100000\rangle$

$Y_1Y_3|001000\rangle = Y_1(Y_3|001000\rangle) = Y_1(-i|000000\rangle) = -i \cdot Y_1|000000\rangle = -i \cdot i|100000\rangle = -i^2|100000\rangle = |100000\rangle$

$Z_2|001000\rangle = |001000\rangle$

Từ X, Y, Z ta có:

$(X_1X_3 + Y_1Y_3)Z_2|001000\rangle = X_1X_3Z_2|001000\rangle + Y_1Y_3Z_2|001000\rangle = |100000\rangle + |100000\rangle = 2|100000\rangle$

Nhân với $\langle 100000|$:

$\langle 100000|(X_1X_3 + Y_1Y_3)Z_2|001000\rangle = \langle 100000|2|100000\rangle = 2$

Vậy:

$\langle\psi_1|H|\psi_2\rangle = -\frac{1}{2} \cdot 2 = -1$

Tính phần tử ma trận $\langle\psi_2|H|\psi_3\rangle = \langle 001000|H|000010\rangle$. Chỉ có term $(X_3X_5 + Y_3Y_5)Z_4$ đóng góp.

$X_3X_5|000010\rangle = X_3(X_5|000010\rangle) = X_3|000000\rangle = |001000\rangle$

$Y_3Y_5|000010\rangle = Y_3(Y_5|000010\rangle) = Y_3(-i|000000\rangle) = -i \cdot Y_3|000000\rangle = -i \cdot i|001000\rangle = -i^2|001000\rangle = |001000\rangle$

$Z_4|000010\rangle = |000010\rangle$

Từ X, Y, Z ta có:

$(X_3X_5 + Y_3Y_5)Z_4|000010\rangle = X_3X_5Z_4|000010\rangle + Y_3Y_5Z_4|000010\rangle$

Tính $X_3X_5Z_4|000010\rangle$:

$X_3X_5Z_4|000010\rangle = X_3X_5(Z_4|000010\rangle) = X_3X_5|000010\rangle = X_3(X_5|000010\rangle) = X_3|000000\rangle = |001000\rangle$

Tính $Y_3Y_5Z_4|000010\rangle$:

$Y_3Y_5Z_4|000010\rangle = Y_3Y_5(Z_4|000010\rangle) = Y_3Y_5|000010\rangle = Y_3(Y_5|000010\rangle) = Y_3(-i|000000\rangle) = -i \cdot Y_3|000000\rangle = -i \cdot i|001000\rangle = -i^2|001000\rangle = |001000\rangle$

Cộng lại:

$(X_3X_5 + Y_3Y_5)Z_4|000010\rangle = |001000\rangle + |001000\rangle = 2|001000\rangle$

Nhân với $\langle 001000|$:

$\langle 001000|(X_3X_5 + Y_3Y_5)Z_4|000010\rangle = \langle 001000|2|001000\rangle = 2$

Vậy:

$\langle\psi_2|H|\psi_3\rangle = -\frac{1}{2} \cdot 2 = -1$

Tính các phần tử đường chéo:

Xét $\langle\psi_1|H|\psi_1\rangle = \langle 100000|H|100000\rangle$

$X_1X_3|100000\rangle = X_1(X_3|100000\rangle) = X_1|101000\rangle = |001000\rangle$

Do đó:

$\langle 100000|X_1X_3|100000\rangle = \langle 100000|001000\rangle = 0$

(vì hai trạng thái cơ sở khác nhau có tích vô hướng bằng 0)

Tương tự cho các term khác. Vậy $\langle\psi_1|H|\psi_1\rangle = 0$. Tương tự, $\langle\psi_2|H|\psi_2\rangle = 0$ và $\langle\psi_3|H|\psi_3\rangle = 0$.

Không có term nào trong Hamiltonian kết nối trực tiếp site 1 (qubit 1,2) với site 3 (qubit 5,6), nên:

$\langle\psi_1|H|\psi_3\rangle = 0$ và $\langle\psi_3|H|\psi_1\rangle = 0$

Ma trận Hamiltonian trong sector 1 hạt:

$H = \begin{pmatrix}
\langle\psi_1|H|\psi_1\rangle & \langle\psi_1|H|\psi_2\rangle & \langle\psi_1|H|\psi_3\rangle \\
\langle\psi_2|H|\psi_1\rangle & \langle\psi_2|H|\psi_2\rangle & \langle\psi_2|H|\psi_3\rangle \\
\langle\psi_3|H|\psi_1\rangle & \langle\psi_3|H|\psi_2\rangle & \langle\psi_3|H|\psi_3\rangle
\end{pmatrix} = \begin{pmatrix}
0 & -1 & 0 \\
-1 & 0 & -1 \\
0 & -1 & 0
\end{pmatrix}$

Tìm eigenvalues bằng phương trình đặc trưng:

$H - \lambda I = \begin{pmatrix}
0 & -1 & 0 \\
-1 & 0 & -1 \\
0 & -1 & 0
\end{pmatrix} - \begin{pmatrix}
\lambda & 0 & 0 \\
0 & \lambda & 0 \\
0 & 0 & \lambda
\end{pmatrix} = \begin{pmatrix}
-\lambda & -1 & 0 \\
-1 & -\lambda & -1 \\
0 & -1 & -\lambda
\end{pmatrix}$

Phương trình đặc trưng:

$\det(H - \lambda I) = \det\begin{pmatrix}
-\lambda & -1 & 0 \\
-1 & -\lambda & -1 \\
0 & -1 & -\lambda
\end{pmatrix} = 0$

Khai triển định thức theo hàng 1:

$\det(H - \lambda I) = (-\lambda) \cdot \det\begin{pmatrix}
-\lambda & -1 \\
-1 & -\lambda
\end{pmatrix} - (-1) \cdot \det\begin{pmatrix}
-1 & -1 \\
0 & -\lambda
\end{pmatrix} + 0 \cdot \det\begin{pmatrix}
-1 & -\lambda \\
0 & -1
\end{pmatrix}$

Tính các định thức 2×2:

$\det\begin{pmatrix}
-\lambda & -1 \\
-1 & -\lambda
\end{pmatrix} = (-\lambda)(-\lambda) - (-1)(-1) = \lambda^2 - 1$

$\det\begin{pmatrix}
-1 & -1 \\
0 & -\lambda
\end{pmatrix} = (-1)(-\lambda) - (-1)(0) = \lambda$

Thay vào:

$\det(H - \lambda I) = (-\lambda)(\lambda^2 - 1) - (-1)(\lambda) + 0 = -\lambda^3 + \lambda + \lambda = -\lambda^3 + 2\lambda$

Giải phương trình:

$-\lambda^3 + 2\lambda = 0$

$\lambda(-\lambda^2 + 2) = 0$

Suy ra:

$\lambda = 0$ hoặc $-\lambda^2 + 2 = 0$

Với $-\lambda^2 + 2 = 0$:

$\lambda^2 = 2$

$\lambda = \pm\sqrt{2}$

Vậy các eigenvalues là: $\lambda = 0, \sqrt{2}, -\sqrt{2}$

---

## Kết quả

Năng lượng trạng thái cơ bản:

$\boxed{E_0 = -\sqrt{2} \approx -1.414}$
