#!/usr/bin/env python3
"""
Levin-Wen String-Net模型

实现String-Net液体和融合范畴
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class FusionCategory:
    """融合范畴数据"""
    objects: List[str]
    fusion_rules: Dict[Tuple[str, str], List[str]]
    quantum_dims: Dict[str, float]
    F_symbols: Optional[Dict] = None

    @property
    def total_quantum_dim(self) -> float:
        """总量子维数 D = √(Σd_a²)"""
        return np.sqrt(sum(d**2 for d in self.quantum_dims.values()))


class FibonacciCategory:
    """Fibonacci融合范畴"""

    def __init__(self):
        """初始化Fibonacci范畴"""
        self.phi = (1 + np.sqrt(5)) / 2  # 黄金比例

        # 对象
        self.objects = ['1', 'tau']

        # 融合规则
        self.fusion_rules = {
            ('1', '1'): ['1'],
            ('1', 'tau'): ['tau'],
            ('tau', '1'): ['tau'],
            ('tau', 'tau'): ['1', 'tau']
        }

        # 量子维数
        self.quantum_dims = {
            '1': 1.0,
            'tau': self.phi
        }

        # 总量子维数
        self.D = np.sqrt(1 + self.phi**2)

        # F-符号
        self._init_F_symbols()

    def _init_F_symbols(self):
        """初始化F-符号"""
        # Fibonacci最重要的F-符号：F^{τττ}_{τττ}
        self.F_tau_tau_tau = np.array([
            [self.phi**(-1), self.phi**(-0.5)],
            [self.phi**(-0.5), -self.phi**(-1)]
        ])

    def get_fusion(self, a: str, b: str) -> List[str]:
        """获取融合结果"""
        return self.fusion_rules.get((a, b), [])

    def get_F_symbol(self, a, b, c, d, e, f):
        """获取F-符号（简化）"""
        if all(x == 'tau' for x in [a, b, c, d, e, f]):
            return self.F_tau_tau_tau
        elif '1' in [a, b, c]:
            # 单位元情况：平凡
            return np.array([[1.0]])
        else:
            # 其他情况需要完整实现
            return np.array([[1.0]])

    def print_info(self):
        """打印范畴信息"""
        print("=" * 60)
        print("Fibonacci融合范畴")
        print("=" * 60)

        print(f"\n对象: {self.objects}")

        print(f"\n融合规则:")
        for (a, b), result in self.fusion_rules.items():
            result_str = " + ".join(result)
            print(f"  {a} × {b} = {result_str}")

        print(f"\n量子维数:")
        for obj, dim in self.quantum_dims.items():
            print(f"  d_{obj} = {dim:.6f}")

        print(f"\n总量子维数:")
        print(f"  𝒟 = {self.D:.6f}")
        print(f"  ln(𝒟) = {np.log(self.D):.6f} (拓扑纠缠熵)")

        print(f"\nF-符号 F^{{τττ}}_{{τττ}}:")
        print(self.F_tau_tau_tau)


class Z2Category:
    """Z₂融合范畴（Toric Code）"""

    def __init__(self):
        """初始化Z₂范畴"""
        self.objects = ['1', 'e']

        self.fusion_rules = {
            ('1', '1'): ['1'],
            ('1', 'e'): ['e'],
            ('e', '1'): ['e'],
            ('e', 'e'): ['1']
        }

        self.quantum_dims = {
            '1': 1.0,
            'e': 1.0
        }

        self.D = 2.0  # √(1² + 1²) = √2 ... 等等，应该是√(1² + 1² + 1² + 1²) = 2

    def print_info(self):
        """打印范畴信息"""
        print("=" * 60)
        print("Z₂融合范畴")
        print("=" * 60)

        print(f"\n对象: {self.objects}")

        print(f"\n融合规则 (群乘法):")
        for (a, b), result in self.fusion_rules.items():
            print(f"  {a} × {b} = {result[0]}")

        print(f"\n量子维数: 全为1 (阿贝尔)")

        print(f"\n总量子维数:")
        print(f"  𝒟 = {self.D:.6f}")
        print(f"  ln(𝒟) = {np.log(self.D):.6f}")


class StringNetState:
    """String-Net态"""

    def __init__(self, category: FibonacciCategory, Lx: int, Ly: int):
        """
        初始化String-Net态

        参数:
            category: 融合范畴
            Lx, Ly: 格子尺寸
        """
        self.category = category
        self.Lx = Lx
        self.Ly = Ly

        # 初始化弦网配置（简化）
        self.config = self._init_config()

    def _init_config(self) -> np.ndarray:
        """初始化弦网配置"""
        # 简化：每条边随机分配弦类型
        n_edges = self.Lx * self.Ly * 3  # 蜂窝格估计
        config = np.zeros(n_edges, dtype=int)
        return config

    def apply_vertex_operator(self, vertex: int) -> bool:
        """
        应用顶点算符

        检查融合规则是否满足

        参数:
            vertex: 顶点索引

        返回:
            是否满足融合规则
        """
        # 简化实现
        return True

    def apply_plaquette_operator(self, plaquette: int) -> complex:
        """
        应用plaquette算符

        参数:
            plaquette: plaquette索引

        返回:
            算符期望值
        """
        # 简化实现：返回1
        return 1.0 + 0j

    def compute_ground_state_energy(self) -> float:
        """计算基态能量"""
        # E = -∑Q_v - ∑B_p
        # 简化：所有算符期望值为1
        n_vertices = self.Lx * self.Ly * 2
        n_plaquettes = self.Lx * self.Ly

        E = -(n_vertices + n_plaquettes)
        return E


def demonstrate_fibonacci():
    """演示Fibonacci范畴"""
    print("\n" + "=" * 60)
    print("Fibonacci任意子与拓扑量子计算")
    print("=" * 60)

    fib = FibonacciCategory()
    fib.print_info()

    # 编织统计
    print("\n" + "=" * 60)
    print("编织统计")
    print("=" * 60)

    print("\nFibonacci任意子的特殊性质:")
    print("1. 非阿贝尔统计")
    print("2. 量子维数 d_τ = φ (无理数!)")
    print("3. τ × τ = 1 + τ (融合到Hilbert空间)")
    print("4. 拓扑量子计算通用性")

    # 融合树
    print("\n融合过程示例:")
    print("  τ × τ = 1 + τ")
    print("  τ × τ × τ = (1 + τ) × τ = τ + (1 + τ) = 1 + 2τ")

    # F-移动可视化
    print("\nF-移动 (重新括号):")
    print("  (τ × τ) × τ  <-F->  τ × (τ × τ)")
    print("     |                      |")
    print("  (1+τ) × τ             τ × (1+τ)")
    print("     |                      |")
    print("   τ + (1+τ)            τ + (1+τ)")

    # 可视化F-符号
    fig, ax = plt.subplots(figsize=(10, 8))

    F_matrix = fib.F_tau_tau_tau
    im = ax.imshow(np.abs(F_matrix), cmap='RdBu_r', aspect='auto')
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(['1', 'τ'])
    ax.set_yticklabels(['1', 'τ'])
    ax.set_title('Fibonacci F-Symbol: $F^{τττ}_{τττ}$',
                fontsize=14, fontweight='bold')

    # 标注数值
    for i in range(2):
        for j in range(2):
            text = ax.text(j, i, f'{F_matrix[i, j]:.4f}',
                          ha="center", va="center", color="black", fontsize=12)

    plt.colorbar(im, ax=ax, label='|F|')
    plt.tight_layout()
    plt.savefig('fibonacci_F_symbol.png', dpi=300)
    print("\n图表已保存: fibonacci_F_symbol.png")
    plt.show()


def compare_categories():
    """比较不同融合范畴"""
    print("\n" + "=" * 60)
    print("融合范畴比较")
    print("=" * 60)

    categories = {
        'Z₂': {'D': 2.0, 'abelian': True, 'TQC': False},
        'Fibonacci': {'D': (1 + np.sqrt(5)) / 2 * np.sqrt(2),
                      'abelian': False, 'TQC': True},
        'Ising': {'D': 2.0, 'abelian': False, 'TQC': False},
    }

    print(f"\n{'Category':<15} {'𝒟':<12} {'Abelian':<10} {'Universal TQC':<15}")
    print("-" * 60)

    for name, props in categories.items():
        print(f"{name:<15} {props['D']:<12.4f} "
              f"{'Yes' if props['abelian'] else 'No':<10} "
              f"{'Yes' if props['TQC'] else 'No':<15}")

    # 可视化
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    names = list(categories.keys())
    D_values = [props['D'] for props in categories.values()]
    S_topo = [np.log(D) for D in D_values]

    # 总量子维数
    ax1.bar(names, D_values, color=['blue', 'orange', 'green'],
           edgecolor='black', linewidth=2, alpha=0.7)
    ax1.set_ylabel('Total Quantum Dimension 𝒟', fontsize=12)
    ax1.set_title('Total Quantum Dimension', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')

    # 拓扑纠缠熵
    ax2.bar(names, S_topo, color=['blue', 'orange', 'green'],
           edgecolor='black', linewidth=2, alpha=0.7)
    ax2.set_ylabel('Topological Entropy ln(𝒟)', fontsize=12)
    ax2.set_title('Topological Entanglement Entropy', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('categories_comparison.png', dpi=300)
    print("\n图表已保存: categories_comparison.png")
    plt.show()


def main():
    """主程序"""
    print("\n" + "=" * 60)
    print("String-Net液体与融合范畴")
    print("=" * 60)

    # Fibonacci演示
    demonstrate_fibonacci()

    # Z₂范畴
    print("\n")
    z2 = Z2Category()
    z2.print_info()

    # 比较
    compare_categories()

    print("\n" + "=" * 60)
    print("总结")
    print("=" * 60)
    print("\nString-Net理论的意义:")
    print("1. 统一框架：描述所有2D拓扑序")
    print("2. 数学基础：融合范畴理论")
    print("3. 应用前景：拓扑量子计算")
    print("4. 理论价值：深化对拓扑序的理解")
    print("=" * 60)


if __name__ == "__main__":
    main()
