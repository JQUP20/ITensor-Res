#!/usr/bin/env python3
"""
自动运行所有示例脚本

用于快速验证所有项目的功能
"""

import subprocess
import sys
from pathlib import Path
import time

project_root = Path(__file__).parent.parent

# 所有可执行示例
EXAMPLES = {
    "Project 1 - MPS Basics": [
        "project1_MPS_basics/src/entanglement.py",
    ],
    "Project 2 - DMRG Haldane": [
        "project2_DMRG_Haldane/src/edge_state_analysis.py",
    ],
    "Project 3 - PEPS Kitaev": [
        "project3_PEPS_Kitaev/src/ctmrg.py",
        "project3_PEPS_Kitaev/src/topological_entropy.py",
    ],
    "Project 4 - MERA CFT": [
        "project4_MERA_CFT/src/mera_optimization.py",
        "project4_MERA_CFT/src/cft_analysis.py",
    ],
    "Project 5 - String-Net": [
        "project5_String-Net/src/levin_wen_model.py",
        "project5_String-Net/src/f_symbol_verification.py",
    ],
    "Project 6 - Categorical Symmetry": [
        "project6_Categorical_Symmetry/src/categorical_symmetry.py",
    ],
}


def run_example(script_path: Path, timeout: int = 60) -> bool:
    """
    运行单个示例脚本

    参数:
        script_path: 脚本路径
        timeout: 超时时间（秒）

    返回:
        是否成功
    """
    print(f"  运行: {script_path.name}...", end=" ", flush=True)

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=script_path.parent
        )

        if result.returncode == 0:
            print("✓")
            return True
        else:
            print("✗")
            print(f"    错误输出: {result.stderr[:200]}")
            return False

    except subprocess.TimeoutExpired:
        print("⏱ (超时)")
        return False
    except Exception as e:
        print(f"✗ ({e})")
        return False


def main():
    """主函数"""
    print("="*70)
    print("运行所有示例脚本")
    print("="*70)
    print()

    total = 0
    passed = 0
    failed = 0

    for project_name, scripts in EXAMPLES.items():
        print(f"\n{project_name}")
        print("-"*70)

        for script_rel_path in scripts:
            script_path = project_root / script_rel_path

            if not script_path.exists():
                print(f"  跳过: {script_path.name} (文件不存在)")
                continue

            total += 1
            if run_example(script_path):
                passed += 1
            else:
                failed += 1

            time.sleep(0.5)  # 避免过快运行

    # 总结
    print()
    print("="*70)
    print("运行总结")
    print("="*70)
    print(f"总计: {total}")
    print(f"成功: {passed} ✓")
    print(f"失败: {failed} ✗")

    if failed == 0:
        print("\n✅ 所有示例运行成功!")
        return 0
    else:
        print(f"\n⚠️  {failed} 个示例运行失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
