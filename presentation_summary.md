# Tóm tắt Thuyết trình: Mô phỏng Fermi-Hubbard bằng VQE
## Thời lượng: 6 phút

---

## Slide 1: Giới thiệu (30 giây)
**Nội dung:**
- Mô hình Fermi-Hubbard: Mô tả electron trên mạng tinh thể
- Mục tiêu: Tìm năng lượng trạng thái cơ bản bằng VQE
- Hệ thống: 3 sites, 6 qubits (3 sites × 2 spins)

**Key points:**
- Ứng dụng: Siêu dẫn nhiệt độ cao, Mott insulator
- Phương pháp: Quantum computing với VQE algorithm

---

## Slide 2: Hamiltonian Fermi-Hubbard (1 phút)
**Nội dung:**
- **Hopping term** ($-J/2$): Động năng, electron di chuyển giữa các site
- **Interaction term** ($U/4$): Thế năng, tương tác Coulomb khi 2 electron cùng site

**Công thức:**
$$H = -\frac{J}{2}[\text{hopping}] + \frac{U}{4}[\text{interaction}]$$

**Kết quả:**
- J=1.0, U=0: 8 Pauli terms (chỉ hopping)
- J=1.0, U>0: 20 Pauli terms (hopping + interaction)
- Ma trận 64×64 (6 qubits)

**Biểu đồ:** Sơ đồ 3-site chain với hopping và interaction

---

## Slide 3: Lựa chọn Ansatz - EfficientSU2 (1 phút)
**Nội dung:**
- **Tại sao EfficientSU2?**
  1. Hardware-efficient: Chỉ dùng Ry, Rz, CNOT
  2. Linear entanglement: Phù hợp với topology 1D
  3. 24 tham số: Đủ expressive cho hệ nhỏ
  4. Đơn giản: Không cần fermionic libraries

**Cấu trúc:**
```
Layer 1: [Ry, Rz] × 6 qubits → CNOT chain
Layer 2: [Ry, Rz] × 6 qubits → CNOT chain
```

**Trade-off:**
- ✓ Tốt cho U=0 (free fermion)
- ✗ Không bảo toàn số hạt chính xác (cần UCCSD cho U lớn)

**Biểu đồ:** Circuit diagram của EfficientSU2

---

## Slide 4: Quy trình VQE (1.5 phút)
**Nội dung:**
- **VQE = Variational Quantum Eigensolver**
- Hybrid quantum-classical algorithm

**Vòng lặp:**
1. **Quantum:** Chuẩn bị trạng thái $|\psi(\theta)\rangle$ → Đo đạc expectation values
2. **Classical:** Tính năng lượng $E(\theta)$ → Optimizer cập nhật $\theta$
3. **Lặp lại** cho đến khi hội tụ

**Optimizer: SLSQP**
- Gradient-based (parameter-shift rule)
- Hội tụ nhanh: 100-300 iterations
- Phù hợp với statevector simulation

**Estimator: StatevectorEstimator**
- Exact computation (không có shot noise)
- Lý tưởng cho mục đích giáo dục

**Biểu đồ:** Flowchart VQE loop

---

## Slide 5: Kết quả - Single Run (1 phút)
**Nội dung:**
- **Exact energy** (J=1.0, U=0): $E_{\text{exact}} = -2.828$
- **VQE energy**: $E_{\text{VQE}} \approx -2.82$
- **Relative error**: < 1% (0.3-0.5%)
- **Iterations**: 150-250

**So sánh:**
| Phương pháp | Năng lượng | Thời gian |
|-------------|-----------|-----------|
| Exact       | -2.828427 | < 1s      |
| VQE         | -2.820    | 2-3s      |

**Kết luận:** VQE hội tụ tốt, ansatz đủ expressive

**Biểu đồ:** Bar chart so sánh Exact vs VQE energy

---

## Slide 6: Nghiên cứu Hội tụ - J-Sweep (1 phút)
**Nội dung:**
- **Mục tiêu:** Đánh giá VQE khi thay đổi J ∈ [1.0, 5.0]
- **Kết quả:**
  - VQE theo sát exact energy
  - Relative error < 2% cho mọi J
  - Không có convergence issues

**Quan sát:**
- J tăng → Năng lượng giảm (kinetic energy thấp hơn)
- VQE robust trên nhiều giá trị J

**Biểu đồ:** Line plot VQE vs Exact energy theo J (với error bars)

---

## Slide 7: Kết luận & Ứng dụng (1 phút)
**Nội dung:**

**Ưu điểm:**
- ✓ VQE chính xác cho hệ nhỏ (error < 1%)
- ✓ Robust trên nhiều tham số J
- ✓ Thời gian tính toán nhanh

**Hạn chế:**
- ✗ Ansatz không bảo toàn số hạt chính xác
- ✗ Cần UCCSD cho U lớn (strongly correlated)
- ✗ Trên hardware thật cần error mitigation

**Ứng dụng:**
- Mở rộng cho hệ lớn hơn (10+ sites, 20+ qubits)
- 2D lattices, time-dependent Hamiltonians
- Nghiên cứu siêu dẫn, Mott insulator

**Biểu đồ:** Summary table với ưu/nhược điểm

---

## Phân chia thời gian chi tiết:

| Slide | Thời gian | Người thuyết trình | Nội dung chính |
|-------|-----------|-------------------|----------------|
| 1     | 0:00-0:30 | Người 1           | Giới thiệu tổng quan |
| 2     | 0:30-1:30 | Người 1           | Hamiltonian (hopping + interaction) |
| 3     | 1:30-2:30 | Người 2           | Ansatz EfficientSU2 |
| 4     | 2:30-4:00 | Người 2           | Quy trình VQE (quantum-classical loop) |
| 5     | 4:00-5:00 | Người 3           | Kết quả single run |
| 6     | 5:00-6:00 | Người 3           | J-sweep & Kết luận |

---

## Tips cho thuyết trình:

1. **Slide 1-2 (Người 1):**
   - Nói rõ tại sao Fermi-Hubbard quan trọng
   - Giải thích J và U bằng hình ảnh trực quan

2. **Slide 3-4 (Người 2):**
   - Demo circuit diagram của EfficientSU2
   - Giải thích VQE loop bằng animation/flowchart

3. **Slide 5-6 (Người 3):**
   - Highlight relative error < 1%
   - Chỉ vào biểu đồ J-sweep để show robustness

4. **Q&A (nếu có):**
   - Chuẩn bị câu hỏi về: UCCSD vs EfficientSU2, barren plateaus, hardware deployment
