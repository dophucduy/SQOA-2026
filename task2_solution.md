# Task 2: Thuật toán Variational cho Fermi-Hubbard Model

## Đề bài
Triển khai thuật toán variational (VQE) cho mô hình Fermi-Hubbard 3-sites. Chọn ansatz phù hợp cho bài toán bảo toàn số hạt.

---

## Lời giải

### 1. Chọn Ansatz bảo toàn số hạt

Để bảo toàn số hạt, ta sử dụng **Hardware Efficient Ansatz** với các cổng không thay đổi số hạt.

**Ansatz được chọn: Particle-Preserving Ansatz**

Cấu trúc:
- Khởi tạo trạng thái với số hạt cố định
- Sử dụng các cổng bảo toàn số hạt: RXX, RYY gates
- Các cổng này tương ứng với hopping giữa các qubits

**Mạch lượng tử:**

```
Khởi tạo: |ψ₀⟩ với n hạt cố định

Layer 1:
  RXX(θ₁) giữa qubits (0,2)  # Site 1↑ ↔ Site 2↑
  RYY(θ₂) giữa qubits (0,2)
  RXX(θ₃) giữa qubits (2,4)  # Site 2↑ ↔ Site 3↑
  RYY(θ₄) giữa qubits (2,4)
  RXX(θ₅) giữa qubits (1,3)  # Site 1↓ ↔ Site 2↓
  RYY(θ₆) giữa qubits (1,3)
  RXX(θ₇) giữa qubits (3,5)  # Site 2↓ ↔ Site 3↓
  RYY(θ₈) giữa qubits (3,5)

Layer 2: (lặp lại với tham số khác)
  RXX(θ₉), RYY(θ₁₀), ...

Số layers: L = 2-3
Tổng số tham số: 8L
```

### 2. Trạng thái khởi tạo

Với 1 hạt spin ↑:
$$|\psi_0\rangle = |100000\rangle$$

Với 2 hạt (1↑, 1↓):
$$|\psi_0\rangle = |110000\rangle$$

### 3. Hàm mục tiêu

Tối thiểu hóa năng lượng kỳ vọng:

$$E(\vec{\theta}) = \langle\psi(\vec{\theta})|H|\psi(\vec{\theta})\rangle$$

Trong đó:
- $|\psi(\vec{\theta})\rangle$ là trạng thái sau khi áp dụng ansatz
- $\vec{\theta}$ là vector tham số cần tối ưu
- $H$ là Hamiltonian Fermi-Hubbard

### 4. Đo đạc

Hamiltonian được phân tích thành tổng các Pauli strings:

$$H = \sum_i c_i P_i$$

Với $P_i$ là các tích tensor của ma trận Pauli.

Mỗi term được đo riêng:
$$\langle P_i \rangle = \langle\psi(\vec{\theta})|P_i|\psi(\vec{\theta})\rangle$$

Năng lượng tổng:
$$E(\vec{\theta}) = \sum_i c_i \langle P_i \rangle$$

### 5. Tối ưu hóa

Sử dụng classical optimizer để tìm $\vec{\theta}^*$:

$$\vec{\theta}^* = \arg\min_{\vec{\theta}} E(\vec{\theta})$$

**Optimizers phù hợp:**
- COBYLA (Constrained Optimization BY Linear Approximation)
- SLSQP (Sequential Least Squares Programming)
- SPSA (Simultaneous Perturbation Stochastic Approximation)

**Thuật toán VQE:**

```
1. Khởi tạo θ = θ₀ (random hoặc zero)
2. Repeat:
   a. Chuẩn bị trạng thái |ψ(θ)⟩
   b. Đo các Pauli terms
   c. Tính E(θ) = Σᵢ cᵢ⟨Pᵢ⟩
   d. Cập nhật θ theo gradient
3. Until convergence
4. Return E(θ*), θ*
```

### 6. Đánh giá độ chính xác

So sánh với kết quả exact từ Task 1:

$$\text{Error} = |E_{VQE} - E_{exact}|$$

$$\text{Relative Error} = \frac{|E_{VQE} - E_{exact}|}{|E_{exact}|} \times 100\%$$

---

## Pseudo-code Implementation

```python
# 1. Định nghĩa Hamiltonian
H = FermiHubbardHamiltonian(n_sites=3, J=1.0, U=0.0)

# 2. Xây dựng ansatz
def build_ansatz(n_qubits=6, n_layers=2):
    qc = QuantumCircuit(n_qubits)
    
    # Khởi tạo trạng thái 1 hạt
    qc.x(0)  # |100000⟩
    
    params = []
    for layer in range(n_layers):
        # Hopping spin ↑
        theta1 = Parameter(f'θ_{layer}_0')
        qc.rxx(theta1, 0, 2)
        params.append(theta1)
        
        theta2 = Parameter(f'θ_{layer}_1')
        qc.ryy(theta2, 0, 2)
        params.append(theta2)
        
        theta3 = Parameter(f'θ_{layer}_2')
        qc.rxx(theta3, 2, 4)
        params.append(theta3)
        
        theta4 = Parameter(f'θ_{layer}_3')
        qc.ryy(theta4, 2, 4)
        params.append(theta4)
        
        # Hopping spin ↓
        theta5 = Parameter(f'θ_{layer}_4')
        qc.rxx(theta5, 1, 3)
        params.append(theta5)
        
        theta6 = Parameter(f'θ_{layer}_5')
        qc.ryy(theta6, 1, 3)
        params.append(theta6)
        
        theta7 = Parameter(f'θ_{layer}_6')
        qc.rxx(theta7, 3, 5)
        params.append(theta7)
        
        theta8 = Parameter(f'θ_{layer}_7')
        qc.ryy(theta8, 3, 5)
        params.append(theta8)
    
    return qc, params

# 3. Chạy VQE
ansatz, params = build_ansatz(n_layers=2)
optimizer = COBYLA(maxiter=1000)

vqe = VQE(
    ansatz=ansatz,
    optimizer=optimizer,
    quantum_instance=Aer.get_backend('statevector_simulator')
)

result = vqe.compute_minimum_eigenvalue(H)

# 4. Kết quả
E_vqe = result.eigenvalue
theta_opt = result.optimal_parameters
```

---

## Kết quả mong đợi

Với ansatz phù hợp và số layers đủ lớn:

$$E_{VQE} \approx E_{exact} = -\frac{1}{\sqrt{2}} \approx -0.707$$

**Độ chính xác phụ thuộc vào:**
- Số layers trong ansatz
- Chất lượng optimizer
- Số lần đo (shots) trên máy thật
- Nhiễu từ phần cứng lượng tử

**Ưu điểm của ansatz này:**
- Bảo toàn số hạt tự động
- Số tham số tuyến tính với số layers
- Phù hợp với cấu trúc vật lý của bài toán

___
new:
# Task 2: Thuật toán Variational cho Fermi-Hubbard Model

## Đề bài
Triển khai thuật toán variational cho mô hình Fermi-Hubbard 3-sites. Chọn ansatz phù hợp cho bài toán bảo toàn số hạt.

---

## Lời giải

Thuật toán variational (VQE) tìm năng lượng trạng thái cơ bản bằng cách tối thiểu hóa hàm năng lượng kỳ vọng:

$E(\vec{\theta}) = \langle\psi(\vec{\theta})|H|\psi(\vec{\theta})\rangle$

với $|\psi(\vec{\theta})\rangle$ là trạng thái thử phụ thuộc tham số $\vec{\theta}$.

Chọn ansatz bảo toàn số hạt dựa trên các toán tử hopping. Với trạng thái khởi tạo $|\psi_0\rangle = |100000\rangle$ (1 hạt spin ↑ ở site 1), ansatz có dạng:

$|\psi(\vec{\theta})\rangle = U(\vec{\theta})|\psi_0\rangle$

trong đó:

$U(\vec{\theta}) = \prod_{\ell=1}^{L} \prod_{(i,j)} e^{-i\theta_{ij}^{(\ell)} G_{ij}}$

với generator hopping:

$G_{ij} = \frac{1}{2}(X_i X_j + Y_i Y_j)$

Các cặp qubits láng giềng: $(1,3), (3,5), (2,4), (4,6)$ tương ứng với hopping giữa các sites.

Ansatz này bảo toàn số hạt vì generator $G_{ij}$ tương ứng với toán tử $a_i^\dagger a_j + a_j^\dagger a_i$ (chỉ di chuyển hạt giữa các orbital, không tạo/hủy hạt). Cấu trúc này phù hợp với Hamiltonian vì cả hai đều chứa các term hopping giống nhau. Với hệ 1 hạt, không gian Hilbert chỉ có 3 chiều (hạt có thể ở 1 trong 3 sites), nên $L=2$ layers đủ để biểu diễn mọi trạng thái trong không gian này.

Năng lượng kỳ vọng được tính bằng cách đo các Pauli terms trong Hamiltonian:

$E(\vec{\theta}) = -\frac{1}{2}\sum_{k} \langle\psi(\vec{\theta})|P_k|\psi(\vec{\theta})\rangle$

với $P_k$ là các term như $(X_1X_3 + Y_1Y_3)Z_2$, etc.

Tối ưu hóa bằng gradient descent với parameter shift rule:

$\frac{\partial E}{\partial \theta_i} = \frac{E(\theta_i + \pi/2) - E(\theta_i - \pi/2)}{2}$

Cập nhật tham số:

$\theta_i \leftarrow \theta_i - \eta \frac{\partial E}{\partial \theta_i}$

Lặp lại cho đến khi $|E^{(t+1)} - E^{(t)}| < \epsilon$.

---

## Kết quả

Với ansatz trên và $L=2$ layers, thuật toán hội tụ về năng lượng trạng thái cơ bản:

$\boxed{E_0 = -\sqrt{2} \approx -1.414}$

Trạng thái tối ưu có dạng:

$|\psi_0\rangle = \frac{1}{2}|100000\rangle + \frac{1}{\sqrt{2}}|001000\rangle + \frac{1}{2}|000010\rangle$

Kết quả này khớp với giá trị exact từ Task 1.
