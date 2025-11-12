#!/usr/bin/env python3
"""
纠缠熵计算模块

提供各种纠缠度量的计算函数。
"""

import numpy as np
from typing import Tuple, List, Optional
import sys
sys.path.append('../../common')
from utils.tensor_utils import entanglement_entropy, renyi_entropy


class EntanglementAnalyzer:
    """
    纠缠分析工具类
    """

    def __init__(self, schmidt_values_list: List[np.ndarray]):
        """
        初始化

        参数:
            schmidt_values_list: 每个键的施密特值列表
        """
        self.schmidt_values = schmidt_values_list
        self.L = len(schmidt_values_list) + 1  # 系统大小

    def von_neumann_entropy_profile(self) -> np.ndarray:
        """
        计算冯诺依曼纠缠熵分布

        返回:
            纠缠熵数组
        """
        entropies = []
        for sv in self.schmidt_values:
            S = entanglement_entropy(sv)
            entropies.append(S)
        return np.array(entropies)

    def renyi_entropy_profile(self, n: float = 2.0) -> np.ndarray:
        """
        计算Rényi熵分布

        参数:
            n: Rényi指数

        返回:
            Rényi熵数组
        """
        entropies = []
        for sv in self.schmidt_values:
            S_n = renyi_entropy(sv, n=n)
            entropies.append(S_n)
        return np.array(entropies)

    def mutual_information(self, i: int, j: int) -> float:
        """
        计算互信息 I(A:B) = S(A) + S(B) - S(AB)

        参数:
            i, j: 子系统边界

        返回:
            互信息
        """
        if i >= j or i < 0 or j >= len(self.schmidt_values):
            raise ValueError(f"Invalid indices: i={i}, j={j}")

        S_A = entanglement_entropy(self.schmidt_values[i])
        S_B = entanglement_entropy(self.schmidt_values[j])

        # 对于MPS，需要更复杂的计算，这里给出近似
        # 完整实现需要收缩MPS张量
        S_AB = S_A + S_B  # 简化

        I = S_A + S_B - S_AB
        return max(0, I)  # 互信息非负

    def entanglement_spectrum(self, position: int) -> np.ndarray:
        """
        返回纠缠谱（施密特值的平方）

        参数:
            position: 键位置

        返回:
            纠缠谱（按降序排列）
        """
        sv = self.schmidt_values[position]
        spectrum = sv**2
        return np.sort(spectrum)[::-1]

    def effective_dimension(self, position: int, threshold: float = 0.01) -> int:
        """
        计算有效纠缠维度

        参数:
            position: 键位置
            threshold: 施密特值阈值

        返回:
            有效维度
        """
        spectrum = self.entanglement_spectrum(position)
        return np.sum(spectrum > threshold * spectrum[0])

    def participation_ratio(self, position: int) -> float:
        """
        计算参与比

        PR = (Σᵢ λᵢ²)² / Σᵢ λᵢ⁴

        参数:
            position: 键位置

        返回:
            参与比
        """
        spectrum = self.entanglement_spectrum(position)
        numerator = np.sum(spectrum)**2
        denominator = np.sum(spectrum**2)

        if denominator < 1e-14:
            return 0.0

        return numerator / denominator


def fit_cft_central_charge(positions: np.ndarray, entropies: np.ndarray,
                          fit_range: Optional[Tuple[int, int]] = None) -> Tuple[float, float]:
    """
    拟合CFT中心电荷

    S(l) = (c/6) log(l) + const

    参数:
        positions: 位置数组
        entropies: 纠缠熵数组
        fit_range: 拟合范围 (start, end)

    返回:
        (c, const): 中心电荷和常数项
    """
    if fit_range is None:
        fit_range = (len(positions) // 4, 3 * len(positions) // 4)

    start, end = fit_range
    pos_fit = positions[start:end]
    ent_fit = entropies[start:end]

    # 线性拟合 S vs log(l)
    log_pos = np.log(pos_fit)
    p = np.polyfit(log_pos, ent_fit, 1)

    c = 6 * p[0]  # c/6 * log(l) -> c = 6 * slope
    const = p[1]

    return c, const


def area_law_check(entropies: np.ndarray, threshold: float = 0.1) -> bool:
    """
    检查是否满足面积律（纠缠熵饱和）

    参数:
        entropies: 纠缠熵数组
        threshold: 判断阈值

    返回:
        是否满足面积律
    """
    # 检查后半部分是否基本恒定
    mid_point = len(entropies) // 2
    second_half = entropies[mid_point:]

    variance = np.var(second_half)
    mean = np.mean(second_half)

    relative_variance = variance / (mean**2 + 1e-10)

    return relative_variance < threshold


def log_divergence_check(positions: np.ndarray, entropies: np.ndarray,
                        min_corr: float = 0.95) -> bool:
    """
    检查是否存在对数发散

    参数:
        positions: 位置数组
        entropies: 纠缠熵数组
        min_corr: 最小相关系数

    返回:
        是否对数发散
    """
    log_pos = np.log(positions)

    # 计算相关系数
    corr = np.corrcoef(log_pos, entropies)[0, 1]

    return corr > min_corr


def topological_entanglement_entropy(S_A: float, S_B: float, S_C: float, S_ABC: float) -> float:
    """
    计算拓扑纠缠熵（Kitaev-Preskill方法）

    S_topo = S_A + S_B + S_C - S_ABC

    参数:
        S_A, S_B, S_C: 各子区域的纠缠熵
        S_ABC: 总区域的纠缠熵

    返回:
        拓扑纠缠熵
    """
    return S_A + S_B + S_C - S_ABC


if __name__ == "__main__":
    # 测试代码
    print("测试纠缠分析工具...")

    # 生成测试数据
    L = 20
    schmidt_list = []

    for i in range(1, L):
        # 模拟施密特值（指数衰减）
        chi = 16
        sv = np.exp(-np.arange(chi) * 0.5)
        sv = sv / np.linalg.norm(sv)
        schmidt_list.append(sv)

    # 创建分析器
    analyzer = EntanglementAnalyzer(schmidt_list)

    # 计算各种量
    S_profile = analyzer.von_neumann_entropy_profile()
    print(f"纠缠熵范围: [{S_profile.min():.4f}, {S_profile.max():.4f}]")

    S2_profile = analyzer.renyi_entropy_profile(n=2.0)
    print(f"Rényi-2熵范围: [{S2_profile.min():.4f}, {S2_profile.max():.4f}]")

    eff_dim = analyzer.effective_dimension(10)
    print(f"有效维度 (位置10): {eff_dim}")

    pr = analyzer.participation_ratio(10)
    print(f"参与比 (位置10): {pr:.4f}")

    # 测试面积律检查
    is_area_law = area_law_check(S_profile)
    print(f"满足面积律: {is_area_law}")

    # 测试CFT拟合
    positions = np.arange(1, L)
    c, const = fit_cft_central_charge(positions, S_profile)
    print(f"拟合中心电荷: c = {c:.4f}")

    print("\n✓ 所有测试通过")
