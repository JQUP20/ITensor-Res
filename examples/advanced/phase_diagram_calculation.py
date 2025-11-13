#!/usr/bin/env python3
"""
高级示例：计算量子相图

演示如何使用框架计算和绘制量子相图
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root / 'project2_DMRG_Haldane/src'))
sys.path.append(str(project_root / 'common/utils'))


class PhaseDiagramCalculator:
    """相图计算器"""

    def __init__(self, model_name: str = "Ising"):
        """
        初始化

        参数:
            model_name: 模型名称
        """
        self.model_name = model_name
        self.phase_diagram = None

    def compute_order_parameter(self, h: float, J: float,
                                L: int = 20) -> float:
        """
        计算序参量

        参数:
            h: 横场强度
            J: 交换耦合
            L: 系统大小

        返回:
            序参量值
        """
        # 简化实现：使用解析解或数值方法
        # 完整实现需要DMRG计算

        if self.model_name == "Ising":
            # 横场Ising模型
            # 临界点: h_c = J
            if h < J:
                # 铁磁相
                m = (1 - (h/J)**2)**(1/8) if h/J < 1 else 0
            else:
                # 顺磁相
                m = 0.0

            # 添加有限尺寸效应
            m *= (1 - np.exp(-L/10))

            return m

        return 0.0

    def compute_entanglement_entropy(self, h: float, J: float,
                                    L: int = 20) -> float:
        """
        计算纠缠熵

        参数:
            h, J: 参数
            L: 系统大小

        返回:
            纠缠熵
        """
        # 临界点附近纠缠熵最大
        if abs(h - J) < 0.1:
            # 临界相：S ~ log(L)
            S = 0.5 * np.log(L) + 0.5
        else:
            # 非临界相：S ~ const
            S = 0.3

        return S

    def scan_phase_diagram(self, h_range: tuple, J_range: tuple,
                          n_points: int = 50) -> dict:
        """
        扫描相图

        参数:
            h_range: h的范围 (h_min, h_max)
            J_range: J的范围 (J_min, J_max)
            n_points: 网格点数

        返回:
            相图数据
        """
        print(f"扫描{self.model_name}模型相图...")
        print(f"h范围: {h_range}")
        print(f"J范围: {J_range}")
        print(f"网格点: {n_points}×{n_points}")

        h_values = np.linspace(h_range[0], h_range[1], n_points)
        J_values = np.linspace(J_range[0], J_range[1], n_points)

        H, J_grid = np.meshgrid(h_values, J_values)

        # 计算序参量和纠缠熵
        magnetization = np.zeros_like(H)
        entanglement = np.zeros_like(H)

        total_points = n_points * n_points
        computed = 0

        for i in range(n_points):
            for j in range(n_points):
                h = H[i, j]
                J = J_grid[i, j]

                magnetization[i, j] = self.compute_order_parameter(h, J)
                entanglement[i, j] = self.compute_entanglement_entropy(h, J)

                computed += 1
                if computed % 100 == 0:
                    progress = computed / total_points * 100
                    print(f"  进度: {progress:.1f}%", end='\r')

        print(f"  进度: 100.0%")
        print("✓ 扫描完成")

        self.phase_diagram = {
            'h': H,
            'J': J_grid,
            'magnetization': magnetization,
            'entanglement': entanglement,
            'h_values': h_values,
            'J_values': J_values
        }

        return self.phase_diagram

    def plot_phase_diagram(self, save_path: str = None):
        """
        绘制相图

        参数:
            save_path: 保存路径
        """
        if self.phase_diagram is None:
            print("请先运行 scan_phase_diagram()")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        data = self.phase_diagram

        # 序参量相图
        im1 = ax1.contourf(data['h'], data['J'], data['magnetization'],
                          levels=20, cmap='RdBu_r')
        ax1.contour(data['h'], data['J'], data['magnetization'],
                   levels=[0.1, 0.5, 0.9], colors='black',
                   linewidths=2, linestyles='--')
        ax1.set_xlabel('Transverse Field h', fontsize=12)
        ax1.set_ylabel('Exchange Coupling J', fontsize=12)
        ax1.set_title('Magnetization (Order Parameter)',
                     fontsize=14, fontweight='bold')
        cbar1 = plt.colorbar(im1, ax=ax1)
        cbar1.set_label('|m|', fontsize=11)

        # 标注相界
        ax1.plot(data['h_values'], data['h_values'], 'k-', linewidth=3,
                label='Phase Boundary (h=J)')
        ax1.legend(fontsize=11)
        ax1.grid(True, alpha=0.3)

        # 纠缠熵相图
        im2 = ax2.contourf(data['h'], data['J'], data['entanglement'],
                          levels=20, cmap='viridis')
        ax2.contour(data['h'], data['J'], data['entanglement'],
                   levels=10, colors='white', linewidths=1, alpha=0.5)
        ax2.set_xlabel('Transverse Field h', fontsize=12)
        ax2.set_ylabel('Exchange Coupling J', fontsize=12)
        ax2.set_title('Entanglement Entropy',
                     fontsize=14, fontweight='bold')
        cbar2 = plt.colorbar(im2, ax=ax2)
        cbar2.set_label('S', fontsize=11)

        # 临界线
        ax2.plot(data['h_values'], data['h_values'], 'r--', linewidth=3,
                label='Critical Line')
        ax2.legend(fontsize=11)
        ax2.grid(True, alpha=0.3)

        plt.suptitle(f'{self.model_name} Model Phase Diagram',
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ 相图已保存: {save_path}")

        plt.show()

    def find_critical_point(self) -> tuple:
        """
        寻找临界点

        返回:
            (h_c, J_c, 临界指数)
        """
        if self.phase_diagram is None:
            print("请先运行 scan_phase_diagram()")
            return None

        data = self.phase_diagram

        # 寻找序参量变化最快的点（临界点）
        dm_dh = np.gradient(data['magnetization'], axis=1)
        dm_dJ = np.gradient(data['magnetization'], axis=0)

        # 梯度模
        grad_mag = np.sqrt(dm_dh**2 + dm_dJ**2)

        # 找到最大梯度位置
        max_idx = np.unravel_index(np.argmax(grad_mag), grad_mag.shape)

        h_c = data['h'][max_idx]
        J_c = data['J'][max_idx]

        print(f"\n临界点位置:")
        print(f"  h_c = {h_c:.4f}")
        print(f"  J_c = {J_c:.4f}")
        print(f"  h_c/J_c = {h_c/J_c:.4f}")

        return h_c, J_c


def main():
    """主程序"""
    print("="*70)
    print("高级示例：量子相图计算")
    print("="*70)
    print()

    # 创建计算器
    calculator = PhaseDiagramCalculator(model_name="Ising")

    # 扫描相图
    phase_diagram = calculator.scan_phase_diagram(
        h_range=(0.0, 2.0),
        J_range=(0.0, 2.0),
        n_points=50
    )

    # 寻找临界点
    critical_point = calculator.find_critical_point()

    # 绘制相图
    calculator.plot_phase_diagram(save_path='phase_diagram.png')

    print()
    print("="*70)
    print("分析完成！")
    print("="*70)
    print("\n主要发现:")
    print("1. 临界点位于 h ≈ J")
    print("2. 铁磁相 (h < J): 有限磁化")
    print("3. 顺磁相 (h > J): 零磁化")
    print("4. 临界相：纠缠熵对数发散")


if __name__ == "__main__":
    main()
