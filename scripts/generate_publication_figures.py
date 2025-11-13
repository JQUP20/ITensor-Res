#!/usr/bin/env python3
"""
生成发表级图表

提供统一的matplotlib配置和高质量图表生成
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from pathlib import Path

# 发表级配置
PUBLICATION_CONFIG = {
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.figsize': (6, 4),
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'lines.linewidth': 1.5,
    'lines.markersize': 6,
    'axes.linewidth': 1.0,
    'grid.linewidth': 0.5,
    'xtick.major.width': 1.0,
    'ytick.major.width': 1.0,
    'text.usetex': False,  # Set True if LaTeX available
}


def setup_publication_style():
    """设置发表级matplotlib样式"""
    mpl.rcParams.update(PUBLICATION_CONFIG)
    print("✓ 已设置发表级样式")


def create_figure(width=6, height=4, nrows=1, ncols=1):
    """
    创建发表级图表

    参数:
        width: 宽度（英寸）
        height: 高度（英寸）
        nrows, ncols: 子图网格

    返回:
        fig, axes
    """
    fig, axes = plt.subplots(nrows, ncols, figsize=(width, height))
    return fig, axes


class PublicationFigure:
    """发表级图表生成器"""

    def __init__(self, output_dir: str = "figures"):
        """
        初始化

        参数:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        setup_publication_style()

    def save_figure(self, fig, filename: str, formats=['pdf', 'png']):
        """
        保存图表为多种格式

        参数:
            fig: matplotlib图表对象
            filename: 文件名（不含扩展名）
            formats: 保存格式列表
        """
        for fmt in formats:
            filepath = self.output_dir / f"{filename}.{fmt}"
            fig.savefig(filepath, format=fmt, dpi=300, bbox_inches='tight')
            print(f"  ✓ 已保存: {filepath}")

    def entanglement_scaling_figure(self):
        """
        Figure 1: 纠缠熵标度

        适用于Project 1, 4
        """
        print("\n生成 Figure 1: 纠缠熵标度")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # 数据（模拟）
        L_values = 2**np.arange(3, 11)

        # (a) CFT临界标度
        c = 0.5  # Ising
        S_cft = (c/3) * np.log(L_values) + 0.5

        ax1.plot(L_values, S_cft, 'o-', label=f'CFT c={c}',
                markersize=8, linewidth=2)
        ax1.set_xscale('log', base=2)
        ax1.set_xlabel('System Size $L$')
        ax1.set_ylabel('Entanglement Entropy $S$')
        ax1.set_title('(a) Critical System')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # (b) 面积律
        S_area = 0.3 * np.ones_like(L_values)
        S_area += 0.05 * np.random.randn(len(L_values))

        ax2.plot(L_values, S_area, 's-', label='Gapped Phase',
                markersize=8, linewidth=2, color='C1')
        ax2.axhline(0.3, color='red', linestyle='--',
                   linewidth=2, label='Area Law')
        ax2.set_xscale('log', base=2)
        ax2.set_xlabel('System Size $L$')
        ax2.set_ylabel('Entanglement Entropy $S$')
        ax2.set_title('(b) Gapped System')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.suptitle('Entanglement Entropy Scaling Laws',
                    fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()

        self.save_figure(fig, 'fig1_entanglement_scaling')
        return fig

    def topological_invariants_figure(self):
        """
        Figure 2: 拓扑不变量

        适用于Project 2, 3
        """
        print("\n生成 Figure 2: 拓扑不变量")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # (a) 弦序参数
        L_values = np.arange(10, 51, 2)
        string_order = 0.4 * np.exp(-L_values/50) + 0.6

        ax1.plot(L_values, string_order, 'o-', markersize=6, linewidth=2)
        ax1.axhline(0.6, color='red', linestyle='--',
                   linewidth=2, label='Thermodynamic Limit')
        ax1.set_xlabel('Separation $r$')
        ax1.set_ylabel('String Order Parameter $O_s(r)$')
        ax1.set_title('(a) String Order (Haldane Phase)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # (b) 拓扑纠缠熵
        categories = ['Trivial', '$\\mathbb{Z}_2$', 'Fibonacci', 'Ising']
        S_topo_values = [0, np.log(2), np.log((1+np.sqrt(5))/2*np.sqrt(2)),
                        np.log(2)]

        bars = ax2.bar(categories, S_topo_values,
                      color=['gray', 'blue', 'orange', 'green'],
                      edgecolor='black', linewidth=2, alpha=0.7)

        ax2.set_ylabel('Topological Entropy $S_{\\rm topo}$')
        ax2.set_title('(b) Topological Entanglement Entropy')
        ax2.grid(True, alpha=0.3, axis='y')

        # 标注数值
        for bar, val in zip(bars, S_topo_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.3f}',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

        plt.tight_layout()
        self.save_figure(fig, 'fig2_topological_invariants')
        return fig

    def phase_diagram_figure(self):
        """
        Figure 3: 量子相图

        适用于所有项目
        """
        print("\n生成 Figure 3: 量子相图")

        fig, ax = plt.subplots(figsize=(8, 6))

        # 模拟相图数据
        h = np.linspace(0, 2, 100)
        J = np.linspace(0, 2, 100)
        H, J_grid = np.meshgrid(h, J)

        # 序参量
        magnetization = np.where(H < J_grid,
                                (1 - (H/J_grid)**2)**(1/8),
                                0)

        # 绘制
        im = ax.contourf(H, J_grid, magnetization,
                        levels=20, cmap='RdBu_r')
        ax.contour(H, J_grid, magnetization,
                  levels=[0.1, 0.5, 0.9],
                  colors='black', linewidths=2, linestyles='--')

        # 相界
        ax.plot(h, h, 'k-', linewidth=3, label='Phase Boundary')

        # 标注相
        ax.text(0.5, 1.5, 'Paramagnetic', fontsize=14, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        ax.text(1.5, 0.5, 'Ferromagnetic', fontsize=14, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        ax.set_xlabel('Transverse Field $h/J$')
        ax.set_ylabel('Exchange Coupling $J$')
        ax.set_title('Quantum Phase Diagram: Transverse-Field Ising Model',
                    fontsize=14, fontweight='bold')
        ax.legend(fontsize=12, loc='upper left')

        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Magnetization $|m|$', fontsize=12)

        plt.tight_layout()
        self.save_figure(fig, 'fig3_phase_diagram')
        return fig

    def fusion_rules_figure(self):
        """
        Figure 4: 融合规则

        适用于Project 5, 6
        """
        print("\n生成 Figure 4: 融合规则")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # (a) Fibonacci融合树
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 8)
        ax1.axis('off')
        ax1.set_title('(a) Fibonacci Fusion: $\\tau \\times \\tau = 1 + \\tau$',
                     fontsize=12, fontweight='bold')

        # 绘制简化的融合树
        ax1.text(5, 6, '$\\tau$', ha='center', fontsize=14,
                bbox=dict(boxstyle='circle', facecolor='orange', alpha=0.8))
        ax1.text(3, 6, '$\\tau$', ha='center', fontsize=14,
                bbox=dict(boxstyle='circle', facecolor='orange', alpha=0.8))
        ax1.text(7, 6, '$\\tau$', ha='center', fontsize=14,
                bbox=dict(boxstyle='circle', facecolor='orange', alpha=0.8))

        ax1.annotate('', xy=(3.5, 5.5), xytext=(2.5, 4.5),
                    arrowprops=dict(arrowstyle='->', lw=2))
        ax1.annotate('', xy=(6.5, 5.5), xytext=(7.5, 4.5),
                    arrowprops=dict(arrowstyle='->', lw=2))

        ax1.text(2, 3.5, '$1$', ha='center', fontsize=14,
                bbox=dict(boxstyle='circle', facecolor='lightblue', alpha=0.8))
        ax1.text(8, 3.5, '$\\tau$', ha='center', fontsize=14,
                bbox=dict(boxstyle='circle', facecolor='orange', alpha=0.8))

        # (b) 量子维数
        phi = (1 + np.sqrt(5)) / 2
        objects = ['$1$', '$\\tau$']
        dims = [1, phi]

        bars = ax2.bar(objects, dims, color=['lightblue', 'orange'],
                      edgecolor='black', linewidth=2, alpha=0.7, width=0.5)

        for bar, val in zip(bars, dims):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.4f}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')

        ax2.axhline(phi, color='red', linestyle='--', linewidth=2,
                   label='$\\phi$ (Golden Ratio)')
        ax2.set_ylabel('Quantum Dimension $d_a$', fontsize=12)
        ax2.set_title('(b) Quantum Dimensions', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        self.save_figure(fig, 'fig4_fusion_rules')
        return fig

    def generate_all_figures(self):
        """生成所有标准图表"""
        print("="*70)
        print("生成所有发表级图表")
        print("="*70)

        self.entanglement_scaling_figure()
        self.topological_invariants_figure()
        self.phase_diagram_figure()
        self.fusion_rules_figure()

        print()
        print("="*70)
        print("✓ 所有图表生成完成!")
        print(f"✓ 保存位置: {self.output_dir.absolute()}")
        print("="*70)


def main():
    """主程序"""
    generator = PublicationFigure(output_dir="publication_figures")
    generator.generate_all_figures()


if __name__ == "__main__":
    main()
