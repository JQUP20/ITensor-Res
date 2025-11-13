#!/usr/bin/env python3
"""
测试张量工具函数
"""

import numpy as np
import sys
sys.path.append('../common')

from utils.tensor_utils import (
    entanglement_entropy,
    renyi_entropy,
    pauli_matrices,
    spin_operators,
    check_hermitian,
)


def test_pauli_matrices():
    """测试Pauli矩阵"""
    print("测试Pauli矩阵...")

    s0, sx, sy, sz = pauli_matrices()

    # 反对易关系
    assert np.allclose(sx @ sy + sy @ sx, np.zeros((2, 2))), "Pauli反对易失败"

    # [sx, sy] = 2i sz
    commutator = sx @ sy - sy @ sx
    assert np.allclose(commutator, 2j * sz), "Pauli对易子失败"

    # 平方
    assert np.allclose(sx @ sx, s0), "σx² ≠ I"

    print("✓ Pauli矩阵测试通过")


def test_spin_operators():
    """测试自旋算符"""
    print("测试自旋算符...")

    # 自旋-1/2
    Sx_half, Sy_half, Sz_half = spin_operators(S=0.5)
    assert Sx_half.shape == (2, 2), "自旋-1/2形状错误"

    # [Sx, Sy] = i Sz
    comm = Sx_half @ Sy_half - Sy_half @ Sx_half
    assert np.allclose(comm, 1j * Sz_half), "自旋对易子失败"

    # 自旋-1
    Sx_one, Sy_one, Sz_one = spin_operators(S=1.0)
    assert Sx_one.shape == (3, 3), "自旋-1形状错误"

    # S² eigenvalue
    S2 = Sx_one @ Sx_one + Sy_one @ Sy_one + Sz_one @ Sz_one
    expected_eigenvalue = 1.0 * (1.0 + 1.0)  # S(S+1)
    eigenvalues = np.linalg.eigvalsh(S2)
    assert np.allclose(eigenvalues, expected_eigenvalue), "S²本征值错误"

    print("✓ 自旋算符测试通过")


def test_entanglement_entropy():
    """测试纠缠熵"""
    print("测试纠缠熵...")

    # 最大纠缠态
    sv_max = np.array([1, 1]) / np.sqrt(2)
    S_max = entanglement_entropy(sv_max)
    expected = np.log(2)
    assert np.abs(S_max - expected) < 1e-10, f"最大纠缠熵错误: {S_max} vs {expected}"

    # 无纠缠态
    sv_zero = np.array([1, 0])
    S_zero = entanglement_entropy(sv_zero)
    assert S_zero < 1e-10, f"无纠缠态熵应为0: {S_zero}"

    # Rényi熵
    S2 = renyi_entropy(sv_max, n=2.0)
    assert S2 > 0, "Rényi熵应为正"

    print("✓ 纠缠熵测试通过")


def test_hermiticity():
    """测试厄米性检查"""
    print("测试厄米性...")

    # 厄米矩阵
    H_hermitian = np.array([[1, 1j], [-1j, 2]])
    assert check_hermitian(H_hermitian), "应识别为厄米矩阵"

    # 非厄米矩阵
    H_non_hermitian = np.array([[1, 1], [2, 2]])
    assert not check_hermitian(H_non_hermitian), "应识别为非厄米矩阵"

    print("✓ 厄米性测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("运行张量工具测试")
    print("=" * 60)

    test_pauli_matrices()
    test_spin_operators()
    test_entanglement_entropy()
    test_hermiticity()

    print("\n" + "=" * 60)
    print("✓ 所有测试通过！")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
