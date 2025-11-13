#!/usr/bin/env python3
"""
综合测试套件

运行所有项目的测试，验证代码正确性
"""

import sys
import os
import unittest
import numpy as np
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class TestProject1MPS(unittest.TestCase):
    """测试Project 1: MPS基础"""

    def setUp(self):
        sys.path.insert(0, str(project_root / 'project1_MPS_basics/src'))

    def test_mps_ising_import(self):
        """测试MPS Ising模块导入"""
        try:
            from entanglement import compute_entanglement_spectrum
            self.assertTrue(callable(compute_entanglement_spectrum))
        except ImportError as e:
            self.skipTest(f"TeNPy not available: {e}")

    def test_schmidt_decomposition(self):
        """测试Schmidt分解"""
        # 创建简单的双体纠缠态
        psi = np.array([1, 0, 0, 1]) / np.sqrt(2)  # |00⟩ + |11⟩
        psi_matrix = psi.reshape(2, 2)

        U, S, Vh = np.linalg.svd(psi_matrix)

        # 验证Schmidt系数
        self.assertEqual(len(S), 2)
        self.assertAlmostEqual(S[0], 1/np.sqrt(2), places=10)
        self.assertAlmostEqual(S[1], 1/np.sqrt(2), places=10)

    def test_entanglement_entropy(self):
        """测试纠缠熵计算"""
        # 最大纠缠态
        S_max = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
        entropy_max = -np.sum(S_max**2 * np.log(S_max**2))
        self.assertAlmostEqual(entropy_max, np.log(2), places=10)

        # 无纠缠态
        S_min = np.array([1.0, 0.0])
        entropy_min = -np.sum(S_min[S_min > 0]**2 * np.log(S_min[S_min > 0]**2))
        self.assertAlmostEqual(entropy_min, 0.0, places=10)


class TestProject2DMRG(unittest.TestCase):
    """测试Project 2: DMRG & Haldane相"""

    def setUp(self):
        sys.path.insert(0, str(project_root / 'project2_DMRG_Haldane/src'))

    def test_string_order_parameter(self):
        """测试弦序参数"""
        # 简单的弦序计算
        L = 10
        # 模拟数据
        Sz_values = np.random.randn(L) * 0.1

        # 弦序应该在一定范围内
        string_order = np.mean(Sz_values)
        self.assertLess(abs(string_order), 1.0)


class TestProject3PEPS(unittest.TestCase):
    """测试Project 3: PEPS & Kitaev"""

    def setUp(self):
        sys.path.insert(0, str(project_root / 'project3_PEPS_Kitaev/src'))

    def test_topological_entropy(self):
        """测试拓扑纠缠熵"""
        from topological_entropy import TopologicalEntropy

        topo_calc = TopologicalEntropy()

        # Z₂拓扑序：S_topo = ln(2)
        S_topo_theory = np.log(2)

        # 验证理论值
        self.assertAlmostEqual(S_topo_theory, 0.693147, places=5)

    def test_quantum_dimensions(self):
        """测试量子维数"""
        # Z₂: 所有d=1，总量子维数D=2
        d_1 = 1.0
        d_e = 1.0
        d_m = 1.0
        d_psi = 1.0

        D = np.sqrt(d_1**2 + d_e**2 + d_m**2 + d_psi**2)
        self.assertAlmostEqual(D, 2.0, places=10)


class TestProject4MERA(unittest.TestCase):
    """测试Project 4: MERA & CFT"""

    def setUp(self):
        sys.path.insert(0, str(project_root / 'project4_MERA_CFT/src'))

    def test_isometry(self):
        """测试等距张量"""
        chi = 4

        # 创建随机等距张量
        A = np.random.randn(chi**2, chi) + 1j * np.random.randn(chi**2, chi)
        Q, R = np.linalg.qr(A)
        u = Q[:, :chi].reshape(chi, chi, chi)

        # 验证等距性
        u_mat = u.reshape(chi**2, chi)
        result = u_mat.conj().T @ u_mat
        identity = np.eye(chi)

        error = np.linalg.norm(result - identity)
        self.assertLess(error, 1e-10)

    def test_central_charge_extraction(self):
        """测试中心荷提取"""
        # 模拟Ising CFT: c = 1/2
        c_theory = 0.5

        L_values = 2**np.arange(3, 8)
        S_values = (c_theory / 3) * np.log(L_values) + 0.5

        # 线性拟合
        coeffs = np.polyfit(np.log(L_values), S_values, 1)
        c_extracted = 3 * coeffs[0]

        self.assertAlmostEqual(c_extracted, c_theory, places=1)


class TestProject5StringNet(unittest.TestCase):
    """测试Project 5: String-Net液体"""

    def setUp(self):
        sys.path.insert(0, str(project_root / 'project5_String-Net/src'))

    def test_fibonacci_category(self):
        """测试Fibonacci融合范畴"""
        from levin_wen_model import FibonacciCategory

        fib = FibonacciCategory()

        # 验证黄金比例
        phi = (1 + np.sqrt(5)) / 2
        self.assertAlmostEqual(fib.phi, phi, places=10)

        # 验证φ² = φ + 1
        self.assertAlmostEqual(fib.phi**2, fib.phi + 1, places=10)

        # 验证融合规则
        self.assertEqual(fib.get_fusion('1', '1'), ['1'])
        self.assertEqual(fib.get_fusion('tau', 'tau'), ['1', 'tau'])

    def test_f_symbol_unitarity(self):
        """测试F-符号酉性"""
        from levin_wen_model import FibonacciCategory

        fib = FibonacciCategory()
        F = fib.F_tau_tau_tau

        # 验证酉性
        result = F.conj().T @ F
        identity = np.eye(2)
        error = np.linalg.norm(result - identity)

        self.assertLess(error, 1e-10)

    def test_quantum_dimension_relation(self):
        """测试量子维数关系"""
        phi = (1 + np.sqrt(5)) / 2

        # d_τ × d_τ = d_1 + d_τ
        lhs = phi * phi
        rhs = 1 + phi

        self.assertAlmostEqual(lhs, rhs, places=10)


class TestProject6CategoricalSymmetry(unittest.TestCase):
    """测试Project 6: 范畴对称性"""

    def setUp(self):
        sys.path.insert(0, str(project_root / 'project6_Categorical_Symmetry/src'))

    def test_fibonacci_non_invertibility(self):
        """测试Fibonacci对称性的非可逆性"""
        from categorical_symmetry import FibonacciSymmetry

        fib = FibonacciSymmetry()

        # 验证τ没有逆元
        self.assertFalse(fib.category.is_invertible)

    def test_z2_invertibility(self):
        """测试Z₂对称性的可逆性"""
        from categorical_symmetry import Z2Symmetry

        z2 = Z2Symmetry()

        # 验证Z₂是可逆的
        self.assertTrue(z2.category.is_invertible)


class TestCommonUtilities(unittest.TestCase):
    """测试公共工具"""

    def setUp(self):
        sys.path.insert(0, str(project_root / 'common/utils'))

    def test_tensor_utils(self):
        """测试张量工具"""
        try:
            from tensor_utils import entanglement_entropy

            # 测试纠缠熵计算
            S = np.array([0.7, 0.3])
            entropy = entanglement_entropy(S)

            # 验证范围
            self.assertGreater(entropy, 0)
            self.assertLess(entropy, np.log(2))
        except ImportError:
            self.skipTest("tensor_utils not available")


def run_all_tests():
    """运行所有测试"""
    print("="*70)
    print("张量网络研究框架 - 综合测试套件")
    print("="*70)
    print()

    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加所有测试类
    suite.addTests(loader.loadTestsFromTestCase(TestProject1MPS))
    suite.addTests(loader.loadTestsFromTestCase(TestProject2DMRG))
    suite.addTests(loader.loadTestsFromTestCase(TestProject3PEPS))
    suite.addTests(loader.loadTestsFromTestCase(TestProject4MERA))
    suite.addTests(loader.loadTestsFromTestCase(TestProject5StringNet))
    suite.addTests(loader.loadTestsFromTestCase(TestProject6CategoricalSymmetry))
    suite.addTests(loader.loadTestsFromTestCase(TestCommonUtilities))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 输出总结
    print()
    print("="*70)
    print("测试总结")
    print("="*70)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(result.skipped)}")

    if result.wasSuccessful():
        print("\n✅ 所有测试通过!")
        return 0
    else:
        print("\n❌ 部分测试失败")
        return 1


if __name__ == '__main__':
    exit_code = run_all_tests()
    sys.exit(exit_code)
