"""
generate_presentation_plots.py
------------------------------
Script để tạo các biểu đồ cho thuyết trình 6 phút về Fermi-Hubbard VQE.
Chạy script này để generate tất cả plots cần thiết.

Usage:
    python generate_presentation_plots.py
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to avoid threading issues
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patches as mpatches

# Import helper functions
from fermi_hubbard_helpers import (
    build_hamiltonian,
    exact_ground_energy,
    run_vqe,
    make_ansatz,
    sweep_J,
)
from qiskit_algorithms.optimizers import SLSQP

# Set style for professional plots
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.figsize'] = (10, 6)

# Create output directory
import os
os.makedirs('presentation_plots', exist_ok=True)


# ============================================================================
# Plot 1: 3-Site Fermi-Hubbard Lattice Diagram
# ============================================================================
def plot_lattice_diagram():
    """Vẽ sơ đồ 3-site chain với hopping và interaction."""
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    # Draw sites
    sites = [2, 5, 8]
    for i, x in enumerate(sites):
        # Site box
        rect = FancyBboxPatch((x-0.4, 1.5), 0.8, 1, 
                               boxstyle="round,pad=0.1", 
                               edgecolor='black', facecolor='lightblue', linewidth=2)
        ax.add_patch(rect)
        
        # Site label
        ax.text(x, 2, f'Site {i+1}', ha='center', va='center', fontsize=14, fontweight='bold')
        
        # Spin arrows
        ax.arrow(x-0.15, 1.7, 0, 0.4, head_width=0.1, head_length=0.1, fc='red', ec='red')
        ax.text(x-0.15, 1.4, '↑', ha='center', fontsize=12, color='red')
        
        ax.arrow(x+0.15, 1.7, 0, 0.4, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
        ax.text(x+0.15, 1.4, '↓', ha='center', fontsize=12, color='blue')
    
    # Draw hopping arrows
    for i in range(len(sites)-1):
        x1, x2 = sites[i], sites[i+1]
        # Hopping arrow
        arrow = FancyArrowPatch((x1+0.4, 2.5), (x2-0.4, 2.5),
                                arrowstyle='<->', mutation_scale=20, 
                                linewidth=2, color='green')
        ax.add_patch(arrow)
        ax.text((x1+x2)/2, 2.8, f'J (hopping)', ha='center', fontsize=12, color='green')
    
    # Draw interaction symbols
    for x in sites:
        ax.text(x, 0.8, 'U (interaction)', ha='center', fontsize=11, color='purple')
        ax.plot([x-0.2, x+0.2], [1.0, 1.0], 'o-', color='purple', markersize=8, linewidth=2)
    
    ax.set_title('Mô hình Fermi-Hubbard 3-site', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('presentation_plots/1_lattice_diagram.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: presentation_plots/1_lattice_diagram.png")
    plt.close()


# ============================================================================
# Plot 2: EfficientSU2 Circuit Diagram (Simplified)
# ============================================================================
def plot_ansatz_circuit():
    """Vẽ sơ đồ circuit của EfficientSU2 ansatz."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis('off')
    
    # Qubit lines
    qubits = 6
    for i in range(qubits):
        y = 6 - i
        ax.plot([0.5, 13.5], [y, y], 'k-', linewidth=1)
        ax.text(0.2, y, f'q{i}', ha='right', va='center', fontsize=12)
    
    # Layer 1
    x_start = 1
    for i in range(qubits):
        y = 6 - i
        # Ry gate
        rect = FancyBboxPatch((x_start, y-0.2), 0.6, 0.4, 
                               boxstyle="round,pad=0.05", 
                               edgecolor='blue', facecolor='lightblue', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x_start+0.3, y, 'Ry', ha='center', va='center', fontsize=10)
        
        # Rz gate
        rect = FancyBboxPatch((x_start+0.8, y-0.2), 0.6, 0.4, 
                               boxstyle="round,pad=0.05", 
                               edgecolor='green', facecolor='lightgreen', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x_start+1.1, y, 'Rz', ha='center', va='center', fontsize=10)
    
    # CNOT chain (Layer 1)
    x_cnot = 2.8
    for i in range(qubits-1):
        y1 = 6 - i
        y2 = 6 - (i+1)
        # Control
        ax.plot(x_cnot, y1, 'ko', markersize=8)
        # Target
        ax.add_patch(plt.Circle((x_cnot, y2), 0.15, color='white', ec='black', linewidth=1.5))
        ax.plot([x_cnot-0.1, x_cnot+0.1], [y2, y2], 'k-', linewidth=1.5)
        ax.plot([x_cnot, x_cnot], [y2-0.1, y2+0.1], 'k-', linewidth=1.5)
        # Vertical line
        ax.plot([x_cnot, x_cnot], [y1, y2], 'k-', linewidth=1.5)
    
    # Layer 2 (similar structure)
    x_start2 = 4
    for i in range(qubits):
        y = 6 - i
        # Ry gate
        rect = FancyBboxPatch((x_start2, y-0.2), 0.6, 0.4, 
                               boxstyle="round,pad=0.05", 
                               edgecolor='blue', facecolor='lightblue', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x_start2+0.3, y, 'Ry', ha='center', va='center', fontsize=10)
        
        # Rz gate
        rect = FancyBboxPatch((x_start2+0.8, y-0.2), 0.6, 0.4, 
                               boxstyle="round,pad=0.05", 
                               edgecolor='green', facecolor='lightgreen', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x_start2+1.1, y, 'Rz', ha='center', va='center', fontsize=10)
    
    # CNOT chain (Layer 2)
    x_cnot2 = 5.8
    for i in range(qubits-1):
        y1 = 6 - i
        y2 = 6 - (i+1)
        # Control
        ax.plot(x_cnot2, y1, 'ko', markersize=8)
        # Target
        ax.add_patch(plt.Circle((x_cnot2, y2), 0.15, color='white', ec='black', linewidth=1.5))
        ax.plot([x_cnot2-0.1, x_cnot2+0.1], [y2, y2], 'k-', linewidth=1.5)
        ax.plot([x_cnot2, x_cnot2], [y2-0.1, y2+0.1], 'k-', linewidth=1.5)
        # Vertical line
        ax.plot([x_cnot2, x_cnot2], [y1, y2], 'k-', linewidth=1.5)
    
    # Labels
    ax.text(2, 6.8, 'Layer 1', ha='center', fontsize=14, fontweight='bold')
    ax.text(5, 6.8, 'Layer 2', ha='center', fontsize=14, fontweight='bold')
    
    ax.set_title('EfficientSU2 Ansatz Circuit (reps=2, entanglement=linear)', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor='lightblue', edgecolor='blue', label='Ry rotation'),
        mpatches.Patch(facecolor='lightgreen', edgecolor='green', label='Rz rotation'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='k', markersize=8, label='CNOT control'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='w', markeredgecolor='k', markersize=10, label='CNOT target')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('presentation_plots/2_ansatz_circuit.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: presentation_plots/2_ansatz_circuit.png")
    plt.close()


# ============================================================================
# Plot 3: VQE Flowchart
# ============================================================================
def plot_vqe_flowchart():
    """Vẽ flowchart của VQE algorithm."""
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Box positions - using LaTeX for math symbols
    boxes = [
        (5, 13, r'Khởi tạo' + '\n' + r'$\theta_0$', 'lightblue'),
        (5, 11, r'Quantum:' + '\n' + r'Chuẩn bị $|\psi(\theta)\rangle$', 'lightgreen'),
        (5, 9, r'Quantum:' + '\n' + r'Đo đạc $\langle P_i \rangle$', 'lightgreen'),
        (5, 7, r'Classical:' + '\n' + r'Tính $E(\theta)$', 'lightyellow'),
        (5, 5, r'Classical:' + '\n' + r'Optimizer' + '\n' + r'cập nhật $\theta$', 'lightyellow'),
        (5, 3, 'Hội tụ?', 'lightcoral'),
        (5, 1, r'Trả về' + '\n' + r'$E_{min}, \theta_{opt}$', 'lightblue'),
    ]
    
    for x, y, text, color in boxes:
        if 'Hội tụ' in text:
            # Diamond shape for decision
            rect = FancyBboxPatch((x-0.8, y-0.4), 1.6, 0.8, 
                                   boxstyle="round,pad=0.1", 
                                   edgecolor='black', facecolor=color, linewidth=2)
        else:
            rect = FancyBboxPatch((x-1, y-0.4), 2, 0.8, 
                                   boxstyle="round,pad=0.1", 
                                   edgecolor='black', facecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Arrows
    arrows = [
        (5, 12.6, 5, 11.4),  # Init -> Prepare
        (5, 10.6, 5, 9.4),   # Prepare -> Measure
        (5, 8.6, 5, 7.4),    # Measure -> Compute
        (5, 6.6, 5, 5.4),    # Compute -> Optimize
        (5, 4.6, 5, 3.4),    # Optimize -> Converge?
        (5, 2.6, 5, 1.4),    # Yes -> Return
    ]
    
    for x1, y1, x2, y2 in arrows:
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                arrowstyle='->', mutation_scale=20, 
                                linewidth=2, color='black')
        ax.add_patch(arrow)
    
    # Loop back arrow (No -> Optimize)
    ax.annotate('', xy=(6.5, 5), xytext=(6.5, 3),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    ax.annotate('', xy=(6.5, 5), xytext=(7, 5),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    ax.text(7.5, 4, 'Không', fontsize=11, color='red', fontweight='bold')
    
    # Yes label
    ax.text(5.5, 2.5, 'Có', fontsize=11, color='green', fontweight='bold')
    
    # Section labels
    ax.text(0.5, 10, 'Quantum\nComputer', ha='left', fontsize=12, 
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    ax.text(0.5, 6, 'Classical\nComputer', ha='left', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    
    ax.set_title('VQE Algorithm Flowchart', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('presentation_plots/3_vqe_flowchart.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: presentation_plots/3_vqe_flowchart.png")
    plt.close()


# ============================================================================
# Plot 4: Single Run Results - Simple and Clear Comparison
# ============================================================================
def plot_single_run_results():
    """Vẽ biểu đồ so sánh đơn giản và rõ ràng Exact vs VQE energy."""
    # Run VQE for J=1.0, U=0
    H = build_hamiltonian(J=1.0, U=0.0)
    exact_energy = exact_ground_energy(H)
    
    ansatz = make_ansatz(num_qubits=6, reps=2)
    optimizer = SLSQP(maxiter=500)
    vqe_result = run_vqe(H, ansatz, optimizer, seed=42)
    vqe_energy = vqe_result.eigenvalue
    
    # Get number of iterations
    n_iterations = getattr(vqe_result.optimizer_result, 'nfev', 'N/A')
    
    # Create single clear plot
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Bar chart
    x_pos = [0, 1]
    methods = ['Exact Diagonalization', 'VQE (EfficientSU2)']
    energies = [exact_energy, vqe_energy]
    colors = ['#3498db', '#e74c3c']
    
    bars = ax.bar(x_pos, energies, color=colors, alpha=0.85, edgecolor='black', linewidth=2.5, width=0.5)
    
    # Add energy values on top of bars
    for i, (bar, energy) in enumerate(zip(bars, energies)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{energy:.6f}',
                ha='center', va='bottom', fontsize=16, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', linewidth=1.5))
    
    # Add method descriptions below x-axis
    ax.text(0, min(energies) * 1.25, 
            'Phương pháp: Diagonalization\nThời gian: < 1 giây\nĐộ chính xác: 100%',
            ha='center', fontsize=11, 
            bbox=dict(boxstyle='round,pad=0.8', facecolor='lightblue', alpha=0.7, edgecolor='blue', linewidth=1.5))
    
    ax.text(1, min(energies) * 1.25, 
            f'Phương pháp: Quantum VQE\nThời gian: 2-3 giây\nIterations: {n_iterations}',
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round,pad=0.8', facecolor='lightcoral', alpha=0.7, edgecolor='red', linewidth=1.5))
    
    # Calculate and display relative error prominently
    rel_error = abs(vqe_energy - exact_energy) / abs(exact_energy) * 100
    
    # Add arrow showing the difference
    ax.annotate('', xy=(1, vqe_energy), xytext=(1, exact_energy),
                arrowprops=dict(arrowstyle='<->', color='green', lw=3))
    ax.text(1.15, (exact_energy + vqe_energy) / 2, 
            f'Sai số:\n{rel_error:.3f}%',
            fontsize=12, fontweight='bold', color='green',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', edgecolor='green', linewidth=2))
    
    # Add horizontal line at exact energy for reference
    ax.axhline(y=exact_energy, color='gray', linestyle='--', linewidth=1.5, alpha=0.5, label='Exact Energy Reference')
    
    # Big result box at top
    result_text = f'KẾT QUẢ: VQE đạt độ chính xác {100-rel_error:.2f}% so với Exact'
    ax.text(0.5, max(energies) * 0.92, result_text,
            ha='center', fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=1', facecolor='yellow', alpha=0.9, edgecolor='orange', linewidth=3))
    
    # Labels and formatting
    ax.set_ylabel('Ground State Energy (Hartree)', fontsize=15, fontweight='bold')
    ax.set_xlabel('Phương pháp tính toán', fontsize=15, fontweight='bold')
    ax.set_title('So sánh Exact Diagonalization vs VQE\n(Fermi-Hubbard 3-site, J=1.0, U=0)', 
                 fontsize=17, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(methods, fontsize=13, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1)
    ax.set_ylim([min(energies) * 1.35, max(energies) * 0.85])
    
    # Add legend
    ax.legend(loc='lower right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('presentation_plots/4_single_run_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: presentation_plots/4_single_run_comparison.png")
    plt.close()


# ============================================================================
# Plot 5: J-Sweep Results - Line Plot
# ============================================================================
def plot_j_sweep_results():
    """Vẽ line plot VQE vs Exact energy theo J."""
    # Run J-sweep
    J_values = np.linspace(1.0, 5.0, 5)
    print("Running J-sweep (this may take a few minutes)...")
    sweep_result = sweep_J(J_values, U=0.0)
    
    # Create line plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Plot 1: Energy comparison
    ax1.plot(sweep_result.param_values, sweep_result.exact_energies, 
             'o-', label='Exact', linewidth=3, markersize=10, color='#2E86AB')
    ax1.plot(sweep_result.param_values, sweep_result.vqe_energies, 
             's-', label='VQE', linewidth=3, markersize=10, color='#A23B72')
    
    # Highlight points with error > 1%
    for i, J in enumerate(sweep_result.param_values):
        if sweep_result.relative_errors[i] > 0.01:
            ax1.plot(J, sweep_result.vqe_energies[i], 'ro', 
                     markersize=15, markerfacecolor='none', markeredgewidth=3,
                     label='Error > 1%' if i == 0 else '')
    
    ax1.set_ylabel('Ground State Energy', fontsize=14, fontweight='bold')
    ax1.set_title('VQE vs Exact Energy (U=0)', fontsize=16, fontweight='bold')
    ax1.legend(fontsize=12, loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Relative error
    ax2.plot(sweep_result.param_values, 
             [err * 100 for err in sweep_result.relative_errors],
             'o-', linewidth=3, markersize=10, color='#F18F01')
    ax2.axhline(y=1, color='red', linestyle='--', linewidth=2, label='1% threshold')
    ax2.axhline(y=5, color='orange', linestyle='--', linewidth=2, label='5% threshold')
    
    ax2.set_xlabel('Hopping Parameter J', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Relative Error (%)', fontsize=14, fontweight='bold')
    ax2.set_title('VQE Relative Error vs J', fontsize=16, fontweight='bold')
    ax2.legend(fontsize=12, loc='best')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('presentation_plots/5_j_sweep_results.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: presentation_plots/5_j_sweep_results.png")
    plt.close()


# ============================================================================
# Plot 6: Summary Table
# ============================================================================
def plot_summary_table():
    """Vẽ bảng tóm tắt ưu/nhược điểm."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    # Table data - using (+) and (-) instead of checkmark symbols
    data = [
        ['Tiêu chí', 'Ưu điểm (+)', 'Nhược điểm (-)'],
        ['Độ chính xác', 'Error < 1% cho U=0', 'Không bảo toàn số hạt chính xác'],
        ['Hiệu suất', 'Nhanh (2-3s)', 'Phụ thuộc khởi tạo tham số'],
        ['Robustness', 'Ổn định với nhiều J', 'Cần UCCSD cho U lớn'],
        ['Scalability', 'Mở rộng được cho hệ lớn', 'Cần error mitigation cho hardware'],
        ['Đơn giản', 'Dễ triển khai', 'Không phù hợp strongly correlated'],
    ]
    
    # Create table
    table = ax.table(cellText=data, cellLoc='left', loc='center',
                     colWidths=[0.2, 0.4, 0.4])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    # Style header row
    for i in range(3):
        cell = table[(0, i)]
        cell.set_facecolor('#2E86AB')
        cell.set_text_props(weight='bold', color='white', fontsize=13)
    
    # Style data rows
    for i in range(1, len(data)):
        # Tiêu chí column
        table[(i, 0)].set_facecolor('#E8F4F8')
        table[(i, 0)].set_text_props(weight='bold')
        
        # Ưu điểm column
        table[(i, 1)].set_facecolor('#D4EDDA')
        
        # Nhược điểm column
        table[(i, 2)].set_facecolor('#F8D7DA')
    
    ax.set_title('Tóm tắt: VQE với EfficientSU2 Ansatz', 
                 fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('presentation_plots/6_summary_table.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: presentation_plots/6_summary_table.png")
    plt.close()


# ============================================================================
# Main execution
# ============================================================================
if __name__ == '__main__':
    print("=" * 60)
    print("Generating presentation plots for Fermi-Hubbard VQE")
    print("=" * 60)
    
    print("\n[1/6] Creating lattice diagram...")
    plot_lattice_diagram()
    
    print("\n[2/6] Creating ansatz circuit diagram...")
    plot_ansatz_circuit()
    
    print("\n[3/6] Creating VQE flowchart...")
    plot_vqe_flowchart()
    
    print("\n[4/6] Running single VQE and creating comparison chart...")
    plot_single_run_results()
    
    print("\n[5/6] Running J-sweep and creating results plot...")
    plot_j_sweep_results()
    
    print("\n[6/6] Creating summary table...")
    plot_summary_table()
    
    print("\n" + "=" * 60)
    print("✓ All plots generated successfully!")
    print("✓ Plots saved in: presentation_plots/")
    print("=" * 60)
