# DMRG与Haldane相理论

## Haldane猜想

### 历史背景

1983年，Haldane提出了一个深刻的猜想：

**整数自旋反铁磁链有能隙，半整数自旋反铁磁链无能隙。**

这个猜想后来被证明，并导致了对称保护拓扑(SPT)相的发现。

### 物理图像

**半整数自旋(S=1/2)**:
- 基态：临界态
- 关联：代数衰减
- 能隙：无能隙
- 边缘态：无

**整数自旋(S=1)**:
- 基态：Haldane相(SPT)
- 关联：指数衰减
- 能隙：Δ ≈ 0.41J
- 边缘态：边缘自旋-1/2

## AKLT模型

### 哈密顿量

$$
H_{\text{AKLT}} = \sum_i \left[ \mathbf{S}_i \cdot \mathbf{S}_{i+1} + \frac{1}{3} (\mathbf{S}_i \cdot \mathbf{S}_{i+1})^2 \right]
$$

### 为什么重要？

1. **精确可解**: AKLT态是精确的基态
2. **VBS表示**: 可以写成价键固体(Valence Bond Solid)
3. **MPS形式**: 自然的MPS表示
4. **拓扑保护**: 边缘态受Z₂对称保护

### VBS图像

每个自旋-1可以看作两个自旋-1/2的对称组合：

$$
|S=1, m\rangle = \sum_{m_1, m_2} C_{m_1 m_2}^{1m} |1/2, m_1\rangle \otimes |1/2, m_2\rangle
$$

AKLT基态：相邻自旋-1/2形成单态键

```
[●══●][●══●][●══●]...
```

边界的自旋-1/2自由 → 边缘态！

## 弦序参数

### 定义

$$
O_z(i,j) = \langle S_i^z \exp\left(i\pi \sum_{k=i+1}^{j-1} S_k^z\right) S_j^z \rangle
$$

### 物理意义

- **局域关联**: $\langle S_i^z S_j^z \rangle$ 指数衰减
- **弦序**: $O_z(i,j)$ 长程有序！

对于AKLT态：
$$
\lim_{|i-j|\to\infty} O_z(i,j) = -\frac{4}{9} \approx 0.444
$$

（数值修正后约0.374）

### 为什么叫"隐藏序"？

普通关联函数看不到，需要插入弦算符 $\exp(i\pi\sum S_k^z)$。

## 边缘态物理

### 开放边界vs周期边界

**周期边界(PBC)**:
- 唯一基态
- 无边缘态
- 完全能隙

**开放边界(OBC)**:
- 四重简并基态
- 边缘自旋-1/2
- 边缘无能隙，体有能隙

### 四重简并

两个边缘，每个贡献自旋-1/2：

总自旋: $S_{\text{total}} = S_{\text{left}} + S_{\text{right}}$

可能态：
1. $|\uparrow\uparrow\rangle$ - 总自旋S=1, Sz=+1
2. $|\uparrow\downarrow\rangle + |\downarrow\uparrow\rangle$ - S=1, Sz=0
3. $|\downarrow\downarrow\rangle$ - S=1, Sz=-1
4. $|\uparrow\downarrow\rangle - |\downarrow\uparrow\rangle$ - S=0, Sz=0

前三个形成S=1三重态，第四个是S=0单态。

### 纠缠熵签名

在边缘处纠缠熵：
$$
S_{\text{edge}} = \ln 2
$$

这是边缘自旋-1/2的纠缠！

## DMRG算法详解

### 基本思想

将系统分为四块：
```
[Left Block] [Site i] [Site i+1] [Right Block]
```

在中心两个格点对角化，保留最重要的态。

### 算法步骤

1. **初始化**: 构建左右块
2. **扫描向右**:
   - 扩展左块
   - 对角化中心
   - 截断态空间(保留χ个态)
3. **扫描向左**: 反向操作
4. **重复**: 直到能量收敛

### 为什么有效？

**纠缠熵有界** → 只需保留有限个施密特值 → 多项式复杂度

### 收敛判据

1. **能量收敛**: $|E_n - E_{n-1}| < \epsilon$
2. **截断误差**: $\epsilon_{\text{trunc}} = 1 - \sum_{\alpha=1}^{\chi} \lambda_\alpha^2 < \delta$

### 性能考虑

**内存**: $O(L \chi^2 d)$
**时间**: $O(L \chi^3 d^2)$ 每次扫描

对于S=1, d=3：
- χ=100: 可以计算L~100
- χ=500: 可以计算L~200

## SPT相分类

### 什么是SPT？

**对称保护拓扑(Symmetry Protected Topological)相**:
- 有能隙
- 无内禀拓扑序(无任意子)
- 对称时拓扑非平凡
- 破坏对称时平凡

### Haldane相的对称性

保护对称：
1. 时间反演: $T$
2. 链反射: $P$ (或称为位反演)
3. 自旋旋转: $SO(3)$ (或至少$SO(2) \times \mathbb{Z}_2^T$)

破坏任一对称 → 边缘态消失！

### 拓扑不变量

对于1D SPT with SO(3)对称：
$$
\mathbb{Z}_2 \text{ classification}
$$

Haldane相 = 非平凡类
平凡顺磁相 = 平凡类

### 与2D拓扑绝缘体的类比

| 1D Haldane | 2D TI |
|------------|-------|
| 边缘自旋-1/2 | 边缘螺旋态 |
| 体能隙 | 体能隙 |
| SO(3)对称 | 时间反演对称 |
| Z₂分类 | Z₂分类 |

## 相图

### 参数空间

考虑推广哈密顿量：
$$
H = \sum_i \left[ J_1 \mathbf{S}_i \cdot \mathbf{S}_{i+1} + J_2 (\mathbf{S}_i \cdot \mathbf{S}_{i+1})^2 + D(S_i^z)^2 \right]
$$

### 相边界

1. **Haldane相**: J₁>0, 适度J₂
2. **Néel相**: 大单轴各向异性D
3. **Large-D相**: 非常大D
4. **二聚化相**: 某些参数区域

### 相变类型

- Haldane ↔ Néel: 一阶相变
- Haldane ↔ Large-D: 二阶相变(Gaussian)

## 数值签名

### 如何识别Haldane相？

1. **能隙**: Δ > 0
2. **弦序**: O_z → 常数
3. **边缘简并**: 4倍(OBC)
4. **边缘纠缠**: S_edge ≈ ln2
5. **关联长度**: ξ < ∞

### 对比其他相

**平凡相**:
- 能隙 ✓
- 弦序 ✗
- 边缘简并 ✗

**临界相**:
- 能隙 ✗
- 无穷关联长度

**Néel序**:
- 自发对称破缺
- 磁化 ≠ 0

## 实验实现

### 准一维材料

1. **NENP**: Ni(C₂H₈N₂)₂NO₂ClO₄
   - 证实Haldane能隙
   - 中子散射

2. **Y₂BaNiO₅**: 钇钡镍氧化物
   - S=1反铁磁链
   - 能隙 Δ ≈ 10K

### 冷原子实现

用光晶格实现S=1玻色原子链：
- 可调相互作用
- 直接观测边缘态
- 量子淬火动力学

## 开放问题

1. 高自旋(S>1)的推广
2. 阶梯系统(2条链)
3. 无序效应
4. 有限温度性质
5. 动力学响应

## 参考文献

### 原始论文

1. **Haldane, F. D. M.** (1983)
   *Continuum dynamics of the 1-D Heisenberg antiferromagnet*
   Physics Letters A **93**, 464

2. **Affleck, I., Kennedy, T., Lieb, E. H. & Tasaki, H.** (1987)
   *Rigorous results on valence-bond ground states*
   PRL **59**, 799

### 现代综述

3. **Chen, X., Gu, Z.-C. & Wen, X.-G.** (2011)
   *Classification of gapped symmetric phases*
   PRB **83**, 035107

4. **Pollmann, F. & Turner, A. M.** (2012)
   *Detection of symmetry-protected topological phases*
   PRB **86**, 125441

---

**下一步**: 理解这些理论后，运行DMRG代码验证！
