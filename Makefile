# Makefile for ITensor-Res Project

.PHONY: help install test clean run-all docs

# 默认目标
help:
	@echo "ITensor-Res Makefile"
	@echo ""
	@echo "可用目标:"
	@echo "  install     - 安装Python依赖"
	@echo "  test        - 运行测试"
	@echo "  clean       - 清理生成文件"
	@echo "  run-all     - 运行所有项目示例"
	@echo "  docs        - 生成文档"
	@echo ""

# 安装依赖
install:
	pip install -r requirements.txt
	@echo "✓ Python依赖安装完成"
	@echo ""
	@echo "如需安装ITensor C++，运行:"
	@echo "  cd scripts && ./install_itensor.sh"

# 运行测试
test:
	@echo "运行测试..."
	python tests/test_tensor_utils.py
	@echo "✓ 测试完成"

# 清理
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ 清理完成"

# 运行所有项目
run-all:
	@echo "运行所有项目示例..."
	@echo ""
	@echo "[1/6] 项目1: MPS基础"
	cd project1_MPS_basics/src && python mps_ising.py --L 30 --h 0.5
	@echo ""
	@echo "[2/6] 项目2: DMRG Haldane"
	cd project2_DMRG_Haldane/src && python aklt_chain.py --L 30 --chi 64
	@echo ""
	@echo "[3/6] 项目3: PEPS Kitaev"
	cd project3_PEPS_Kitaev/src && python kitaev_model.py --Lx 4 --Ly 4
	@echo ""
	@echo "[4/6] 项目4: MERA CFT"
	cd project4_MERA_CFT/src && python mera_ising.py --L 64 --layers 5
	@echo ""
	@echo "[5/6] 项目5: 弦网"
	cd project5_StringNet/src && python string_net.py --Lx 6 --Ly 6
	@echo ""
	@echo "[6/6] 项目6: 范畴对称"
	cd project6_Categorical_Symmetry/src && python categorical_symmetry.py
	@echo ""
	@echo "✓ 所有项目运行完成"

# 生成文档（可选）
docs:
	@echo "生成文档..."
	@echo "（需要sphinx，运行: pip install sphinx sphinx-rtd-theme）"
	# cd docs && make html
