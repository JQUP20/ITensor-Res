"""
张量网络可视化工具

提供常用的绘图函数。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple, Optional
import seaborn as sns

# 设置样式
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 10


def plot_entanglement_profile(positions: np.ndarray,
                              entropies: np.ndarray,
                              labels: Optional[List[str]] = None,
                              title: str = "Entanglement Entropy Profile",
                              save_path: Optional[str] = None):
    """
    绘制纠缠熵分布图

    参数:
        positions: 位置数组
        entropies: 纠缠熵数组 (可以是2D数组，每行一条曲线)
        labels: 标签列表
        title: 图表标题
        save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    if entropies.ndim == 1:
        entropies = entropies.reshape(1, -1)
        labels = [labels] if labels else ['Entropy']

    colors = sns.color_palette("husl", len(entropies))

    for i, entropy in enumerate(entropies):
        label = labels[i] if labels else f"Series {i+1}"
        ax.plot(positions, entropy, 'o-', label=label,
               color=colors[i], markersize=4, linewidth=2)

    ax.set_xlabel('Bond Position', fontsize=12)
    ax.set_ylabel('Entanglement Entropy $S$', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {save_path}")

    plt.tight_layout()
    return fig, ax


def plot_mps_structure(L: int, chi_values: List[int],
                      save_path: Optional[str] = None):
    """
    绘制MPS结构示意图

    参数:
        L: 系统大小
        chi_values: 各键的维度
        save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(12, 4))

    # 绘制物理指标
    for i in range(L):
        x = i * 2
        # 张量
        rect = patches.Rectangle((x - 0.3, 0), 0.6, 0.6,
                                 linewidth=2, edgecolor='black',
                                 facecolor='lightblue')
        ax.add_patch(rect)
        ax.text(x, 0.3, f'$A^{{{i+1}}}$', ha='center', va='center',
               fontsize=10, fontweight='bold')

        # 物理指标
        ax.arrow(x, 0.6, 0, 0.4, head_width=0.15, head_length=0.1,
                fc='red', ec='red')
        ax.text(x, 1.2, f'$s_{{{i+1}}}$', ha='center', fontsize=9)

        # 键
        if i < L - 1:
            ax.plot([x + 0.3, x + 1.7], [0.3, 0.3], 'b-', linewidth=3)
            chi = chi_values[i] if i < len(chi_values) else '?'
            ax.text(x + 1, 0.5, f'$\\chi={chi}$', ha='center',
                   fontsize=8, color='blue')

    ax.set_xlim(-1, L * 2)
    ax.set_ylim(-0.5, 1.5)
    ax.axis('off')
    ax.set_title('MPS Structure', fontsize=14, fontweight='bold')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.tight_layout()
    return fig, ax


def plot_phase_diagram(x_values: np.ndarray,
                      y_values: np.ndarray,
                      z_values: np.ndarray,
                      xlabel: str = 'Parameter 1',
                      ylabel: str = 'Parameter 2',
                      zlabel: str = 'Observable',
                      title: str = 'Phase Diagram',
                      save_path: Optional[str] = None):
    """
    绘制相图

    参数:
        x_values, y_values: 参数网格
        z_values: 观测量值
        xlabel, ylabel, zlabel: 标签
        title: 标题
        save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    contour = ax.contourf(x_values, y_values, z_values,
                         levels=20, cmap='viridis')
    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label(zlabel, fontsize=12)

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.tight_layout()
    return fig, ax


def plot_correlation_function(distances: np.ndarray,
                             correlations: np.ndarray,
                             fit_curve: Optional[np.ndarray] = None,
                             title: str = 'Correlation Function',
                             log_scale: bool = True,
                             save_path: Optional[str] = None):
    """
    绘制关联函数

    参数:
        distances: 距离数组
        correlations: 关联函数值
        fit_curve: 拟合曲线 (可选)
        title: 标题
        log_scale: 是否使用对数坐标
        save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(distances, np.abs(correlations), 'o',
           label='Data', markersize=6)

    if fit_curve is not None:
        ax.plot(distances, fit_curve, '--',
               label='Fit', linewidth=2, color='red')

    if log_scale:
        ax.set_yscale('log')

    ax.set_xlabel('Distance $r$', fontsize=12)
    ax.set_ylabel('$|C(r)|$', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.tight_layout()
    return fig, ax


def plot_energy_spectrum(energies: np.ndarray,
                        degeneracies: Optional[List[int]] = None,
                        title: str = 'Energy Spectrum',
                        save_path: Optional[str] = None):
    """
    绘制能量谱

    参数:
        energies: 能量数组
        degeneracies: 简并度 (可选)
        title: 标题
        save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    if degeneracies is None:
        degeneracies = [1] * len(energies)

    # 相对于基态能量
    E_gs = energies[0]
    energies_rel = energies - E_gs

    colors = ['red' if d > 1 else 'blue' for d in degeneracies]

    ax.scatter(range(len(energies)), energies_rel,
              s=[d * 50 for d in degeneracies],
              c=colors, alpha=0.6)

    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)

    ax.set_xlabel('State Index', fontsize=12)
    ax.set_ylabel('$E - E_0$', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.grid(True, alpha=0.3)

    # 添加图例
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w',
              markerfacecolor='blue', markersize=8,
              label='Non-degenerate'),
        Line2D([0], [0], marker='o', color='w',
              markerfacecolor='red', markersize=8,
              label='Degenerate')
    ]
    ax.legend(handles=legend_elements)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.tight_layout()
    return fig, ax


if __name__ == "__main__":
    # 测试绘图函数
    print("测试可视化工具...")

    # 测试纠缠熵分布
    L = 20
    positions = np.arange(1, L)
    entropies = np.log(positions + 1) + np.random.randn(L - 1) * 0.1

    plot_entanglement_profile(positions, entropies,
                              title="Test: Entanglement Profile")

    # 测试MPS结构
    plot_mps_structure(L=5, chi_values=[2, 4, 4, 2])

    plt.show()
    print("✓ 测试完成")
