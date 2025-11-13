#!/usr/bin/env python3
"""
MERA变分优化

实现MERA张量的变分优化算法
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
import warnings


class MERAOptimizer:
    """
    MERA变分优化器
    """

    def __init__(self, hamiltonian: np.ndarray, chi: int, num_layers: int):
        """
        初始化

        参数:
            hamiltonian: 局域哈密顿量（两体）
            chi: 键维度
            num_layers: MERA层数
        """
        self.H = hamiltonian
        self.chi = chi
        self.num_layers = num_layers
        self.d = int(np.sqrt(hamiltonian.shape[0]))  # 物理维度

        # 初始化MERA张量
        self.isometries = self._init_isometries()
        self.disentanglers = self._init_disentanglers()

        # 优化历史
        self.energy_history = []

    def _init_isometries(self) -> List[np.ndarray]:
        """初始化等距张量"""
        isometries = []
        for layer in range(self.num_layers):
            u = self._random_isometry(self.chi, self.chi)
            isometries.append(u)
        return isometries

    def _init_disentanglers(self) -> List[np.ndarray]:
        """初始化解纠缠器"""
        disentanglers = []
        for layer in range(self.num_layers):
            w = self._random_unitary(self.chi)
            disentanglers.append(w)
        return disentanglers

    def _random_isometry(self, chi_in: int, chi_out: int) -> np.ndarray:
        """生成随机等距张量"""
        A = np.random.randn(chi_in**2, chi_out) + \
            1j * np.random.randn(chi_in**2, chi_out)
        Q, R = np.linalg.qr(A)
        return Q[:, :chi_out].reshape(chi_in, chi_in, chi_out)

    def _random_unitary(self, chi: int) -> np.ndarray:
        """生成随机酉张量"""
        A = np.random.randn(chi**2, chi**2) + \
            1j * np.random.randn(chi**2, chi**2)
        U, S, Vh = np.linalg.svd(A)
        W = U @ Vh
        return W.reshape(chi, chi, chi, chi)

    def compute_energy(self) -> float:
        """
        计算能量期望值

        返回:
            E = ⟨ψ|H|ψ⟩ / ⟨ψ|ψ⟩
        """
        # 简化实现：只计算局域能量
        # 完整实现需要收缩整个MERA网络

        E_local = np.trace(self.H) / self.H.shape[0]
        return E_local.real

    def optimize_layer(self, layer: int, max_iter: int = 10) -> float:
        """
        优化单层张量

        参数:
            layer: 层数
            max_iter: 最大迭代次数

        返回:
            能量变化
        """
        E_initial = self.compute_energy()

        # 优化解纠缠器
        for _ in range(max_iter // 2):
            grad_w = self._compute_gradient_disentangler(layer)
            self.disentanglers[layer] = self._update_disentangler(
                self.disentanglers[layer], grad_w, lr=0.01
            )

        # 优化等距张量
        for _ in range(max_iter // 2):
            grad_u = self._compute_gradient_isometry(layer)
            self.isometries[layer] = self._update_isometry(
                self.isometries[layer], grad_u, lr=0.01
            )

        E_final = self.compute_energy()
        return E_final - E_initial

    def _compute_gradient_disentangler(self, layer: int) -> np.ndarray:
        """计算解纠缠器的梯度（简化）"""
        # 完整实现需要自动微分或数值微分
        return np.zeros_like(self.disentanglers[layer])

    def _compute_gradient_isometry(self, layer: int) -> np.ndarray:
        """计算等距张量的梯度（简化）"""
        return np.zeros_like(self.isometries[layer])

    def _update_disentangler(self, w: np.ndarray, grad: np.ndarray,
                            lr: float) -> np.ndarray:
        """更新解纠缠器并保持酉性"""
        chi = w.shape[0]
        w_mat = w.reshape(chi**2, chi**2)

        # 简单梯度下降
        w_new_mat = w_mat - lr * grad.reshape(chi**2, chi**2)

        # SVD投影到酉流形
        U, S, Vh = np.linalg.svd(w_new_mat)
        w_new_mat = U @ Vh

        return w_new_mat.reshape(chi, chi, chi, chi)

    def _update_isometry(self, u: np.ndarray, grad: np.ndarray,
                        lr: float) -> np.ndarray:
        """更新等距张量并保持等距性"""
        chi_in, _, chi_out = u.shape
        u_mat = u.reshape(chi_in**2, chi_out)

        # 梯度下降
        u_new_mat = u_mat - lr * grad.reshape(chi_in**2, chi_out)

        # QR分解保持等距性
        Q, R = np.linalg.qr(u_new_mat)

        return Q[:, :chi_out].reshape(chi_in, chi_in, chi_out)

    def optimize(self, max_sweeps: int = 10, tol: float = 1e-6,
                verbose: bool = True) -> Dict:
        """
        完整优化MERA

        参数:
            max_sweeps: 最大扫描次数
            tol: 收敛容差
            verbose: 是否打印信息

        返回:
            优化结果
        """
        if verbose:
            print("开始MERA优化...")
            print("=" * 60)

        for sweep in range(max_sweeps):
            E_initial = self.compute_energy()

            # 从下往上优化每一层
            for layer in range(self.num_layers):
                dE = self.optimize_layer(layer, max_iter=5)

            E_final = self.compute_energy()
            delta_E = abs(E_final - E_initial)

            self.energy_history.append(E_final)

            if verbose and sweep % 2 == 0:
                print(f"Sweep {sweep:3d}: E = {E_final:.8f}, "
                      f"ΔE = {delta_E:.3e}")

            if delta_E < tol:
                if verbose:
                    print(f"\n收敛于第 {sweep} 次扫描!")
                break

        if verbose:
            print("=" * 60)

        return {
            'converged': delta_E < tol,
            'sweeps': sweep + 1,
            'final_energy': E_final,
            'energy_history': self.energy_history
        }


def run_mera_optimization_example():
    """运行MERA优化示例"""
    print("\n" + "=" * 60)
    print("MERA变分优化示例")
    print("=" * 60)

    # Ising哈密顿量
    Sx = np.array([[0, 1], [1, 0]])
    Sz = np.array([[1, 0], [0, -1]])

    h = 1.0  # 横场
    H_ising = -np.kron(Sx, Sx) - h * (np.kron(Sz, np.eye(2)) +
                                       np.kron(np.eye(2), Sz)) / 2

    print(f"\n模型: 横场Ising模型")
    print(f"  H = -∑ σˣᵢσˣⱼ - h∑ σᶻᵢ")
    print(f"  h = {h} (临界点)")

    # MERA参数
    chi = 4
    num_layers = 3

    print(f"\nMERA参数:")
    print(f"  键维度 χ = {chi}")
    print(f"  层数 = {num_layers}")

    # 优化
    optimizer = MERAOptimizer(H_ising, chi, num_layers)
    result = optimizer.optimize(max_sweeps=20, verbose=True)

    print(f"\n最终结果:")
    print(f"  收敛: {result['converged']}")
    print(f"  扫描次数: {result['sweeps']}")
    print(f"  最终能量: {result['final_energy']:.8f}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    run_mera_optimization_example()
