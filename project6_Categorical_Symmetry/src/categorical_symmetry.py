#!/usr/bin/env python3
"""
范畴对称性实现

实现非可逆对称性和对称性缺陷
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SymmetryCategory:
    """对称性范畴"""
    objects: List[str]
    fusion_rules: Dict[Tuple[str, str], List[Tuple[str, float]]]
    quantum_dims: Dict[str, float]

    @property
    def is_invertible(self) -> bool:
        """检查是否所有对象都可逆"""
        for obj in self.objects:
            has_inverse = any(
                '1' in [c for c, _ in self.fusion_rules.get((obj, other), [])]
                for other in self.objects
            )
            if not has_inverse and obj != '1':
                return False
        return True


class FibonacciSymmetry:
    """Fibonacci对称性（非可逆）"""

    def __init__(self):
        """初始化"""
        self.phi = (1 + np.sqrt(5)) / 2
        self.category = SymmetryCategory(
            objects=['1', 'tau'],
            fusion_rules={
                ('1', '1'): [('1', 1.0)],
                ('1', 'tau'): [('tau', 1.0)],
                ('tau', '1'): [('tau', 1.0)],
                ('tau', 'tau'): [('1', 1.0), ('tau', 1.0)]
            },
            quantum_dims={'1': 1.0, 'tau': self.phi}
        )

    def print_info(self):
        """打印对称性信息"""
        print("="*60)
        print("Fibonacci非可逆对称性")
        print("="*60)
        print(f"\n对象: {self.category.objects}")
        print(f"可逆性: {self.category.is_invertible}")


def main():
    """主程序"""
    print("\n"+"="*60)
    print("范畴对称性与非可逆对称性")
    print("="*60)
    fib = FibonacciSymmetry()
    fib.print_info()


if __name__ == "__main__":
    main()
