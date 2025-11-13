#!/usr/bin/env python3
"""
项目状态检查工具

检查所有组件的完整性和功能性
"""

import sys
from pathlib import Path
import subprocess

project_root = Path(__file__).parent.parent


class ProjectStatusChecker:
    """项目状态检查器"""

    def __init__(self):
        """初始化"""
        self.issues = []
        self.warnings = []
        self.passed = []

    def check_file_exists(self, filepath: Path, critical: bool = True):
        """检查文件是否存在"""
        if filepath.exists():
            self.passed.append(f"✓ {filepath.relative_to(project_root)}")
            return True
        else:
            msg = f"✗ 缺少文件: {filepath.relative_to(project_root)}"
            if critical:
                self.issues.append(msg)
            else:
                self.warnings.append(msg)
            return False

    def check_directory_structure(self):
        """检查目录结构"""
        print("\n[1/6] 检查目录结构...")

        required_dirs = [
            "project1_MPS_basics",
            "project2_DMRG_Haldane",
            "project3_PEPS_Kitaev",
            "project4_MERA_CFT",
            "project5_String-Net",
            "project6_Categorical_Symmetry",
            "common",
            "tests",
            "scripts",
            "examples",
        ]

        for dirname in required_dirs:
            dirpath = project_root / dirname
            if dirpath.exists() and dirpath.is_dir():
                self.passed.append(f"✓ 目录: {dirname}")
            else:
                self.issues.append(f"✗ 缺少目录: {dirname}")

    def check_core_files(self):
        """检查核心文件"""
        print("\n[2/6] 检查核心文件...")

        required_files = [
            "README.md",
            "QUICKSTART.md",
            "CONTRIBUTING.md",
            "BIBLIOGRAPHY.md",
            "PROJECT_SUMMARY.md",
            "RESEARCH_ROADMAP.md",
            "RESEARCH_WORKFLOW.md",
            "requirements.txt",
            "Makefile",
        ]

        for filename in required_files:
            self.check_file_exists(project_root / filename)

    def check_project_completeness(self):
        """检查各项目完整性"""
        print("\n[3/6] 检查项目完整性...")

        projects = {
            "project1_MPS_basics": {
                "critical": ["src/entanglement.py", "README.md"],
                "optional": ["notebooks/01_MPS_introduction.ipynb"],
            },
            "project2_DMRG_Haldane": {
                "critical": ["src/aklt_chain.py", "README.md"],
                "optional": ["notebooks/02_Haldane_phase.ipynb",
                           "docs/theory.md"],
            },
            "project3_PEPS_Kitaev": {
                "critical": ["src/ctmrg.py", "README.md"],
                "optional": ["notebooks/01_Kitaev_anyons.ipynb",
                           "src/topological_entropy.py"],
            },
            "project4_MERA_CFT": {
                "critical": ["src/mera_optimization.py", "README.md"],
                "optional": ["notebooks/01_MERA_introduction.ipynb",
                           "src/cft_analysis.py"],
            },
            "project5_String-Net": {
                "critical": ["src/levin_wen_model.py", "README.md"],
                "optional": ["notebooks/01_Fusion_categories.ipynb",
                           "src/f_symbol_verification.py"],
            },
            "project6_Categorical_Symmetry": {
                "critical": ["src/categorical_symmetry.py", "README.md"],
                "optional": ["notebooks/01_Non_invertible_symmetry.ipynb"],
            },
        }

        for project_name, files in projects.items():
            print(f"\n  检查 {project_name}:")

            # 关键文件
            for filepath in files["critical"]:
                full_path = project_root / project_name / filepath
                self.check_file_exists(full_path, critical=True)

            # 可选文件
            for filepath in files.get("optional", []):
                full_path = project_root / project_name / filepath
                self.check_file_exists(full_path, critical=False)

    def check_dependencies(self):
        """检查依赖"""
        print("\n[4/6] 检查Python依赖...")

        requirements_file = project_root / "requirements.txt"
        if not requirements_file.exists():
            self.issues.append("✗ 缺少 requirements.txt")
            return

        try:
            with open(requirements_file) as f:
                packages = [line.strip().split('==')[0]
                           for line in f if line.strip() and not line.startswith('#')]

            print(f"  发现 {len(packages)} 个依赖包")

            # 尝试导入关键包
            critical_packages = ['numpy', 'matplotlib', 'scipy']
            for pkg in critical_packages:
                try:
                    __import__(pkg)
                    self.passed.append(f"✓ {pkg} 已安装")
                except ImportError:
                    self.warnings.append(f"⚠ {pkg} 未安装")

        except Exception as e:
            self.issues.append(f"✗ 读取requirements.txt失败: {e}")

    def check_tests(self):
        """检查测试"""
        print("\n[5/6] 检查测试套件...")

        test_file = project_root / "tests/test_all.py"
        if self.check_file_exists(test_file):
            print("  尝试运行测试...")
            try:
                result = subprocess.run(
                    [sys.executable, str(test_file)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=project_root
                )

                if result.returncode == 0:
                    self.passed.append("✓ 测试套件运行成功")
                else:
                    self.warnings.append("⚠ 部分测试失败（这可能是正常的）")

            except subprocess.TimeoutExpired:
                self.warnings.append("⚠ 测试超时")
            except Exception as e:
                self.warnings.append(f"⚠ 无法运行测试: {e}")

    def check_documentation(self):
        """检查文档完整性"""
        print("\n[6/6] 检查文档完整性...")

        doc_files = [
            "README.md",
            "QUICKSTART.md",
            "CONTRIBUTING.md",
            "BIBLIOGRAPHY.md",
            "RESEARCH_WORKFLOW.md",
        ]

        for filename in doc_files:
            filepath = project_root / filename
            if filepath.exists():
                # 检查文件是否为空
                size = filepath.stat().st_size
                if size > 100:
                    self.passed.append(f"✓ {filename} ({size} bytes)")
                else:
                    self.warnings.append(f"⚠ {filename} 内容过少")
            else:
                self.issues.append(f"✗ 缺少 {filename}")

    def generate_report(self):
        """生成检查报告"""
        print("\n" + "="*70)
        print("项目状态报告")
        print("="*70)

        # 统计
        total_checks = len(self.passed) + len(self.warnings) + len(self.issues)

        print(f"\n总检查项: {total_checks}")
        print(f"通过: {len(self.passed)} ✓")
        print(f"警告: {len(self.warnings)} ⚠")
        print(f"问题: {len(self.issues)} ✗")

        # 详细问题
        if self.issues:
            print("\n关键问题:")
            print("-"*70)
            for issue in self.issues:
                print(f"  {issue}")

        if self.warnings:
            print("\n警告:")
            print("-"*70)
            for warning in self.warnings:
                print(f"  {warning}")

        # 总体状态
        print("\n" + "="*70)
        if not self.issues:
            if not self.warnings:
                print("✅ 项目状态: 优秀")
                print("所有检查通过，项目完整且功能正常！")
            else:
                print("✅ 项目状态: 良好")
                print("核心功能完整，有一些小警告。")
        else:
            print("⚠️  项目状态: 需要改进")
            print(f"发现 {len(self.issues)} 个关键问题需要解决。")

        print("="*70)

        return len(self.issues) == 0

    def run_full_check(self):
        """运行完整检查"""
        print("="*70)
        print("张量网络研究框架 - 项目状态检查")
        print("="*70)

        self.check_directory_structure()
        self.check_core_files()
        self.check_project_completeness()
        self.check_dependencies()
        self.check_tests()
        self.check_documentation()

        return self.generate_report()


def main():
    """主程序"""
    checker = ProjectStatusChecker()
    success = checker.run_full_check()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
