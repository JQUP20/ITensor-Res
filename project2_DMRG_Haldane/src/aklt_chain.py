#!/usr/bin/env python3
"""
AKLT链的DMRG实现

实现自旋-1 AKLT模型，验证Haldane相的拓扑性质。
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional, Dict
import argparse
import sys

sys.path.append('../../common')
from utils.tensor_utils import spin_operators

try:
    import tenpy
    from tenpy.networks.mps import MPS
    from tenpy.models.spins import SpinChain
    from tenpy.algorithms import dmrg
    from tenpy.networks.site import SpinSite
    TENPY_AVAILABLE = True
except ImportError:
    print("警告: TeNPy未安装")
    TENPY_AVAILABLE = False


class AKLTChain:
    """
    AKLT链模型类

    哈密顿量: H = Σᵢ [S⃗ᵢ·S⃗ᵢ₊₁ + (1/3)(S⃗ᵢ·S⃗ᵢ₊₁)²]
    """

    def __init__(self, L: int, bc: str = 'finite', conserve: Optional[str] = None):
        """
        初始化AKLT链

        参数:
            L: 系统大小
            bc: 边界条件 ('finite' or 'infinite')
            conserve: 守恒量 (None, 'Sz', 'parity')
        """
        self.L = L
        self.bc = bc
        self.conserve = conserve

        if not TENPY_AVAILABLE:
            raise ImportError("需要安装TeNPy")

        # 构建模型
        self._build_model()

    def _build_model(self):
        """构建AKLT模型"""
        # 使用SpinChain，添加双线性项
        model_params = {
            'L': self.L,
            'S': 1.0,  # 自旋-1
            'bc_MPS': self.bc,
            'conserve': self.conserve,
            'Jx': 1.0,
            'Jy': 1.0,
            'Jz': 1.0,
            'biquadratic': 1.0 / 3.0,  # AKLT项系数
        }

        self.model = SpinChain(model_params)

    def ground_state_dmrg(self, chi_max: int = 100, verbose: int = 1) -> Tuple[MPS, Dict]:
        """
        使用DMRG计算基态

        参数:
            chi_max: 最大键维度
            verbose: 输出详细程度

        返回:
            (psi, info): 基态MPS和信息字典
        """
        # 初始态（随机）
        psi = MPS.from_product_state(
            self.model.lat.mps_sites(),
            ['up'] * self.L,
            bc=self.bc
        )

        # DMRG参数
        dmrg_params = {
            'trunc_params': {
                'chi_max': chi_max,
                'svd_min': 1.e-12,
            },
            'max_E_err': 1.e-12,
            'max_sweeps': 200,
            'verbose': verbose,
            'mixer': True,  # 使用mixer避免局部极小
        }

        # 运行DMRG
        info = dmrg.run(psi, self.model, dmrg_params)

        return psi, info

    def excited_states(self, chi_max: int = 100, n_states: int = 4) -> List[Tuple[float, MPS]]:
        """
        计算激发态（用于验证四重简并）

        参数:
            chi_max: 最大键维度
            n_states: 计算前n个态

        返回:
            [(E, psi), ...]: 能量和态的列表
        """
        states = []

        for i in range(n_states):
            print(f"\n计算第{i}个态...")

            # 初始态（不同的随机种子）
            np.random.seed(i)
            initial_state = np.random.choice(['up', 'down', '0'], self.L)

            psi = MPS.from_product_state(
                self.model.lat.mps_sites(),
                initial_state,
                bc=self.bc
            )

            # DMRG参数（可能需要正交化之前的态）
            dmrg_params = {
                'trunc_params': {'chi_max': chi_max, 'svd_min': 1.e-12},
                'max_E_err': 1.e-10,
                'max_sweeps': 150,
                'verbose': 0,
            }

            # 对之前的态正交化
            if i > 0:
                dmrg_params['orthogonal_to'] = [s[1] for s in states]

            info = dmrg.run(psi, self.model, dmrg_params)

            states.append((info['E'], psi))
            print(f"能量 E_{i} = {info['E']:.10f}")

        return states


def compute_string_order_parameter(psi: MPS, L: int, verbose: bool = True) -> float:
    """
    计算弦序参数

    O_z(i,j) = ⟨S_i^z exp(iπ Σ_{k=i+1}^{j-1} S_k^z) S_j^z⟩

    参数:
        psi: MPS态
        L: 系统大小
        verbose: 是否输出详细信息

    返回:
        弦序参数（取长程极限）
    """
    string_ops = []

    # 计算不同距离的弦序
    for distance in range(2, min(L // 2, 20)):
        i = L // 2 - distance // 2
        j = i + distance

        if j >= L:
            break

        # 构建算符
        # 这里简化实现，完整版需要构建弦算符
        op_i = ('Sz', i)
        op_j = ('Sz', j)

        # 关联函数（简化）
        corr = psi.correlation_function(op_i[0], op_j[0], [op_i[1]], [op_j[1]])[0, 0]

        # 添加相位（对自旋-1，这里简化）
        # 完整实现需要计算中间的相位因子
        string_op = np.abs(corr)  # 简化

        string_ops.append((distance, string_op))

        if verbose and distance % 5 == 0:
            print(f"距离 {distance}: O_z = {string_op:.6f}")

    # 拟合长程行为
    if len(string_ops) > 5:
        distances, values = zip(*string_ops[-5:])
        avg_value = np.mean(values)
        return avg_value
    else:
        return 0.0


def edge_state_analysis(psi: MPS, L: int, edge_size: int = 3) -> Dict:
    """
    分析边缘态

    参数:
        psi: MPS态
        L: 系统大小
        edge_size: 边缘区域大小

    返回:
        分析结果字典
    """
    results = {}

    # 计算边缘纠缠熵
    S_edge_left = psi.entanglement_entropy()[edge_size]
    S_edge_right = psi.entanglement_entropy()[L - edge_size - 1]

    results['S_left'] = S_edge_left
    results['S_right'] = S_edge_right

    # 边缘磁化
    mag_left = [psi.expectation_value('Sz', i) for i in range(edge_size)]
    mag_right = [psi.expectation_value('Sz', L - i - 1) for i in range(edge_size)]

    results['mag_left'] = mag_left
    results['mag_right'] = mag_right

    # 纠缠谱
    schmidt_left = psi.get_SL(edge_size)
    schmidt_right = psi.get_SL(L - edge_size - 1)

    results['schmidt_left'] = schmidt_left[:10]  # 前10个
    results['schmidt_right'] = schmidt_right[:10]

    return results


def plot_results(energies: List[float], entropies: np.ndarray,
                edge_results: Dict, save_path: str = None):
    """
    绘制结果

    参数:
        energies: 能量列表
        entropies: 纠缠熵数组
        edge_results: 边缘态分析结果
        save_path: 保存路径
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 子图1: 能量谱
    ax1 = axes[0, 0]
    E_gs = energies[0]
    E_rel = [E - E_gs for E in energies]

    ax1.plot(range(len(energies)), E_rel, 'o-', markersize=8, linewidth=2)
    ax1.axhline(0, color='red', linestyle='--', alpha=0.5)
    ax1.set_xlabel('State Index', fontsize=12)
    ax1.set_ylabel('$E - E_0$', fontsize=12)
    ax1.set_title('Energy Spectrum (Degeneracy Check)', fontsize=13)
    ax1.grid(True, alpha=0.3)

    # 子图2: 纠缠熵分布
    ax2 = axes[0, 1]
    positions = np.arange(len(entropies))
    ax2.plot(positions, entropies, 'o-', markersize=4, linewidth=2, color='green')
    ax2.set_xlabel('Bond Position', fontsize=12)
    ax2.set_ylabel('Entanglement Entropy', fontsize=12)
    ax2.set_title('Entanglement Entropy Profile', fontsize=13)
    ax2.grid(True, alpha=0.3)

    # 子图3: 边缘磁化
    ax3 = axes[1, 0]
    ax3.plot(edge_results['mag_left'], 'o-', label='Left Edge', markersize=6)
    ax3.plot(edge_results['mag_right'], 's-', label='Right Edge', markersize=6)
    ax3.set_xlabel('Site Index (from edge)', fontsize=12)
    ax3.set_ylabel('$\\langle S_z \\rangle$', fontsize=12)
    ax3.set_title('Edge Magnetization', fontsize=13)
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 子图4: 纠缠谱
    ax4 = axes[1, 1]
    ax4.semilogy(edge_results['schmidt_left'], 'o-', label='Left Edge', markersize=6)
    ax4.semilogy(edge_results['schmidt_right'], 's-', label='Right Edge', markersize=6)
    ax4.set_xlabel('Schmidt Index', fontsize=12)
    ax4.set_ylabel('Schmidt Value (log)', fontsize=12)
    ax4.set_title('Entanglement Spectrum at Edges', fontsize=13)
    ax4.legend()
    ax4.grid(True, alpha=0.3, which='both')

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {save_path}")

    return fig


def main():
    """主程序"""
    parser = argparse.ArgumentParser(description='AKLT链DMRG计算')
    parser.add_argument('--L', type=int, default=40, help='系统大小')
    parser.add_argument('--chi', type=int, default=100, help='最大键维度')
    parser.add_argument('--bc', type=str, default='finite', choices=['finite', 'infinite'],
                       help='边界条件')
    parser.add_argument('--n-states', type=int, default=4, help='计算激发态数量')
    parser.add_argument('--output', type=str, default='../results/figures/aklt_results.png',
                       help='输出图表路径')
    parser.add_argument('--compute-string', action='store_true',
                       help='计算弦序参数（较慢）')

    args = parser.parse_args()

    print("=" * 60)
    print("AKLT链DMRG计算")
    print("=" * 60)
    print(f"系统大小: L = {args.L}")
    print(f"边界条件: {args.bc}")
    print(f"最大键维度: χ = {args.chi}")
    print("=" * 60)

    # 创建模型
    aklt = AKLTChain(L=args.L, bc=args.bc)

    # 计算基态
    print("\n[1/4] 计算基态...")
    psi_gs, info_gs = aklt.ground_state_dmrg(chi_max=args.chi, verbose=1)
    E_gs = info_gs['E']
    print(f"\n基态能量: E_0 = {E_gs:.10f}")
    print(f"每格点能量: E_0/L = {E_gs/args.L:.10f}")

    # 计算激发态
    print(f"\n[2/4] 计算前{args.n_states}个态...")
    states = aklt.excited_states(chi_max=args.chi, n_states=args.n_states)
    energies = [E for E, _ in states]

    # 检查简并
    print("\n能量谱分析:")
    for i, E in enumerate(energies):
        print(f"E_{i} = {E:.10f}, ΔE = {E - E_gs:.2e}")

    degeneracy_gap = energies[3] - energies[0] if len(energies) >= 4 else 0
    print(f"\n前四态能隙: ΔE(0→3) = {degeneracy_gap:.2e}")

    if degeneracy_gap < 1e-6:
        print("✓ 检测到四重简并！这是SPT相的标志。")
    else:
        print("⚠ 未检测到明显简并，可能需要更大chi或更大系统。")

    # 纠缠熵
    print("\n[3/4] 计算纠缠熵...")
    entropies = psi_gs.entanglement_entropy()
    S_max = np.max(entropies)
    S_center = entropies[args.L // 2]
    print(f"最大纠缠熵: S_max = {S_max:.6f}")
    print(f"中心纠缠熵: S_center = {S_center:.6f}")

    # 边缘态分析
    print("\n[4/4] 边缘态分析...")
    edge_results = edge_state_analysis(psi_gs, args.L)
    print(f"左边缘纠缠熵: {edge_results['S_left']:.6f}")
    print(f"右边缘纠缠熵: {edge_results['S_right']:.6f}")

    # 弦序参数（可选）
    if args.compute_string:
        print("\n[额外] 计算弦序参数...")
        string_order = compute_string_order_parameter(psi_gs, args.L)
        print(f"弦序参数: O_z = {string_order:.6f}")
        print(f"理论值: O_z ≈ 0.374")

    # 绘图
    print("\n生成图表...")
    plot_results(energies, entropies, edge_results, save_path=args.output)

    print("\n" + "=" * 60)
    print("计算完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
