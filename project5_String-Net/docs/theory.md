# String-Net液体与Levin-Wen模型理论

## String-Net简介

### 什么是String-Net?

**String-Net凝聚态**是一类拓扑有序态，由Levin和Wen于2005年提出，用于统一描述多种拓扑相。

核心思想：
- 基态由"弦网"(string-net)的量子叠加构成
- 弦带有"标签"（对应融合范畴中的对象）
- 满足特定的融合规则

## Levin-Wen模型

### 哈密顿量

定义在蜂窝格或其他二维格子上：

$$
H = -\sum_v Q_v - \sum_p B_p
$$

其中：
- $Q_v$: 顶点算符
- $B_p$: 格点(plaquette)算符

### 输入数据：融合范畴

String-Net模型由**幺半融合范畴**(unitary fusion category)完全确定：

1. **对象** (Objects): {a, b, c, ...}
2. **融合规则** (Fusion rules): $a \times b = \sum_c N_{ab}^c c$
3. **F-符号** (F-symbols): $F_{abc}^{def}$ - 结合性约束
4. **量子维数** (Quantum dimensions): $d_a$

### Fibonacci String-Net

最简单的非阿贝尔例子：

**对象**: {1, τ}

**融合规则**:
$$
\begin{align}
1 \times 1 &= 1 \\
1 \times τ &= τ \\
τ \times τ &= 1 + τ
\end{align}
$$

**量子维数**:
$$
d_1 = 1, \quad d_τ = φ = \frac{1 + \sqrt{5}}{2}
$$

**总量子维数**:
$$
\mathcal{D} = \sqrt{d_1^2 + d_τ^2} = \sqrt{1 + φ^2} = φ\sqrt{2}
$$

## 顶点算符

### 定义

在每个顶点v，$Q_v$强制融合规则：

```
    a
     \
      v---c
     /
    b
```

只有满足 $c \in a \times b$ 的配置被保留。

### 作用

- 投影到满足融合规则的弦网
- 创建局域守恒量

## Plaquette算符

### 定义

在每个六边形plaquette上：

$$
B_p = \sum_{\{s_i\}} \text{Tr}[F \cdot F \cdot F \cdot ...]
$$

使用F-符号在不同基之间变换。

### 物理意义

- 产生弦环涨落
- 对应拓扑激发（anyons）

## 拓扑激发

### 准粒子

String-Net的激发对应融合范畴的对象：

对于Fibonacci理论：
- **真空**: 1
- **非阿贝尔任意子**: τ

### 编织统计

**Fibonacci anyons**:
- 融合: $τ \times τ = 1 + τ$
- 编织相位: 非阿贝尔！
- 量子维数: $d_τ = φ$

### 应用

**拓扑量子计算**:
- Fibonacci任意子是通用的
- 编织操作实现量子门
- 拓扑保护

## F-符号

### 结合性

不同结合方式的变换：

$$
\sum_x F_{abc}^{def} |a,b,c;x⟩ = |a,b,c;y⟩
$$

### 五边形方程 (Pentagon Equation)

F-符号必须满足：

$$
\sum_n F_{abe}^{cdn} F_{cdf}^{emn} = \sum_p F_{bcd}^{fep} F_{apc}^{emf}
$$

这保证了结合性的一致性。

### Fibonacci F-符号

$$
F_{\tau\tau\tau}^{\tau\tau\tau} = \begin{pmatrix}
φ^{-1} & φ^{-1/2} \\
φ^{-1/2} & -φ^{-1}
\end{pmatrix}
$$

其中 $φ = (1+\sqrt{5})/2$ (黄金比例)

## 与其他模型的关系

### Toric Code

**Z₂ String-Net**:
- 对象: {1, e}
- 融合: $e \times e = 1$
- 等价于Toric Code

### 量子双模型 (Quantum Double)

**D(G) String-Net**:
- 群G的量子双模型
- 融合范畴: Rep(D(G))
- 包含所有群规范理论

### Kitaev模型

某些参数下：
- Kitaev蜂窝 ≈ Z₂ String-Net
- 都有相同的拓扑序

## 数值实现

### 基态波函数

$$
|ψ⟩ = \sum_{\{弦网配置\}} \text{权重} |配置⟩
$$

权重由F-符号和量子维数决定。

### 计算挑战

1. **组合爆炸**: 弦网配置数指数增长
2. **F-符号复杂**: 高阶张量
3. **收缩困难**: NP-hard

### 解决方案

- **PEPS表示**: 用PEPS表示String-Net态
- **MPS方法**: 对柱形几何
- **Monte Carlo**: 经典采样（符号问题）

## 拓扑不变量

### 拓扑纠缠熵

$$
S_{\text{topo}} = \ln \mathcal{D}
$$

对于Fibonacci:
$$
S_{\text{topo}} = \ln(φ\sqrt{2}) \approx 1.046
$$

### 基态简并

在环面上：
$$
\text{GSD} = \text{number of anyons}
$$

对Fibonacci: GSD = 2 (on torus)

## 范畴理论基础

### 幺半融合范畴 (UFC)

**公理**:
1. **结合性**: $(a \times b) \times c \cong a \times (b \times c)$
2. **单位元**: $1 \times a = a \times 1 = a$
3. **幺半性**: $⟨a|b⟩ = δ_{ab} d_a$

### 图形演算 (Graphical Calculus)

用图形表示张量网络：
- **线**: 对象/态
- **顶点**: 态射/算符
- **融合**: Y形顶点
- **F-移动**: 重新括号

### 模张量范畴 (MTC)

**额外要求**:
- **辫子化** (Braiding): 交换算符R
- **可模性** (Modularity): S矩阵可逆

Fibonacci理论是MTC！

## 实验相关性

### 候选系统

1. **拓扑序材料**:
   - 分数量子霍尔态
   - 某些自旋液体

2. **人工系统**:
   - 超导量子比特阵列
   - 冷原子格子

### 探测方法

- **拓扑纠缠熵测量**
- **编织实验**
- **干涉测量**

## 高级主题

### 1. 非幺半范畴

推广到非幺半情况：
- **超范畴** (Superfusion categories)
- **费米子对称性**

### 2. 对称破缺

String-Net + 全局对称性：
- **对称富集拓扑序** (SET)
- **分数化对称性**

### 3. 三维推广

**Walker-Wang模型**:
- 3D版本的String-Net
- 拓扑序分类

### 4. 边界理论

String-Net边缘：
- **Chiral CFT**
- **Anyonic边缘态**

## 计算技术

### F-符号求解

**输入**: 融合规则 $N_{ab}^c$

**输出**: F-符号满足五边形方程

**方法**:
- 数值求解非线性方程
- 符号计算（小范畴）
- 查表（已知范畴）

### 弦网收缩

**张量网络方法**:
1. 将弦网映射到PEPS
2. 使用CTMRG收缩
3. 计算物理量

## 常见融合范畴

| 名称 | 对象 | $\mathcal{D}$ | 性质 |
|------|------|---------------|------|
| Z₂ | {1, e} | 2 | 阿贝尔 |
| Fibonacci | {1, τ} | φ√2 | 非阿贝尔 |
| Ising | {1, σ, ψ} | 2 | 非阿贝尔 |
| SU(2)ₖ | {0, 1/2, ..., k/2} | √(2sin(π/(k+2))) | 非阿贝尔 |

## 参考文献

### 原始论文

1. **Levin, M. & Wen, X. G.** (2005)
   *String-net condensation: A physical mechanism for topological phases*
   PRB **71**, 045110

### 分类理论

2. **Kitaev, A.** (2006)
   *Anyons in an exactly solved model and beyond*
   Annals of Physics

3. **Wang, Z. et al.** (2010)
   *Topological quantum computation*
   Book - Microsoft Station Q

### 数值方法

4. **Gu, Z. C. et al.** (2009)
   *Tensor-Entanglement-Filtering Renormalization*
   PRB **80**, 155131

---

**下一步**: 实现Fibonacci String-Net，验证编织统计！
