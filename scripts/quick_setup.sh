#!/bin/bash
# 快速设置脚本 - 自动配置研究环境

echo "========================================================================"
echo "张量网络研究框架 - 快速设置"
echo "========================================================================"
echo

# 检查Python版本
echo "[1/5] 检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python版本: $python_version"

required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "  ✓ Python版本满足要求 (>= 3.8)"
else
    echo "  ✗ Python版本过低 (需要 >= 3.8)"
    exit 1
fi

# 创建虚拟环境（可选）
echo
echo "[2/5] 创建虚拟环境 (可选)..."
read -p "是否创建Python虚拟环境? (y/n): " create_venv

if [ "$create_venv" = "y" ] || [ "$create_venv" = "Y" ]; then
    python3 -m venv venv
    source venv/bin/activate
    echo "  ✓ 虚拟环境已创建并激活"
else
    echo "  跳过虚拟环境创建"
fi

# 安装依赖
echo
echo "[3/5] 安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "  ✓ 依赖安装成功"
else
    echo "  ✗ 依赖安装失败"
    exit 1
fi

# 运行测试
echo
echo "[4/5] 运行测试套件..."
python3 tests/test_all.py

if [ $? -eq 0 ]; then
    echo "  ✓ 测试通过"
else
    echo "  ⚠ 部分测试失败（可能由于缺少TeNPy/ITensor）"
fi

# 检查项目状态
echo
echo "[5/5] 检查项目状态..."
python3 scripts/check_project_status.py

echo
echo "========================================================================"
echo "✓ 设置完成！"
echo "========================================================================"
echo
echo "下一步:"
echo "  1. 阅读 QUICKSTART.md 获取15分钟快速入门"
echo "  2. 阅读 RESEARCH_WORKFLOW.md 了解研究流程"
echo "  3. 探索 examples/ 目录中的示例"
echo "  4. 运行 Jupyter notebooks 学习理论"
echo
echo "常用命令:"
echo "  - 运行所有测试: python tests/test_all.py"
echo "  - 运行示例: python scripts/run_all_examples.py"
echo "  - 生成图表: python scripts/generate_publication_figures.py"
echo "  - 检查状态: python scripts/check_project_status.py"
echo
echo "祝研究顺利！ 🚀"
