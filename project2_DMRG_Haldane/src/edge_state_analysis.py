#!/usr/bin/env python3
"""
边缘态详细分析工具

分析Haldane链的边缘态性质
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict, List
import sys

sys.path.append('../../common')

try:
    from tenpy.networks.mps import MPS
    from tenpy.algorithms import dmrg
    TENPY_AVAILABLE = True
except ImportError:
    TENPY_AVAILABLE = False


class EdgeStateAnalyzer:
    """
    边缘态分析器
    """

    def __init__(self, psi: MPS, L: int):
        """
        初始化

        参数:
            psi: MPS态
            L: 系统大小
        """
        self.psi = psi
        self.L = L

    def edge_magnetization(self, edge_width: int = 5) -> Dict:
        """
        计算边缘磁化

        参数:
            edge_width: 边缘区域宽度

        返回:
            磁化数据字典
        """
        mag_left = []
        mag_right = []

        for i in range(edge_width):
            # 左边缘
            m_l = self.psi.expectation_value('Sz', i)
            mag_left.append(m_l)

            # 右边缘
            m_r = self.psi.expectation_value('Sz', self.L - i - 1)
            mag_right.append(m_r)

        return {
            'left': np.array(mag_left),
            'right': np.array(mag_right),
            'positions_left': np.arange(edge_width),
            'positions_right': np.arange(edge_width)
        }

    def edge_entanglement_spectrum(self, position: int = 3) -> np.ndarray:
        """
        计算边缘纠缠谱

        参数:
            position: 边缘附近的键位置

        返回:
            施密特值数组
        """
        return self.psi.get_SL(position)

    def bulk_vs_edge_comparison(self) -> Dict:
        """
        比较体和边缘的性质

        返回:
            比较数据
        """
        # 体中心
        center = self.L // 2
        S_bulk = self.psi.get_SL(center)

        # 边缘
        S_edge_left = self.psi.get_SL(3)
        S_edge_right = self.psi.get_SL(self.L - 4)

        return {
            'bulk_schmidt': S_bulk,
            'edge_left_schmidt': S_edge_left,
            'edge_right_schmidt': S_edge_right,
            'bulk_entropy': self.psi.entanglement_entropy()[center],
            'edge_left_entropy': self.psi.entanglement_entropy()[3],
            'edge_right_entropy': self.psi.entanglement_entropy()[self.L - 4]
        }


def plot_edge_magnetization(mag_data: Dict, save_path: str = None):
    """
    绘制边缘磁化

    参数:
        mag_data: 磁化数据
        save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(mag_data['positions_left'], mag_data['left'],
           'o-', markersize=8, linewidth=2, label='Left Edge')
    ax.plot(mag_data['positions_right'], mag_data['right'],
           's-', markersize=8, linewidth=2, label='Right Edge')

    ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('Distance from Edge', fontsize=12)
    ax.set_ylabel('$\\langle S^z \\rangle$', fontsize=12)
    ax.set_title('Edge Magnetization Profile', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.tight_layout()
    return fig


def plot_entanglement_spectrum_comparison(bulk_schmidt: np.ndarray,
                                         edge_schmidt: np.ndarray,
                                         save_path: str = None):
    """
    比较体和边缘的纠缠谱

    参数:
        bulk_schmidt: 体的施密特值
        edge_schmidt: 边缘的施密特值
        save_path: 保存路径
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 纠缠谱
    ax1.semilogy(range(len(bulk_schmidt)), bulk_schmidt,
                'o-', markersize=6, label='Bulk')
    ax1.semilogy(range(len(edge_schmidt)), edge_schmidt,
                's-', markersize=6, label='Edge')
    ax1.set_xlabel('Schmidt Index', fontsize=12)
    ax1.set_ylabel('Schmidt Value (log)', fontsize=12)
    ax1.set_title('Entanglement Spectrum', fontsize=13)
    ax1.legend()
    ax1.grid(True, alpha=0.3, which='both')

    # 累积分布
    cum_bulk = np.cumsum(bulk_schmidt**2)
    cum_edge = np.cumsum(edge_schmidt**2)

    ax2.plot(range(len(cum_bulk)), cum_bulk,
            'o-', markersize=6, label='Bulk')
    ax2.plot(range(len(cum_edge)), cum_edge,
            's-', markersize=6, label='Edge')
    ax2.axhline(np.log(2), color='red', linestyle='--',
               alpha=0.5, label='$\\ln 2$ (Edge Theory)')
    ax2.set_xlabel('Number of States', fontsize=12)
    ax2.set_ylabel('Cumulative Weight', fontsize=12)
    ax2.set_title('Cumulative Distribution', fontsize=13)
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.tight_layout()
    return fig


def analyze_edge_state_degeneracy(energies: List[float],
                                  threshold: float = 1e-4) -> Dict:
    """
    分析能级简并度

    参数:
        energies: 能量列表
        threshold: 简并判定阈值

    返回:
        简并分析结果
    """
    E_sorted = np.sort(energies)
    E_rel = E_sorted - E_sorted[0]

    # 找简并的能级
    degenerate_groups = []
    current_group = [0]

    for i in range(1, len(E_rel)):
        if E_rel[i] - E_rel[current_group[0]] < threshold:
            current_group.append(i)
        else:
            if len(current_group) > 1:
                degenerate_groups.append(current_group)
            current_group = [i]

    if len(current_group) > 1:
        degenerate_groups.append(current_group)

    results = {
        'energies': E_sorted,
        'relative_energies': E_rel,
        'degenerate_groups': degenerate_groups,
        'ground_state_degeneracy': len(degenerate_groups[0]) if degenerate_groups else 1
    }

    return results


def plot_degeneracy_analysis(degeneracy_data: Dict, save_path: str = None):
    """
    绘制简并度分析

    参数:
        degeneracy_data: 简并度数据
        save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    E_rel = degeneracy_data['relative_energies']
    degenerate_groups = degeneracy_data['degenerate_groups']

    # 绘制能级
    colors = ['red' if i in degenerate_groups[0] else 'blue'
             for i in range(len(E_rel))]

    ax.scatter(range(len(E_rel)), E_rel,
              c=colors, s=150, alpha=0.7, edgecolors='black', linewidth=2)

    # 标记简并度
    if degenerate_groups:
        gsd = len(degenerate_groups[0])
        ax.text(len(E_rel) * 0.7, max(E_rel) * 0.8,
               f'Ground State Degeneracy: {gsd}\\n(Expected: 4 for OBC)',
               fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat'))

    ax.set_xlabel('State Index', fontsize=12)
    ax.set_ylabel('Relative Energy (J)', fontsize=12)
    ax.set_title('Energy Spectrum and Degeneracy Analysis', fontsize=14)
    ax.grid(True, alpha=0.3, axis='y')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    plt.tight_layout()
    return fig


def main():
    """主程序"""
    print("=" * 60)
    print("边缘态分析工具")
    print("=" * 60)

    if not TENPY_AVAILABLE:
        print("需要TeNPy库")
        print("这里提供分析框架和可视化示例")

    # 模拟数据示例
    print("\n生成示例数据...")

    # 模拟边缘磁化
    mag_data = {
        'left': 0.1 * np.random.randn(5),
        'right': 0.1 * np.random.randn(5),
        'positions_left': np.arange(5),
        'positions_right': np.arange(5)
    }

    plot_edge_magnetization(mag_data)

    # 模拟简并度
    energies = [-10.0, -10.0001, -9.9999, -10.0002,  # 四重简并
                -9.5, -9.2, -8.8]  # 激发态

    degeneracy_data = analyze_edge_state_degeneracy(energies)
    print(f"\n基态简并度: {degeneracy_data['ground_state_degeneracy']}")

    plot_degeneracy_analysis(degeneracy_data)

    plt.show()

    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
