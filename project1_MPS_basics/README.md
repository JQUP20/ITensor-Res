# 项目1: MPS基础构建与纠缠标度律

## 目标

掌握矩阵乘积态(MPS)表示方法，通过数值实验验证**纠缠面积律**。

## 研究系统

**一维横场伊辛模型** (Transverse Field Ising Model, TFIM)

```
H = -J Σᵢ σᵢᶻ σᵢ₊₁ᶻ - h Σᵢ σᵢˣ
```

其中:
- J: 铁磁耦合强度
- h: 横场强度
- σᶻ, σˣ: Pauli矩阵

## 物理背景

### 相图
- **h << J**: 铁磁有序相，自发对称破缺
- **h >> J**: 极化相，所有自旋沿x方向
- **hc = J**: 量子临界点，相变点

### 纠缠性质
- **有序相**: 纠缠熵饱和 (面积律)
- **临界点**: 对数发散 S ~ (c/3)log(L)

## 任务清单

### 任务1: MPS基础实现 ✓
- [ ] 理解MPS张量结构
- [ ] 实现施密特分解函数
- [ ] 构建随机MPS态
- [ ] 可视化MPS键维度

### 任务2: 横场伊辛哈密顿量 ✓
- [ ] 构建局域哈密顿量矩阵
- [ ] 实现MPO表示
- [ ] 验证哈密顿量厄米性

### 任务3: 纠缠熵计算 ✓
- [ ] 计算约化密度矩阵
- [ ] 实现冯诺依曼熵 S = -Tr(ρ ln ρ)
- [ ] 绘制纠缠熵随位置变化

### 任务4: 相变分析 ✓
- [ ] 扫描不同h/J比值
- [ ] 绘制临界点纠缠熵发散
- [ ] 拟合CFT预测 S ~ (c/6)log(L)

## 目录结构

```
project1_MPS_basics/
├── README.md                    # 本文件
├── src/
│   ├── mps_ising.py            # 主程序 (TeNPy)
│   ├── mps_ising.cpp           # C++版本 (ITensor)
│   ├── entanglement.py         # 纠缠熵计算
│   └── visualization.py        # 可视化工具
├── notebooks/
│   ├── 01_MPS_introduction.ipynb
│   ├── 02_Schmidt_decomposition.ipynb
│   └── 03_Entanglement_scaling.ipynb
├── docs/
│   ├── theory.md               # 理论背景
│   ├── numerical_methods.md   # 数值方法
│   └── results_report.md       # 结果报告模板
└── results/
    ├── figures/                # 生成的图表
    └── data/                   # 数值数据
```

## 快速开始

### 1. Python版本 (TeNPy)

```bash
cd src
python mps_ising.py --L 50 --J 1.0 --h 0.5 --chi 32
```

参数说明:
- `--L`: 系统大小 (格点数)
- `--J`: 耦合强度
- `--h`: 横场强度
- `--chi`: 键维度 (bond dimension)

### 2. C++版本 (ITensor)

```bash
cd src
g++ -std=c++17 mps_ising.cpp -o mps_ising -litensor
./mps_ising
```

### 3. Jupyter Notebook

```bash
cd notebooks
jupyter notebook 01_MPS_introduction.ipynb
```

## 关键概念

### 矩阵乘积态 (MPS)

一维量子态可以表示为:

```
|ψ⟩ = Σ A[1]^{s₁} A[2]^{s₂} ... A[L]^{sₗ} |s₁s₂...sₗ⟩
```

其中 A[i]^{sᵢ} 是 χᵢ₋₁ × χᵢ 矩阵，sᵢ 是物理指标。

### 施密特分解

将系统分为两部分 A 和 B:

```
|ψ⟩ = Σₐ λₐ |φₐ⟩_A ⊗ |ϕₐ⟩_B
```

施密特值 λₐ 满足 Σₐ λₐ² = 1

### 冯诺依曼纠缠熵

```
S = -Tr(ρ_A ln ρ_A) = -Σₐ λₐ² ln(λₐ²)
```

## 预期结果

### 图1: MPS结构示意图
```
[χ₀=1] -- A¹ -- [χ₁] -- A² -- [χ₂] -- ... -- Aᴸ -- [χₗ=1]
           |             |                     |
          s₁            s₂                    sₗ
```

### 图2: 纠缠熵随位置变化
- x轴: 键位置 i
- y轴: 纠缠熵 S(i)
- 不同曲线: 不同 h/J 比值

### 图3: 临界点标度行为
- x轴: log(L)
- y轴: S_max
- 斜率: c/6 ≈ 1/12 (伊辛CFT)

## 理论基础

### 面积律 (Area Law)

对于基态，纠缠熵满足:

```
S(L) ~ L^{d-1}  (d维系统)
```

一维系统 (d=1): S ~ 常数

### 临界点对数发散

在量子临界点:

```
S(l) = (c/6) log(l) + const
```

其中 c 是中心电荷 (伊辛模型: c=1/2)

## 物理量计算

### 1. 磁化强度

```python
M = ⟨σᶻ⟩ = (1/L) Σᵢ ⟨σᵢᶻ⟩
```

### 2. 关联函数

```python
C(r) = ⟨σ₀ᶻ σᵣᶻ⟩ - ⟨σ₀ᶻ⟩⟨σᵣᶻ⟩
```

### 3. 保真度感受率

```python
χ_F = -∂²F/∂h²
```

其中 F = -log|⟨ψ(h)|ψ(h+δh)⟩| 是保真度。

## 数值技巧

### 键维度选择
- 远离临界点: χ = 16-32 足够
- 临界点附近: χ = 64-128
- 精确计算: 监控截断误差

### 收敛判据
```python
ε = 1 - Σₐ λₐ² < 10⁻¹⁰
```

### 性能优化
- 使用对称性 (Z₂)
- SVD数值稳定性
- 避免全对角化

## 参考资料

### 核心论文
1. **Vidal (2003)** - *Phys. Rev. Lett. 91, 147902*
   "Efficient Classical Simulation of Slightly Entangled Quantum Computations"

2. **Schollwöck (2011)** - *Ann. Phys. 326, 96*
   "The density-matrix renormalization group in the age of matrix product states"

3. **Orús (2014)** - *Ann. Phys. 349, 117*
   "A practical introduction to tensor networks"

### 教程
- TeNPy官方教程: https://tenpy.readthedocs.io/
- ITensor入门: https://itensor.org/docs.cgi?vers=cppv3

## 练习题

1. **推导**: 证明开放边界MPS的施密特秩最多为χ。

2. **编程**: 实现周期边界条件的MPS。

3. **分析**: 为什么临界点需要更大的键维度？

4. **扩展**: 计算Rényi熵 Sₙ = 1/(1-n) log(Tr ρⁿ)

## 成果检查清单

- [ ] 代码通过单元测试
- [ ] 生成所有结果图表
- [ ] 完成结果报告 (见 `docs/results_report.md`)
- [ ] 组内演讲准备 (15分钟)
- [ ] 代码文档完整

## 下一步

完成本项目后，你应该:
1. 理解MPS为什么高效
2. 掌握纠缠熵计算方法
3. 能解释面积律的物理意义
4. 准备好进入 **项目2: DMRG**

---

**预计完成时间**: 1-2个月
**难度**: ⭐⭐☆☆☆
**必备知识**: 量子力学、线性代数、Python基础
