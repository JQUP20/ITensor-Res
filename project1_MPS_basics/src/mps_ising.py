#!/usr/bin/env python3
"""
MPS基础: 一维横场伊辛模型
===========================

实现矩阵乘积态(MPS)表示并计算纠缠熵，验证面积律。

作者: [Your Name]
日期: 2025-11-12
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
import argparse

try:
    import tenpy
    from tenpy.networks.mps import MPS
    from tenpy.models.tf_ising import TFIChain
    from tenpy.algorithms import dmrg
    TENPY_AVAILABLE = True
except ImportError:
    print("警告: TeNPy未安装，将使用简化实现")
    TENPY_AVAILABLE = False


class SimpleMPS:
    """
    简化的MPS实现（用于教学）
    """

    def __init__(self, L: int, d: int = 2, chi: int = 16):
        """
        初始化MPS

        参数:
            L: 系统大小（格点数）
            d: 物理维度（自旋-1/2: d=2）
            chi: 键维度（bond dimension）
        """
        self.L = L
        self.d = d
        self.chi = chi
        self.tensors = []

        # 初始化为随机态
        self._initialize_random()

    def _initialize_random(self):
        """初始化为随机MPS"""
        chi_left = 1

        for i in range(self.L):
            chi_right = min(self.chi, self.d**(i+1), self.d**(self.L-i-1))

            # 创建张量 A[i]^s: chi_left × chi_right × d
            tensor = np.random.randn(chi_left, chi_right, self.d)
            self.tensors.append(tensor)

            chi_left = chi_right

    def schmidt_decomposition(self, position: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        在指定位置进行施密特分解

        参数:
            position: 分割位置 (0 到 L-1)

        返回:
            U, S, Vt: SVD分解结果
        """
        # 合并左半部分张量
        left_tensor = self.tensors[0]
        for i in range(1, position + 1):
            # 合并张量
            tensor = self.tensors[i]
            shape = left_tensor.shape
            left_tensor = np.tensordot(left_tensor, tensor, axes=([1], [0]))
            # 重排索引: (chi_0, d_0, ..., d_i, chi_i)

        # 将左半部分reshape为矩阵
        dim_left = left_tensor.shape[0] * np.prod([self.d for _ in range(position + 1)])
        dim_right = left_tensor.shape[-1]

        matrix = left_tensor.reshape(dim_left, dim_right)

        # SVD分解
        U, S, Vt = np.linalg.svd(matrix, full_matrices=False)

        return U, S, Vt

    def entanglement_entropy(self, position: int) -> float:
        """
        计算指定键的冯诺依曼纠缠熵

        参数:
            position: 键位置

        返回:
            纠缠熵 S = -Σ λᵢ² log(λᵢ²)
        """
        _, S, _ = self.schmidt_decomposition(position)

        # 归一化施密特值
        S_normalized = S / np.linalg.norm(S)

        # 计算熵
        entropy = 0.0
        for s in S_normalized:
            if s > 1e-14:  # 避免log(0)
                p = s**2
                entropy -= p * np.log(p)

        return entropy


class TransverseFieldIsing:
    """
    横场伊辛模型类
    """

    def __init__(self, L: int, J: float = 1.0, h: float = 0.5):
        """
        初始化哈密顿量

        参数:
            L: 系统大小
            J: 耦合强度
            h: 横场强度
        """
        self.L = L
        self.J = J
        self.h = h

        # Pauli矩阵
        self.sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
        self.sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        self.sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
        self.identity = np.eye(2, dtype=complex)

    def local_hamiltonian(self, i: int) -> np.ndarray:
        """
        构建第i个格点的局域哈密顿量

        返回:
            2L × 2L 哈密顿量矩阵
        """
        H = np.zeros((2**self.L, 2**self.L), dtype=complex)

        # ZZ项
        if i < self.L - 1:
            term = self._operator_at_site(self.sigma_z, i)
            term = term @ self._operator_at_site(self.sigma_z, i + 1)
            H -= self.J * term

        # X项
        term = self._operator_at_site(self.sigma_x, i)
        H -= self.h * term

        return H

    def _operator_at_site(self, operator: np.ndarray, site: int) -> np.ndarray:
        """
        构建作用于特定格点的算符
        """
        op_list = [self.identity] * self.L
        op_list[site] = operator

        result = op_list[0]
        for op in op_list[1:]:
            result = np.kron(result, op)

        return result

    def full_hamiltonian(self) -> np.ndarray:
        """
        构建完整哈密顿量
        """
        H = np.zeros((2**self.L, 2**self.L), dtype=complex)

        for i in range(self.L):
            H += self.local_hamiltonian(i)

        return H


def compute_entanglement_profile_simple(L: int = 20, J: float = 1.0, h: float = 0.5,
                                       chi: int = 32) -> Tuple[np.ndarray, np.ndarray]:
    """
    使用简化MPS计算纠缠熵分布

    注意: 这是教学版本，实际研究应使用TeNPy
    """
    print(f"使用简化MPS (L={L}, J={J}, h={h}, χ={chi})")

    mps = SimpleMPS(L=L, d=2, chi=chi)

    positions = np.arange(1, L)
    entropies = []

    for pos in positions:
        S = mps.entanglement_entropy(pos)
        entropies.append(S)

    return positions, np.array(entropies)


def compute_entanglement_profile_tenpy(L: int = 50, J: float = 1.0, h: float = 0.5,
                                       chi: int = 64) -> Tuple[np.ndarray, np.ndarray]:
    """
    使用TeNPy计算纠缠熵分布（推荐）
    """
    print(f"使用TeNPy DMRG (L={L}, J={J}, h={h}, χ={chi})")

    # 设置模型
    model_params = {
        'L': L,
        'J': J,
        'g': h,  # TeNPy中使用g表示横场
        'bc_MPS': 'finite',
        'conserve': None
    }

    model = TFIChain(model_params)

    # 初始态
    psi = MPS.from_product_state(model.lat.mps_sites(), ['up'] * L, bc='finite')

    # DMRG参数
    dmrg_params = {
        'trunc_params': {
            'chi_max': chi,
            'svd_min': 1.e-10,
        },
        'max_E_err': 1.e-10,
        'max_sweeps': 100,
        'verbose': 1
    }

    # 运行DMRG
    info = dmrg.run(psi, model, dmrg_params)

    print(f"DMRG收敛，能量: {info['E']:.10f}")

    # 计算纠缠熵
    positions = np.arange(1, L)
    entropies = []

    for pos in positions:
        S = psi.entanglement_entropy()[pos]
        entropies.append(S)

    return positions, np.array(entropies)


def plot_entanglement_profile(results: dict, save_path: str = None):
    """
    绘制纠缠熵分布图

    参数:
        results: {label: (positions, entropies), ...}
        save_path: 保存路径
    """
    plt.figure(figsize=(10, 6))

    for label, (positions, entropies) in results.items():
        plt.plot(positions, entropies, 'o-', label=label, markersize=4)

    plt.xlabel('Bond Position', fontsize=12)
    plt.ylabel('Entanglement Entropy S', fontsize=12)
    plt.title('Entanglement Entropy Profile', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"图表已保存: {save_path}")

    plt.show()


def phase_diagram_scan(L: int = 40, chi: int = 64):
    """
    扫描相图，研究临界点附近的纠缠熵
    """
    h_values = [0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0]  # h/J比值
    J = 1.0

    results = {}

    for h in h_values:
        if TENPY_AVAILABLE:
            positions, entropies = compute_entanglement_profile_tenpy(L=L, J=J, h=h, chi=chi)
        else:
            positions, entropies = compute_entanglement_profile_simple(L=L, J=J, h=h, chi=32)

        results[f'h/J = {h:.1f}'] = (positions, entropies)

    return results


def main():
    """主程序"""
    parser = argparse.ArgumentParser(description='MPS横场伊辛模型')
    parser.add_argument('--L', type=int, default=40, help='系统大小')
    parser.add_argument('--J', type=float, default=1.0, help='耦合强度')
    parser.add_argument('--h', type=float, default=0.5, help='横场强度')
    parser.add_argument('--chi', type=int, default=64, help='键维度')
    parser.add_argument('--scan', action='store_true', help='扫描相图')
    parser.add_argument('--output', type=str, default='../results/figures/entanglement.png',
                       help='输出图表路径')

    args = parser.parse_args()

    print("=" * 60)
    print("MPS基础: 横场伊辛模型纠缠熵计算")
    print("=" * 60)

    if args.scan:
        print("\n扫描相图...")
        results = phase_diagram_scan(L=args.L, chi=args.chi)
    else:
        print(f"\n单点计算: L={args.L}, J={args.J}, h={args.h}, χ={args.chi}")

        if TENPY_AVAILABLE:
            positions, entropies = compute_entanglement_profile_tenpy(
                L=args.L, J=args.J, h=args.h, chi=args.chi
            )
        else:
            positions, entropies = compute_entanglement_profile_simple(
                L=args.L, J=args.J, h=args.h, chi=args.chi
            )

        results = {f'h/J = {args.h:.1f}': (positions, entropies)}

    # 绘图
    plot_entanglement_profile(results, save_path=args.output)

    print("\n计算完成！")


if __name__ == "__main__":
    main()
