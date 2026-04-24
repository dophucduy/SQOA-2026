# Phân chia công việc thuyết trình
## Dự án: Mô phỏng Fermi-Hubbard bằng VQE

---

## Tổng quan phân công

| Người | Slides | Thời gian | Nội dung chính |
|-------|--------|-----------|----------------|
| **Người 1** | 1-2 | 0:00-1:30 | Giới thiệu + Hamiltonian |
| **Người 2** | 3-4 | 1:30-4:00 | Ansatz + VQE Algorithm |
| **Người 3** | 5-7 | 4:00-6:00 | Kết quả + Kết luận |

---

## Chi tiết công việc từng người

### 👤 Người 1: Giới thiệu & Hamiltonian (1.5 phút)

#### Slide 1: Giới thiệu (30 giây)
**Chuẩn bị:**
- [ ] Đọc phần Introduction trong `solution.md`
- [ ] Hiểu rõ ứng dụng của Fermi-Hubbard model
- [ ] Chuẩn bị câu mở đầu hấp dẫn

**Nội dung thuyết trình:**
```
"Chào mọi người, hôm nay nhóm em xin trình bày về mô phỏng mô hình 
Fermi-Hubbard bằng thuật toán VQE. Mô hình này rất quan trọng trong 
nghiên cứu vật lý chất rắn, đặc biệt là hiện tượng siêu dẫn nhiệt độ cao 
và Mott insulator. Hệ thống của chúng em là 3 sites với 6 qubits."
```

**Hình ảnh cần:**
- Sơ đồ tổng quan hệ thống
- Ứng dụng thực tế (nếu có)

---

#### Slide 2: Hamiltonian Fermi-Hubbard (1 phút)
**Chuẩn bị:**
- [ ] Đọc kỹ phần 1.1, 1.2 trong `solution.md`
- [ ] Hiểu rõ hopping term và interaction term
- [ ] Xem hình `presentation_plots/1_lattice_diagram.png`

**Nội dung thuyết trình:**
```
"Hamiltonian Fermi-Hubbard gồm 2 thành phần chính:

1. Hopping term (hệ số -J/2): Mô tả động năng, electron di chuyển giữa 
   các site láng giềng. J lớn thì electron phi định xứ, tạo tính kim loại.

2. Interaction term (hệ số U/4): Mô tả thế năng, tương tác Coulomb khi 
   2 electron cùng site. U > 0 thì đẩy nhau, U lớn tạo Mott insulator.

Với J=1.0 và U=0, Hamiltonian có 8 Pauli terms, chỉ gồm hopping. 
Khi U > 0, có thêm 12 interaction terms, tổng cộng 20 terms."
```

**Hình ảnh cần:**
- `presentation_plots/1_lattice_diagram.png`
- Công thức Hamiltonian (từ `solution.md`)

**Tips:**
- Chỉ tay vào sơ đồ khi giải thích hopping và interaction
- Nhấn mạnh sự cạnh tranh giữa J và U

---

### 👤 Người 2: Ansatz & VQE Algorithm (2.5 phút)

#### Slide 3: Lựa chọn Ansatz - EfficientSU2 (1 phút)
**Chuẩn bị:**
- [ ] Đọc kỹ phần 2.2, 2.3 trong `solution.md`
- [ ] Hiểu tại sao chọn EfficientSU2 thay vì UCCSD
- [ ] Xem hình `presentation_plots/2_ansatz_circuit.png`

**Nội dung thuyết trình:**
```
"Chúng em chọn EfficientSU2 ansatz vì 4 lý do chính:

1. Hardware-efficient: Chỉ dùng Ry, Rz rotations và CNOT gates, 
   dễ triển khai trên phần cứng lượng tử thực tế.

2. Linear entanglement: Cấu trúc CNOT tuyến tính phù hợp với topology 
   1D của mạng Fermi-Hubbard.

3. Số tham số hợp lý: 24 tham số (6 qubits × 2 rotations × 2 layers), 
   đủ expressive nhưng không quá phức tạp.

4. Đơn giản: Không cần fermionic libraries phức tạp.

Trade-off là ansatz này không bảo toàn số hạt chính xác, nên với U lớn 
cần dùng UCCSD."
```

**Hình ảnh cần:**
- `presentation_plots/2_ansatz_circuit.png`
- Bảng so sánh EfficientSU2 vs UCCSD (nếu có)

**Tips:**
- Giải thích circuit diagram từ trái sang phải
- Nhấn mạnh "hardware-efficient" là ưu điểm lớn

---

#### Slide 4: Quy trình VQE (1.5 phút)
**Chuẩn bị:**
- [ ] Đọc kỹ phần 3.1, 3.2, 3.3 trong `solution.md`
- [ ] Hiểu rõ quantum-classical loop
- [ ] Xem hình `presentation_plots/3_vqe_flowchart.png`

**Nội dung thuyết trình:**
```
"VQE là thuật toán hybrid quantum-classical, hoạt động theo vòng lặp:

Bước 1 - Quantum: Chuẩn bị trạng thái |ψ(θ)⟩ bằng ansatz circuit, 
         sau đó đo đạc expectation values của các Pauli terms.

Bước 2 - Classical: Tính năng lượng E(θ) từ expectation values, 
         sau đó optimizer SLSQP cập nhật tham số θ để giảm E(θ).

Bước 3: Lặp lại cho đến khi hội tụ (relative error < 5%).

Chúng em dùng SLSQP optimizer vì nó gradient-based, hội tụ nhanh 
trong 100-300 iterations. StatevectorEstimator cho phép tính chính xác 
không có shot noise, lý tưởng cho mục đích giáo dục."
```

**Hình ảnh cần:**
- `presentation_plots/3_vqe_flowchart.png`
- Animation của VQE loop (nếu có)

**Tips:**
- Chỉ vào flowchart khi giải thích từng bước
- Nhấn mạnh "hybrid" = quantum + classical

---

### 👤 Người 3: Kết quả & Kết luận (2 phút)

#### Slide 5: Kết quả Single Run (1 phút)
**Chuẩn bị:**
- [ ] Đọc kỹ phần 4.1 trong `solution.md`
- [ ] Hiểu ý nghĩa của relative error < 1%
- [ ] Xem hình `presentation_plots/4_single_run_comparison.png`

**Nội dung thuyết trình:**
```
"Kết quả cho J=1.0, U=0:

Exact energy: -2.828427 (tính bằng diagonalization)
VQE energy: -2.820 (tính bằng VQE với EfficientSU2)
Relative error: 0.3-0.5%, rất nhỏ!

VQE hội tụ trong 150-250 iterations, mất khoảng 2-3 giây trên 
statevector simulator. Điều này chứng tỏ ansatz EfficientSU2 
có đủ expressibility cho hệ 3-site với U=0."
```

**Hình ảnh cần:**
- `presentation_plots/4_single_run_comparison.png`
- Bảng so sánh Exact vs VQE

**Tips:**
- Nhấn mạnh relative error < 1% là rất tốt
- Giải thích tại sao VQE chậm hơn exact một chút

---

#### Slide 6: Nghiên cứu Hội tụ - J-Sweep (30 giây)
**Chuẩn bị:**
- [ ] Đọc kỹ phần 4.2 trong `solution.md`
- [ ] Hiểu xu hướng năng lượng theo J
- [ ] Xem hình `presentation_plots/5_j_sweep_results.png`

**Nội dung thuyết trình:**
```
"Chúng em nghiên cứu VQE với J từ 1.0 đến 5.0:

Kết quả: VQE theo sát exact energy trên toàn bộ khoảng J, 
relative error < 2% cho mọi J. Khi J tăng, năng lượng giảm 
vì kinetic energy thấp hơn. VQE rất robust, không có 
convergence issues."
```

**Hình ảnh cần:**
- `presentation_plots/5_j_sweep_results.png`

**Tips:**
- Chỉ vào biểu đồ để show VQE và Exact overlap
- Nhấn mạnh "robust" = ổn định

---

#### Slide 7: Kết luận & Ứng dụng (30 giây)
**Chuẩn bị:**
- [ ] Đọc kỹ phần 4.4 trong `solution.md`
- [ ] Xem hình `presentation_plots/6_summary_table.png`

**Nội dung thuyết trình:**
```
"Kết luận:

Ưu điểm: VQE chính xác (error < 1%), robust, nhanh.
Hạn chế: Không bảo toàn số hạt chính xác, cần UCCSD cho U lớn.

Ứng dụng: Phương pháp này có thể mở rộng cho hệ lớn hơn 
(10+ sites, 20+ qubits) nơi exact diagonalization không khả thi. 
Có thể áp dụng cho 2D lattices, time-dependent Hamiltonians, 
và nghiên cứu siêu dẫn.

Cảm ơn mọi người đã lắng nghe!"
```

**Hình ảnh cần:**
- `presentation_plots/6_summary_table.png`
- Slide "Thank you" với contact info

**Tips:**
- Nói nhanh nhưng rõ ràng
- Kết thúc với nụ cười và sẵn sàng trả lời câu hỏi

---

## Checklist chuẩn bị chung

### Trước buổi thuyết trình (1 tuần):
- [ ] Chạy `python generate_presentation_plots.py` để tạo tất cả plots
- [ ] Tạo slides PowerPoint/Google Slides với plots đã generate
- [ ] Mỗi người đọc kỹ phần của mình trong `solution.md`
- [ ] Họp nhóm lần 1: Phân công chi tiết và review slides

### Trước buổi thuyết trình (3 ngày):
- [ ] Tập thuyết trình riêng (mỗi người 2-3 lần)
- [ ] Họp nhóm lần 2: Tập thuyết trình cả nhóm, đo thời gian
- [ ] Điều chỉnh nội dung nếu quá dài/ngắn
- [ ] Chuẩn bị câu trả lời cho Q&A

### Ngày thuyết trình:
- [ ] Kiểm tra laptop, projector, remote
- [ ] Backup slides trên USB và cloud
- [ ] Mỗi người mang notes (nếu cần)
- [ ] Đến sớm 15 phút để setup

---

## Câu hỏi Q&A có thể gặp

### Câu hỏi về Ansatz:
**Q:** "Tại sao không dùng UCCSD thay vì EfficientSU2?"
**A:** "UCCSD bảo toàn số hạt chính xác hơn, nhưng phức tạp và cần 
fermionic libraries. Với hệ nhỏ (6 qubits) và U=0, EfficientSU2 
đủ chính xác và đơn giản hơn nhiều."

### Câu hỏi về VQE:
**Q:** "VQE có gặp barren plateaus không?"
**A:** "Với hệ nhỏ 6 qubits, chúng em không gặp barren plateaus. 
Vấn đề này thường xảy ra với hệ lớn hơn (20+ qubits)."

### Câu hỏi về Hardware:
**Q:** "Kết quả này có áp dụng được trên quantum hardware thật không?"
**A:** "Trên hardware thật sẽ có shot noise và gate errors. Cần thêm 
error mitigation techniques, nhưng phương pháp vẫn áp dụng được."

### Câu hỏi về Scalability:
**Q:** "Có thể mở rộng cho hệ lớn hơn không?"
**A:** "Có, VQE scale tốt hơn exact diagonalization. Với 20 qubits, 
exact cần 2^20 = 1M basis states, nhưng VQE vẫn chạy được."

---

## Tips chung cho cả nhóm

1. **Thời gian:** Tập với đồng hồ, đảm bảo không quá 6 phút
2. **Chuyển tiếp:** Người sau nói "Cảm ơn [tên người trước], tiếp theo em sẽ..."
3. **Eye contact:** Nhìn vào audience, không chỉ đọc slides
4. **Giọng nói:** Nói rõ ràng, không quá nhanh
5. **Pointer:** Dùng laser pointer hoặc chuột để chỉ vào hình
6. **Backup plan:** Nếu ai đó bị stuck, người khác sẵn sàng tiếp tục
7. **Enthusiasm:** Thể hiện sự hứng thú với đề tài!

---

## Tài liệu tham khảo

- `solution.md`: Nội dung chi tiết đầy đủ
- `fermi_hubbard_vqe.ipynb`: Code và giải thích
- `presentation_plots/`: Tất cả hình ảnh cần thiết
- `presentation_summary.md`: Tóm tắt nội dung

**Chúc các bạn thuyết trình thành công! 🎉**
