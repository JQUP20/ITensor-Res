#!/usr/bin/env python3
"""
MPS可视化模块

专门用于项目1的可视化函数。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from typing import List, Tuple, Optional
import seaborn as sns

sns.set_style("whitegrid")


def plot_schmidt_values(schmidt_values: np.ndarray, position: int,
                       save_path: Optional[str] = None):
    """
    绘制施密特值分布

    参数:
        schmidt_values: 施密特值数组
        position: 键位置
        save_path: 保存路径
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 线性标度
    ax1.bar(range(len(schmidt_values)), schmidt_values, color='steelblue', alpha=0.7)
    ax1.set_xlabel('Schmidt Index', fontsize=12)
    ax1.set_ylabel('Schmidt Value $\\lambda_\\alpha$', fontsize=12)
    ax1.set_title(f'Schmidt Spectrum (Position {position})', fontsize=13)
    ax1.grid(True, alpha=0.3)

    # 对数标度
    sv_normalized = schmidt_values / np.linalg.norm(schmidt_values)
    ax2.semilogy(range(len(sv_normalized)), sv_normalized, 'o-',
                color='crimson', markersize=6)
    ax2.set_xlabel('Schmidt Index', fontsize=12)
    ax2.set_ylabel('Normalized Schmidt Value (log)', fontsize=12)
    ax2.set_title('Schmidt Spectrum (Log Scale)', fontsize=13)
    ax2.grid(True, alpha=0.3, which='both')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {save_path}")

    return fig, (ax1, ax2)


def plot_phase_diagram_scan(h_values: np.ndarray,
                           max_entropies: np.ndarray,
                           energies: np.ndarray,
                           J: float = 1.0,
                           save_path: Optional[str] = None):
    """
    绘制相图扫描结果

    参数:
        h_values: 横场强度数组
        max_entropies: 最大纠缠熵数组
        energies: 基态能量数组
        J: 耦合强度
        save_path: 保存路径
    """
    fig = plt.figure(figsize=(14, 5))
    gs = GridSpec(1, 3, figure=fig, wspace=0.3)

    # 子图1: 纠缠熵 vs h
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(h_values / J, max_entropies, 'o-', linewidth=2, markersize=6)
    ax1.axvline(1.0, color='red', linestyle='--', alpha=0.5, label='Critical Point')
    ax1.set_xlabel('$h/J$', fontsize=12)
    ax1.set_ylabel('Max Entanglement Entropy', fontsize=12)
    ax1.set_title('Entanglement vs Field Strength', fontsize=13)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 子图2: 能量 vs h
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(h_values / J, energies, 's-', linewidth=2, markersize=6, color='green')
    ax2.axvline(1.0, color='red', linestyle='--', alpha=0.5)
    ax2.set_xlabel('$h/J$', fontsize=12)
    ax2.set_ylabel('Ground State Energy', fontsize=12)
    ax2.set_title('Energy vs Field Strength', fontsize=13)
    ax2.grid(True, alpha=0.3)

    # 子图3: 能量导数（类似比热）
    ax3 = fig.add_subplot(gs[0, 2])
    if len(h_values) > 2:
        dE_dh = np.gradient(energies, h_values)
        ax3.plot(h_values / J, np.abs(dE_dh), '^-', linewidth=2,
                markersize=6, color='purple')
        ax3.axvline(1.0, color='red', linestyle='--', alpha=0.5)
        ax3.set_xlabel('$h/J$', fontsize=12)
        ax3.set_ylabel('$|dE/dh|$', fontsize=12)
        ax3.set_title('Energy Derivative (Susceptibility)', fontsize=13)
        ax3.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {save_path}")

    return fig


def plot_cft_scaling(positions: np.ndarray, entropies: np.ndarray,
                    c_fit: float, const_fit: float,
                    save_path: Optional[str] = None):
    """
    绘制CFT标度分析

    参数:
        positions: 位置数组
        entropies: 纠缠熵数组
        c_fit: 拟合的中心电荷
        const_fit: 拟合常数
        save_path: 保存路径
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 子图1: S vs position
    ax1.plot(positions, entropies, 'o', label='Data', markersize=6, alpha=0.7)

    # 拟合曲线
    fit_curve = (c_fit / 6) * np.log(positions) + const_fit
    ax1.plot(positions, fit_curve, '--', linewidth=2, color='red',
            label=f'Fit: $c = {c_fit:.3f}$')

    ax1.set_xlabel('Position $i$', fontsize=12)
    ax1.set_ylabel('Entanglement Entropy $S(i)$', fontsize=12)
    ax1.set_title('Entanglement Entropy Profile', fontsize=13)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 子图2: S vs log(position)
    ax2.plot(np.log(positions), entropies, 'o', label='Data',
            markersize=6, alpha=0.7)

    log_positions = np.log(positions)
    fit_line = (c_fit / 6) * log_positions + const_fit
    ax2.plot(log_positions, fit_line, '--', linewidth=2, color='red',
            label=f'Slope = $c/6 = {c_fit/6:.3f}$')

    ax2.set_xlabel('$\\log(i)$', fontsize=12)
    ax2.set_ylabel('Entanglement Entropy $S(i)$', fontsize=12)
    ax2.set_title('CFT Scaling Analysis', fontsize=13)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {save_path}")

    return fig


def plot_entanglement_spectrum_evolution(schmidt_values_list: List[np.ndarray],
                                        positions: List[int],
                                        save_path: Optional[str] = None):
    """
    绘制纠缠谱随位置的演化

    参数:
        schmidt_values_list: 施密特值列表
        positions: 对应的位置列表
        save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    # 创建2D热图数据
    max_chi = max(len(sv) for sv in schmidt_values_list)
    spectrum_matrix = np.zeros((len(positions), max_chi))

    for i, sv in enumerate(schmidt_values_list):
        spectrum = sv**2
        spectrum_matrix[i, :len(spectrum)] = spectrum

    # 绘制热图
    im = ax.imshow(spectrum_matrix.T, aspect='auto', cmap='YlOrRd',
                  origin='lower', interpolation='nearest')

    ax.set_xlabel('Bond Position', fontsize=12)
    ax.set_ylabel('Schmidt Index $\\alpha$', fontsize=12)
    ax.set_title('Entanglement Spectrum Evolution', fontsize=14)

    # 颜色条
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('$\\lambda_\\alpha^2$', fontsize=12)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {save_path}")

    return fig


def plot_comparison_with_exact(positions: np.ndarray,
                              mps_entropies: np.ndarray,
                              exact_entropies: np.ndarray,
                              save_path: Optional[str] = None):
    """
    比较MPS结果与精确对角化

    参数:
        positions: 位置数组
        mps_entropies: MPS计算的纠缠熵
        exact_entropies: 精确对角化的纠缠熵
        save_path: 保存路径
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

    # 子图1: 比较
    ax1.plot(positions, mps_entropies, 'o-', label='MPS', markersize=6)
    ax1.plot(positions, exact_entropies, 's--', label='Exact', markersize=5)
    ax1.set_xlabel('Position', fontsize=12)
    ax1.set_ylabel('Entanglement Entropy', fontsize=12)
    ax1.set_title('MPS vs Exact Diagonalization', fontsize=13)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 子图2: 相对误差
    relative_error = np.abs(mps_entropies - exact_entropies) / (exact_entropies + 1e-10)
    ax2.semilogy(positions, relative_error, 'o-', color='red', markersize=6)
    ax2.set_xlabel('Position', fontsize=12)
    ax2.set_ylabel('Relative Error', fontsize=12)
    ax2.set_title('Relative Error', fontsize=13)
    ax2.grid(True, alpha=0.3, which='both')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {save_path}")

    return fig


if __name__ == "__main__":
    # 测试可视化函数
    print("测试可视化工具...")

    # 测试施密特值绘图
    chi = 16
    sv = np.exp(-np.arange(chi) * 0.3)
    sv = sv / np.linalg.norm(sv)

    plot_schmidt_values(sv, position=10)

    # 测试相图扫描
    h_values = np.linspace(0.2, 2.0, 20)
    max_ent = 0.5 + 0.8 * np.exp(-(h_values - 1.0)**2 / 0.1)
    energies = -h_values - 0.5 * h_values**2

    plot_phase_diagram_scan(h_values, max_ent, energies)

    plt.show()
    print("✓ 测试完成")
