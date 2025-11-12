#!/usr/bin/env python3
"""
GPU加速工具

使用JAX或CuPy加速张量运算
"""

import numpy as np
from typing import Optional, Tuple
import warnings

# 尝试导入JAX
try:
    import jax
    import jax.numpy as jnp
    from jax import jit, grad, vmap
    JAX_AVAILABLE = True
except ImportError:
    JAX_AVAILABLE = False
    warnings.warn("JAX未安装，GPU加速不可用")

# 尝试导入CuPy
try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False


class GPUTensorOps:
    """
    GPU张量操作类
    """

    def __init__(self, backend: str = 'jax'):
        """
        初始化

        参数:
            backend: 后端选择 ('jax' or 'cupy')
        """
        self.backend = backend

        if backend == 'jax' and not JAX_AVAILABLE:
            raise ImportError("JAX未安装")
        elif backend == 'cupy' and not CUPY_AVAILABLE:
            raise ImportError("CuPy未安装")

        print(f"GPU加速后端: {backend}")

    def to_device(self, array: np.ndarray):
        """将数组转移到GPU"""
        if self.backend == 'jax':
            return jnp.array(array)
        elif self.backend == 'cupy':
            return cp.array(array)
        return array

    def to_numpy(self, array):
        """将数组转换回NumPy"""
        if self.backend == 'jax':
            return np.array(array)
        elif self.backend == 'cupy':
            return cp.asnumpy(array)
        return array

    def svd(self, matrix):
        """GPU加速SVD"""
        if self.backend == 'jax':
            return jnp.linalg.svd(matrix, full_matrices=False)
        elif self.backend == 'cupy':
            return cp.linalg.svd(matrix, full_matrices=False)
        return np.linalg.svd(matrix, full_matrices=False)

    def eigh(self, matrix):
        """GPU加速厄米矩阵对角化"""
        if self.backend == 'jax':
            return jnp.linalg.eigh(matrix)
        elif self.backend == 'cupy':
            return cp.linalg.eigh(matrix)
        return np.linalg.eigh(matrix)

    def tensor_contract(self, A, B, axes):
        """GPU加速张量收缩"""
        if self.backend == 'jax':
            return jnp.tensordot(A, B, axes=axes)
        elif self.backend == 'cupy':
            return cp.tensordot(A, B, axes=axes)
        return np.tensordot(A, B, axes=axes)


if JAX_AVAILABLE:
    @jit
    def entanglement_entropy_jax(schmidt_values):
        """
        JAX加速纠缠熵计算

        参数:
            schmidt_values: 施密特值（JAX数组）

        返回:
            纠缠熵
        """
        sv_normalized = schmidt_values / jnp.linalg.norm(schmidt_values)
        p = sv_normalized**2
        # 过滤小值
        p_filtered = jnp.where(p > 1e-14, p, 0)
        # 计算熵（避免log(0)）
        entropy = -jnp.sum(jnp.where(p_filtered > 0,
                                    p_filtered * jnp.log(p_filtered),
                                    0))
        return entropy

    @jit
    def mps_contraction_jax(A, B):
        """
        JAX加速MPS张量收缩

        参数:
            A, B: MPS张量

        返回:
            收缩结果
        """
        return jnp.tensordot(A, B, axes=([1], [0]))


def benchmark_gpu_vs_cpu(size: int = 1000, n_trials: int = 10):
    """
    GPU vs CPU性能对比

    参数:
        size: 矩阵大小
        n_trials: 测试次数
    """
    import time

    print(f"\nGPU vs CPU性能测试 (矩阵大小: {size}×{size})")
    print("=" * 60)

    # 生成随机矩阵
    A_np = np.random.randn(size, size)

    # CPU测试
    cpu_times = []
    for _ in range(n_trials):
        start = time.time()
        U, S, Vt = np.linalg.svd(A_np, full_matrices=False)
        cpu_times.append(time.time() - start)

    cpu_time = np.mean(cpu_times)
    print(f"CPU (NumPy): {cpu_time:.4f} 秒")

    # JAX GPU测试
    if JAX_AVAILABLE:
        A_jax = jnp.array(A_np)

        # Warm-up
        _ = jnp.linalg.svd(A_jax, full_matrices=False)

        jax_times = []
        for _ in range(n_trials):
            start = time.time()
            U, S, Vt = jnp.linalg.svd(A_jax, full_matrices=False)
            # 等待计算完成
            S.block_until_ready()
            jax_times.append(time.time() - start)

        jax_time = np.mean(jax_times)
        print(f"GPU (JAX): {jax_time:.4f} 秒")
        print(f"加速比: {cpu_time / jax_time:.2f}x")

    # CuPy测试
    if CUPY_AVAILABLE:
        A_cupy = cp.array(A_np)

        cupy_times = []
        for _ in range(n_trials):
            start = time.time()
            U, S, Vt = cp.linalg.svd(A_cupy, full_matrices=False)
            cp.cuda.Stream.null.synchronize()
            cupy_times.append(time.time() - start)

        cupy_time = np.mean(cupy_times)
        print(f"GPU (CuPy): {cupy_time:.4f} 秒")
        print(f"加速比: {cpu_time / cupy_time:.2f}x")

    print("=" * 60)


def optimize_mps_with_jax(n_sites: int = 10, chi: int = 16, n_steps: int = 100):
    """
    使用JAX自动微分优化MPS

    参数:
        n_sites: 格点数
        chi: 键维度
        n_steps: 优化步数
    """
    if not JAX_AVAILABLE:
        print("需要安装JAX才能运行此示例")
        return

    print(f"\n使用JAX优化MPS (L={n_sites}, χ={chi})")
    print("=" * 60)

    # 初始化MPS张量（简化）
    def init_mps(key, n_sites, chi, d=2):
        """初始化随机MPS"""
        keys = jax.random.split(key, n_sites)
        tensors = []
        for i in range(n_sites):
            chi_l = 1 if i == 0 else chi
            chi_r = 1 if i == n_sites - 1 else chi
            tensor = jax.random.normal(keys[i], (chi_l, chi_r, d))
            tensors.append(tensor)
        return tensors

    # 损失函数（能量期望值）
    @jit
    def energy_loss(tensors):
        """计算能量（简化）"""
        # 这里应该是哈密顿量期望值
        # 简化为范数
        total = 0.0
        for tensor in tensors:
            total += jnp.sum(tensor**2)
        return total

    # 梯度下降
    @jit
    def update_step(tensors, lr=0.01):
        """单步更新"""
        grads = grad(energy_loss)(tensors)
        new_tensors = []
        for tensor, g in zip(tensors, grads):
            new_tensors.append(tensor - lr * g)
        return new_tensors

    # 优化循环
    key = jax.random.PRNGKey(0)
    tensors = init_mps(key, n_sites, chi)

    energies = []
    for step in range(n_steps):
        energy = energy_loss(tensors)
        energies.append(float(energy))

        if step % 20 == 0:
            print(f"Step {step}: Energy = {energy:.6f}")

        tensors = update_step(tensors)

    print(f"\n最终能量: {energies[-1]:.6f}")
    print("=" * 60)

    return energies


if __name__ == "__main__":
    print("=" * 60)
    print("GPU加速工具测试")
    print("=" * 60)

    # 性能测试
    if JAX_AVAILABLE or CUPY_AVAILABLE:
        benchmark_gpu_vs_cpu(size=2000, n_trials=5)

    # JAX优化示例
    if JAX_AVAILABLE:
        energies = optimize_mps_with_jax(n_sites=8, chi=8, n_steps=50)

    if not JAX_AVAILABLE and not CUPY_AVAILABLE:
        print("\n未安装GPU后端。")
        print("安装方法:")
        print("  JAX: pip install jax jaxlib")
        print("  CuPy: pip install cupy-cuda11x  # 根据CUDA版本选择")
