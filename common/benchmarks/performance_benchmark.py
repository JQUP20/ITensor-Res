#!/usr/bin/env python3
"""
性能基准测试

测试不同实现的性能并生成报告
"""

import numpy as np
import time
import sys
from typing import Dict, List
import matplotlib.pyplot as plt

sys.path.append('..')
from utils.tensor_utils import entanglement_entropy, spin_operators


def benchmark_entanglement_entropy(sizes: List[int], n_trials: int = 100) -> Dict:
    """
    测试纠缠熵计算性能

    参数:
        sizes: 施密特值数组大小列表
        n_trials: 每个大小的试验次数

    返回:
        性能数据字典
    """
    results = {'sizes': sizes, 'times': []}

    print("测试纠缠熵计算性能...")

    for size in sizes:
        # 生成随机施密特值
        sv = np.random.rand(size)
        sv = sv / np.linalg.norm(sv)

        times = []
        for _ in range(n_trials):
            start = time.perf_counter()
            S = entanglement_entropy(sv)
            elapsed = time.perf_counter() - start
            times.append(elapsed)

        avg_time = np.mean(times) * 1000  # 转换为毫秒
        results['times'].append(avg_time)

        print(f"  Size {size:4d}: {avg_time:.4f} ms")

    return results


def benchmark_spin_operators(S_values: List[float], n_trials: int = 100) -> Dict:
    """
    测试自旋算符生成性能

    参数:
        S_values: 自旋量子数列表
        n_trials: 试验次数

    返回:
        性能数据
    """
    results = {'S_values': S_values, 'times': []}

    print("\n测试自旋算符生成性能...")

    for S in S_values:
        times = []
        for _ in range(n_trials):
            start = time.perf_counter()
            Sx, Sy, Sz = spin_operators(S)
            elapsed = time.perf_counter() - start
            times.append(elapsed)

        avg_time = np.mean(times) * 1000
        results['times'].append(avg_time)

        dim = int(2 * S + 1)
        print(f"  S={S} (dim={dim}): {avg_time:.4f} ms")

    return results


def benchmark_matrix_operations(sizes: List[int]) -> Dict:
    """
    测试矩阵操作性能

    参数:
        sizes: 矩阵大小列表

    返回:
        性能数据
    """
    results = {
        'sizes': sizes,
        'svd_times': [],
        'eigh_times': [],
        'matmul_times': []
    }

    print("\n测试矩阵操作性能...")

    for size in sizes:
        # SVD
        A = np.random.randn(size, size)
        start = time.perf_counter()
        U, S, Vt = np.linalg.svd(A)
        svd_time = (time.perf_counter() - start) * 1000
        results['svd_times'].append(svd_time)

        # 厄米对角化
        H = A + A.T  # 对称矩阵
        start = time.perf_counter()
        eigenvalues, eigenvectors = np.linalg.eigh(H)
        eigh_time = (time.perf_counter() - start) * 1000
        results['eigh_times'].append(eigh_time)

        # 矩阵乘法
        B = np.random.randn(size, size)
        start = time.perf_counter()
        C = A @ B
        matmul_time = (time.perf_counter() - start) * 1000
        results['matmul_times'].append(matmul_time)

        print(f"  Size {size:4d}: SVD={svd_time:.2f}ms, "
              f"EIGH={eigh_time:.2f}ms, MATMUL={matmul_time:.2f}ms")

    return results


def plot_benchmark_results(results_list: List[Dict], save_path: str = None):
    """
    绘制性能测试结果

    参数:
        results_list: 结果字典列表
        save_path: 保存路径
    """
    n_plots = len(results_list)
    fig, axes = plt.subplots(1, n_plots, figsize=(6 * n_plots, 5))

    if n_plots == 1:
        axes = [axes]

    for ax, results in zip(axes, results_list):
        if 'sizes' in results:
            x = results['sizes']
            xlabel = 'Size'
        elif 'S_values' in results:
            x = results['S_values']
            xlabel = 'Spin S'
        else:
            continue

        if 'times' in results:
            ax.plot(x, results['times'], 'o-', markersize=6, linewidth=2)
            ax.set_ylabel('Time (ms)', fontsize=12)
        elif 'svd_times' in results:
            ax.plot(x, results['svd_times'], 'o-', label='SVD',
                   markersize=6, linewidth=2)
            ax.plot(x, results['eigh_times'], 's-', label='EIGH',
                   markersize=6, linewidth=2)
            ax.plot(x, results['matmul_times'], '^-', label='MATMUL',
                   markersize=6, linewidth=2)
            ax.set_ylabel('Time (ms)', fontsize=12)
            ax.set_yscale('log')
            ax.legend()

        ax.set_xlabel(xlabel, fontsize=12)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\n图表已保存: {save_path}")

    plt.show()


def generate_benchmark_report(output_file: str = 'benchmark_report.txt'):
    """
    生成完整的性能测试报告

    参数:
        output_file: 输出文件路径
    """
    print("=" * 60)
    print("性能基准测试")
    print("=" * 60)

    # 测试1: 纠缠熵
    ent_results = benchmark_entanglement_entropy(
        sizes=[10, 50, 100, 200, 500],
        n_trials=1000
    )

    # 测试2: 自旋算符
    spin_results = benchmark_spin_operators(
        S_values=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
        n_trials=500
    )

    # 测试3: 矩阵操作
    matrix_results = benchmark_matrix_operations(
        sizes=[50, 100, 200, 500, 1000]
    )

    # 生成报告
    with open(output_file, 'w') as f:
        f.write("张量网络库性能测试报告\n")
        f.write("=" * 60 + "\n\n")

        f.write("测试环境:\n")
        f.write(f"  NumPy版本: {np.__version__}\n")
        f.write(f"  Python版本: {sys.version.split()[0]}\n\n")

        f.write("测试结果摘要:\n")
        f.write("-" * 60 + "\n")

        # 纠缠熵
        f.write("\n1. 纠缠熵计算:\n")
        for size, t in zip(ent_results['sizes'], ent_results['times']):
            f.write(f"   Size {size:4d}: {t:.4f} ms\n")

        # 自旋算符
        f.write("\n2. 自旋算符生成:\n")
        for S, t in zip(spin_results['S_values'], spin_results['times']):
            dim = int(2 * S + 1)
            f.write(f"   S={S} (dim={dim}): {t:.4f} ms\n")

        # 矩阵操作
        f.write("\n3. 矩阵操作:\n")
        for size, svd_t, eigh_t, mm_t in zip(
            matrix_results['sizes'],
            matrix_results['svd_times'],
            matrix_results['eigh_times'],
            matrix_results['matmul_times']
        ):
            f.write(f"   Size {size:4d}:\n")
            f.write(f"     SVD:    {svd_t:.2f} ms\n")
            f.write(f"     EIGH:   {eigh_t:.2f} ms\n")
            f.write(f"     MATMUL: {mm_t:.2f} ms\n")

        f.write("\n" + "=" * 60 + "\n")

    print(f"\n报告已保存到: {output_file}")

    # 绘图
    plot_benchmark_results([ent_results, spin_results, matrix_results],
                          save_path='benchmark_plots.png')


if __name__ == "__main__":
    generate_benchmark_report()
