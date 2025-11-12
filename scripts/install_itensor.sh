#!/bin/bash
# ITensor C++库安装脚本

set -e

echo "=========================================="
echo "ITensor C++ 安装脚本"
echo "=========================================="

# 检测操作系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
else
    echo "不支持的操作系统: $OSTYPE"
    exit 1
fi

# 安装路径
INSTALL_DIR="$HOME/local/itensor"
ITENSOR_VERSION="v3.1.10"

echo "安装目录: $INSTALL_DIR"
echo "ITensor版本: $ITENSOR_VERSION"

# 创建目录
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# 克隆ITensor
if [ ! -d "ITensor" ]; then
    echo "克隆ITensor仓库..."
    git clone https://github.com/ITensor/ITensor.git
    cd ITensor
    git checkout $ITENSOR_VERSION
else
    echo "ITensor已存在，更新..."
    cd ITensor
    git pull
fi

# 创建配置文件
echo "创建options.mk..."
cat > options.mk << EOF
# ITensor编译配置

# 编译器
CCCOM=g++ -std=c++17

# BLAS/LAPACK
PLATFORM=$OS
BLAS_LAPACK_LIBFLAGS=-lblas -llapack

# 优化选项
OPTIMIZATIONS=-O2 -DNDEBUG

# 调试选项 (可选)
# OPTIMIZATIONS=-g -DDEBUG

# 并行 (可选)
# OPTIMIZATIONS+=-fopenmp
EOF

# 编译
echo "开始编译ITensor..."
make -j4

# 添加到环境变量
echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "请将以下内容添加到 ~/.bashrc 或 ~/.zshrc:"
echo ""
echo "export ITENSOR_DIR=$INSTALL_DIR/ITensor"
echo "export LIBRARY_PATH=\$ITENSOR_DIR/lib:\$LIBRARY_PATH"
echo "export LD_LIBRARY_PATH=\$ITENSOR_DIR/lib:\$LD_LIBRARY_PATH"
echo "export CPLUS_INCLUDE_PATH=\$ITENSOR_DIR:\$CPLUS_INCLUDE_PATH"
echo ""
echo "然后运行: source ~/.bashrc"
echo ""

# 测试编译
echo "测试ITensor..."
cd tutorial/01_one_site
make
./one_site

echo ""
echo "✓ ITensor安装成功！"
