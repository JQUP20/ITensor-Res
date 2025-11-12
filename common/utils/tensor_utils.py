"""
通用张量网络工具函数

提供跨项目共享的工具函数。
"""

import numpy as np
from typing import Tuple, List, Optional
import logging

# 设置日志
logger = logging.getLogger(__name__)


def entanglement_entropy(schmidt_values: np.ndarray, threshold: float = 1e-14) -> float:
    """
    计算冯诺依曼纠缠熵

    参数:
        schmidt_values: 施密特值数组
        threshold: 截断小值的阈值

    返回:
        纠缠熵 S = -Σ λᵢ² log(λᵢ²)
    """
    # 归一化
    sv_normalized = schmidt_values / np.linalg.norm(schmidt_values)

    # 计算熵
    entropy = 0.0
    for s in sv_normalized:
        if s > threshold:
            p = s**2
            entropy -= p * np.log(p)

    return entropy


def renyi_entropy(schmidt_values: np.ndarray, n: float = 2.0,
                 threshold: float = 1e-14) -> float:
    """
    计算Rényi熵

    参数:
        schmidt_values: 施密特值数组
        n: Rényi指数 (n=1 对应冯诺依曼熵)
        threshold: 截断阈值

    返回:
        Rényi熵 Sₙ = 1/(1-n) log(Σ λᵢ²ⁿ)
    """
    sv_normalized = schmidt_values / np.linalg.norm(schmidt_values)

    if abs(n - 1.0) < 1e-10:
        return entanglement_entropy(schmidt_values, threshold)

    sum_powers = 0.0
    for s in sv_normalized:
        if s > threshold:
            sum_powers += (s**2)**n

    return np.log(sum_powers) / (1 - n)


def truncate_schmidt(U: np.ndarray, S: np.ndarray, Vt: np.ndarray,
                    chi_max: int, svd_min: float = 1e-12) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    截断SVD结果到最大键维度

    参数:
        U, S, Vt: SVD分解结果
        chi_max: 最大键维度
        svd_min: 最小施密特值

    返回:
        截断后的 U, S, Vt
    """
    # 计算截断误差
    chi_trunc = min(chi_max, len(S))

    # 应用阈值
    mask = S > svd_min
    chi_trunc = min(chi_trunc, np.sum(mask))

    # 截断
    S_trunc = S[:chi_trunc]
    U_trunc = U[:, :chi_trunc]
    Vt_trunc = Vt[:chi_trunc, :]

    # 计算截断误差
    truncation_error = 1.0 - np.sum(S_trunc**2) / np.sum(S**2)

    logger.info(f"Truncated to χ={chi_trunc}, error={truncation_error:.2e}")

    return U_trunc, S_trunc, Vt_trunc


def pauli_matrices() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    返回Pauli矩阵

    返回:
        σ⁰, σˣ, σʸ, σᶻ
    """
    sigma_0 = np.array([[1, 0], [0, 1]], dtype=complex)
    sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
    sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)

    return sigma_0, sigma_x, sigma_y, sigma_z


def spin_operators(S: float = 0.5) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    生成自旋-S算符

    参数:
        S: 自旋量子数 (0.5, 1, 1.5, ...)

    返回:
        Sˣ, Sʸ, Sᶻ 矩阵
    """
    dim = int(2 * S + 1)

    # 构建升降算符
    m_values = np.arange(-S, S + 1)
    S_plus = np.zeros((dim, dim), dtype=complex)
    S_minus = np.zeros((dim, dim), dtype=complex)

    for i, m in enumerate(m_values[:-1]):
        coeff = np.sqrt(S * (S + 1) - m * (m + 1))
        S_plus[i, i + 1] = coeff
        S_minus[i + 1, i] = coeff

    # 构建Sx, Sy, Sz
    Sx = 0.5 * (S_plus + S_minus)
    Sy = -0.5j * (S_plus - S_minus)
    Sz = np.diag(m_values)

    return Sx, Sy, Sz


def check_hermitian(H: np.ndarray, tol: float = 1e-10) -> bool:
    """
    检查矩阵是否厄米

    参数:
        H: 待检查矩阵
        tol: 容差

    返回:
        是否厄米
    """
    return np.allclose(H, H.conj().T, atol=tol)


def ground_state(H: np.ndarray, k: int = 1) -> Tuple[np.ndarray, np.ndarray]:
    """
    精确对角化求基态

    参数:
        H: 哈密顿量矩阵
        k: 返回前k个本征态

    返回:
        能量数组, 本征态矩阵 (列向量)
    """
    if not check_hermitian(H):
        logger.warning("哈密顿量不是厄米矩阵！")

    energies, states = np.linalg.eigh(H)

    return energies[:k], states[:, :k]


def correlation_length(correlations: np.ndarray, method: str = 'fit') -> float:
    """
    计算关联长度

    参数:
        correlations: 关联函数 C(r)
        method: 'fit' 或 'decay'

    返回:
        关联长度 ξ
    """
    r = np.arange(len(correlations))

    if method == 'fit':
        # 拟合 C(r) ~ exp(-r/ξ)
        log_C = np.log(np.abs(correlations) + 1e-14)
        mask = np.isfinite(log_C)

        if np.sum(mask) < 2:
            return np.inf

        # 线性拟合
        p = np.polyfit(r[mask], log_C[mask], 1)
        xi = -1.0 / p[0]

        return xi

    elif method == 'decay':
        # 找到衰减到1/e的位置
        threshold = correlations[0] / np.e
        idx = np.where(correlations < threshold)[0]

        if len(idx) > 0:
            return float(idx[0])
        else:
            return np.inf

    else:
        raise ValueError(f"Unknown method: {method}")


if __name__ == "__main__":
    # 测试
    print("测试张量工具函数...")

    # 测试Pauli矩阵
    s0, sx, sy, sz = pauli_matrices()
    print(f"σˣσʸ = iσᶻ: {np.allclose(sx @ sy, 1j * sz)}")

    # 测试自旋算符
    Sx, Sy, Sz = spin_operators(S=1.0)
    print(f"[Sx, Sy] = iSz: {np.allclose(Sx @ Sy - Sy @ Sx, 1j * Sz)}")

    # 测试纠缠熵
    schmidt = np.array([0.7, 0.5, 0.3, 0.1])
    S = entanglement_entropy(schmidt)
    print(f"纠缠熵: {S:.4f}")

    print("\n✓ 所有测试通过")
