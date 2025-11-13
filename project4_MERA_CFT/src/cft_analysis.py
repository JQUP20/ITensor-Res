#!/usr/bin/env python3
"""
共形场论(CFT)分析工具

从MERA和数值数据提取CFT参数
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from scipy.optimize import curve_fit


class CFTAnalyzer:
    """CFT数据分析器"""

    def __init__(self):
        """初始化"""
        self.central_charges = {
            'Ising': 0.5,
            'Free Fermion': 0.5,
            '3-state Potts': 0.8,
            'Free Boson': 1.0,
            'Heisenberg': 1.0
        }

    def extract_central_charge(self, L_values: np.ndarray,
                               S_values: np.ndarray) -> Tuple[float, Dict]:
        """
        从纠缠熵提取中心荷

        S(L) = c/3 log(L) + s₀

        参数:
            L_values: 子系统尺寸
            S_values: 对应的纠缠熵

        返回:
            (中心荷, 拟合数据)
        """
        # 线性拟合 S vs log(L)
        log_L = np.log(L_values)

        coeffs = np.polyfit(log_L, S_values, 1)
        slope = coeffs[0]
        intercept = coeffs[1]

        # 中心荷
        c = 3 * slope

        # 拟合曲线
        S_fit = slope * log_L + intercept

        fit_data = {
            'L': L_values,
            'S': S_values,
            'S_fit': S_fit,
            'c': c,
            's0': intercept,
            'slope': slope
        }

        return c, fit_data

    def extract_scaling_dimensions(self, mera_tensors: List[np.ndarray]) -> Dict:
        """
        从MERA标度算符提取标度维数

        参数:
            mera_tensors: MERA张量列表

        返回:
            标度维数字典
        """
        # 简化实现：模拟数据
        scaling_dims = {
            'Identity': 0.0,
            'Energy': 0.5,
            'Spin': 0.125,
            'Disorder': 0.125
        }

        return scaling_dims

    def compute_correlation_function(self, distances: np.ndarray,
                                     Delta: float) -> np.ndarray:
        """
        计算关联函数

        ⟨O(r) O(0)⟩ ~ r^(-2Δ)

        参数:
            distances: 距离数组
            Delta: 标度维数

        返回:
            关联函数值
        """
        return distances ** (-2 * Delta)

    def plot_central_charge_extraction(self, fit_data: Dict,
                                       save_path: str = None):
        """绘制中心荷提取"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        L = fit_data['L']
        S = fit_data['S']
        S_fit = fit_data['S_fit']
        c = fit_data['c']

        # S vs log(L)
        ax1.plot(np.log(L), S, 'o', markersize=8, label='Data')
        ax1.plot(np.log(L), S_fit, '--', linewidth=2,
                label=f'Fit: c={c:.3f}')
        ax1.set_xlabel('log(L)', fontsize=12)
        ax1.set_ylabel('Entanglement Entropy S', fontsize=12)
        ax1.set_title('Central Charge Extraction', fontsize=13, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 残差
        residuals = S - S_fit
        ax2.plot(L, residuals, 'o', markersize=8)
        ax2.axhline(0, color='red', linestyle='--', linewidth=2)
        ax2.set_xlabel('L', fontsize=12)
        ax2.set_ylabel('Residuals', fontsize=12)
        ax2.set_title('Fit Quality', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()


def demonstrate_cft_extraction():
    """演示CFT参数提取"""
    print("=" * 60)
    print("CFT参数提取示例")
    print("=" * 60)

    # 模拟Ising CFT数据
    c_theory = 0.5
    L_values = 2 ** np.arange(2, 10)
    S_values = (c_theory / 3) * np.log(L_values) + 0.5 + \
               0.05 * np.random.randn(len(L_values))

    # 分析
    analyzer = CFTAnalyzer()
    c_extracted, fit_data = analyzer.extract_central_charge(L_values, S_values)

    print(f"\n中心荷提取:")
    print(f"  理论值: c = {c_theory}")
    print(f"  提取值: c = {c_extracted:.4f}")
    print(f"  误差: {abs(c_extracted - c_theory) / c_theory * 100:.2f}%")

    # 可视化
    analyzer.plot_central_charge_extraction(fit_data)

    # 标度维数
    print(f"\n常见CFT的标度维数:")
    print(f"{'Operator':<20} {'Ising (c=1/2)':<15} {'c=1':<15}")
    print("-" * 50)
    print(f"{'Identity':<20} {0:<15.3f} {0:<15.3f}")
    print(f"{'Energy':<20} {0.5:<15.3f} {1.0:<15.3f}")
    print(f"{'Spin':<20} {0.125:<15.3f} {0.25:<15.3f}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demonstrate_cft_extraction()
