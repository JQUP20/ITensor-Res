# 快速入门指南

欢迎开始张量网络研究之旅！本指南将帮助你在15分钟内设置环境并运行第一个示例。

## 🚀 三步开始

### 步骤1: 克隆并设置环境 (5分钟)

```bash
# 克隆仓库 (如果还没有)
git clone https://github.com/your-username/ITensor-Res.git
cd ITensor-Res

# 创建Python虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装Python依赖
pip install --upgrade pip
pip install -r requirements.txt
```

**验证安装:**

```bash
python -c "import tenpy; print('TeNPy version:', tenpy.__version__)"
```

如果看到版本号,说明安装成功! ✓

### 步骤2: 运行第一个MPS示例 (5分钟)

```bash
cd project1_MPS_basics/src
python mps_ising.py --L 30 --h 0.5 --chi 32
```

这将计算横场伊辛模型的纠缠熵并生成图表。

**预期输出:**
- 计算基态能量
- 显示纠缠熵分布
- 保存图表到 `../results/figures/`

### 步骤3: 探索Jupyter Notebook (5分钟)

```bash
cd ../notebooks
jupyter notebook 01_MPS_introduction.ipynb
```

按照notebook中的说明逐步学习MPS基础。

## 📚 学习路径

### 第1周: MPS基础
- ✅ 运行 `mps_ising.py`
- ✅ 完成 `01_MPS_introduction.ipynb`
- ✅ 理解施密特分解
- 📝 修改参数,观察纠缠熵变化

### 第2-4周: 扩展实验
- 实现周期边界条件
- 计算关联函数
- 研究临界点标度

### 第2个月: 进入项目2
- 学习DMRG算法
- 实现Haldane链
- 计算弦序参数

## 🛠️ 常见问题

### Q1: TeNPy安装失败?

**解决方案:**
```bash
pip install --no-cache-dir tenpy
# 或者从源码安装
pip install git+https://github.com/tenpy/tenpy.git
```

### Q2: 需要C++版本吗?

**回答:** 项目1-2用Python即可。项目3+推荐使用ITensor C++以提高性能。

安装ITensor:
```bash
cd scripts
./install_itensor.sh
```

### Q3: 如何加速计算?

**建议:**
1. 使用更小的系统 (`--L 20`)
2. 降低键维度 (`--chi 16`)
3. 使用GPU (安装JAX GPU版本)

### Q4: 图表不显示?

**解决方案:**
```python
import matplotlib
matplotlib.use('TkAgg')  # 或 'Qt5Agg'
```

## 📊 示例输出

运行项目1后,你应该看到:

```
==========================================
MPS基础: 横场伊辛模型纠缠熵计算
==========================================

使用TeNPy DMRG (L=30, J=1.0, h=0.5, χ=32)
DMRG收敛，能量: -28.3456789012

图表已保存: ../results/figures/entanglement.png

计算完成！
```

## 🎯 下一步

### 立即行动:
1. ⭐ Star 本仓库
2. 📖 阅读 [主README](README.md) 了解完整项目
3. 💬 加入讨论组分享进展

### 推荐资源:
- **TeNPy教程**: https://tenpy.readthedocs.io/
- **Orus综述**: arXiv:1306.2164
- **Schollwöck DMRG**: arXiv:1008.3477

## 🤝 获取帮助

遇到问题?

1. 检查 [主README](README.md) 的参考资料部分
2. 查看各项目文件夹的 `README.md`
3. 提交 [Issue](https://github.com/your-username/ITensor-Res/issues)

## 🎓 研究建议

### 第1个月目标
- [ ] 完成项目1所有任务
- [ ] 理解MPS为什么高效
- [ ] 能独立修改代码
- [ ] 组内演讲介绍MPS

### 衡量进度
- **初级**: 能运行示例代码
- **中级**: 能修改参数并解释结果
- **高级**: 能实现新功能 (如周期边界)
- **专家**: 能优化算法性能

---

**准备好了吗? 开始你的第一个计算!** 🚀

```bash
cd project1_MPS_basics/src
python mps_ising.py --L 20 --h 1.0 --chi 32  # 临界点!
```

观察纠缠熵的对数发散,这是量子临界性的标志！

**祝研究顺利!** 💪
