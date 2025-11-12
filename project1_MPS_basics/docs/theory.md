# 项目1理论背景

## 矩阵乘积态(MPS)

### 基本概念

一维量子多体态可以写成矩阵乘积形式:

$$
|\psi\rangle = \sum_{s_1,\ldots,s_L} \text{Tr}[A^{s_1}[1] A^{s_2}[2] \cdots A^{s_L}[L]] |s_1 s_2 \cdots s_L\rangle
$$

其中:
- $A^{s_i}[i]$ 是 $\chi_{i-1} \times \chi_i$ 矩阵
- $s_i$ 是物理指标（对自旋-1/2：$s_i \in \{0,1\}$）
- $\chi_i$ 是键维度(bond dimension)

### 为什么MPS有效？

**纠缠面积律**: 对于基态，纠缠熵满足

$$
S(L_A) \propto \text{Area}(\partial A)
$$

一维系统中，边界是零维点，因此 $S \sim \text{const}$，可用有限 $\chi$ 表示。

## 施密特分解

将系统分为左右两部分 $A$ 和 $B$:

$$
|\psi\rangle = \sum_{\alpha=1}^{\chi} \lambda_\alpha |\phi_\alpha\rangle_A \otimes |\chi_\alpha\rangle_B
$$

其中:
- $\lambda_\alpha$ 是**施密特值**，满足 $\sum_\alpha \lambda_\alpha^2 = 1$
- $|\phi_\alpha\rangle_A$ 和 $|\chi_\alpha\rangle_B$ 分别是 $A$ 和 $B$ 的正交基
- $\chi$ 是**施密特秩**

### 性质

1. **唯一性**: 施密特分解（除简并情况）是唯一的
2. **纠缠度量**: 施密特值直接描述纠缠程度
3. **约化密度矩阵**: $\rho_A = \sum_\alpha \lambda_\alpha^2 |\phi_\alpha\rangle\langle\phi_\alpha|$

## 冯诺依曼纠缠熵

定义:

$$
S_\text{vN} = -\text{Tr}(\rho_A \ln \rho_A) = -\sum_\alpha \lambda_\alpha^2 \ln(\lambda_\alpha^2)
$$

### 性质

1. **非负性**: $S \geq 0$
2. **最大值**: 对于 $\dim(\mathcal{H}_A) = d$, $S_\text{max} = \ln d$
3. **可加性**: 对无纠缠态 $S(\rho_A \otimes \rho_B) = S(\rho_A) + S(\rho_B)$

## 横场伊辛模型

哈密顿量:

$$
H = -J \sum_{i=1}^{L-1} \sigma_i^z \sigma_{i+1}^z - h \sum_{i=1}^L \sigma_i^x
$$

### 相图

#### 1. 铁磁相 ($h \ll J$)
- **基态**: $|\uparrow\uparrow\cdots\uparrow\rangle$ 或 $|\downarrow\downarrow\cdots\downarrow\rangle$
- **对称性**: 自发 $\mathbb{Z}_2$ 对称破缺
- **纠缠**: 面积律，$S \sim \text{const}$
- **关联长度**: $\xi \sim e^{J/h}$（指数小）

#### 2. 顺磁相 ($h \gg J$)
- **基态**: $|\rightarrow\rightarrow\cdots\rightarrow\rangle$ (所有自旋沿 $x$ 方向)
- **对称性**: 对称
- **纠缠**: 弱纠缠
- **关联长度**: $\xi \sim J/h$（小）

#### 3. 临界点 ($h = h_c = J$)
- **量子相变**: 连续相变
- **普适类**: 2D经典伊辛模型（量子-经典对应）
- **共形场论**: $c = 1/2$ 自由费米子
- **关联长度**: $\xi \to \infty$
- **纠缠**: 对数发散

$$
S(l) = \frac{c}{6} \ln(l) + \text{const} = \frac{1}{12} \ln(l) + \text{const}
$$

### 对偶性

通过Jordan-Wigner变换，模型等价于自由费米子:

$$
H = -\sum_i (c_i^\dagger c_{i+1} + \text{h.c.}) - h \sum_i (2n_i - 1)
$$

可精确求解！

## 纠缠标度

### 面积律 (Area Law)

非临界相:

$$
S \sim \text{const}
$$

物理图像：短程纠缠，局域化

### 对数违反 (Logarithmic Violation)

临界点（1D）:

$$
S(l) \sim \frac{c}{3} \ln\left(\frac{L}{\pi} \sin\frac{\pi l}{L}\right) + s_0
$$

其中:
- $c$: 中心电荷
- $L$: 系统大小
- $l$: 子系统大小

### 体积律 (Volume Law)

热态或随机态:

$$
S \sim L^{d-1}
$$

## Rényi熵

定义:

$$
S_n = \frac{1}{1-n} \ln\left(\sum_\alpha \lambda_\alpha^{2n}\right)
$$

特殊情况:
- $n=1$: 冯诺依曼熵（取极限）
- $n=2$: $S_2 = -\ln(\text{Tr}(\rho^2))$
- $n=\infty$: $S_\infty = -\ln(\lambda_\text{max}^2)$

## CFT预测

### 中心电荷提取

从纠缠熵拟合:

$$
S(l) = \frac{c}{6} \ln(l) + \text{const}
$$

斜率 $= c/6 \Rightarrow c = 6 \times \text{slope}$

### 标度维度

算符 $\mathcal{O}$ 的标度维度 $\Delta$ 通过关联函数:

$$
\langle \mathcal{O}(0) \mathcal{O}(r) \rangle \sim r^{-2\Delta}
$$

伊辛模型:
- 自旋算符: $\Delta_\sigma = 1/8$
- 能量算符: $\Delta_\varepsilon = 1$

## 数值方法

### 精确对角化 (ED)

- **优点**: 精确
- **缺点**: 指数复杂度 $\mathcal{O}(2^L)$，限于 $L \lesssim 20$

### MPS表示

- **优点**: 多项式复杂度 $\mathcal{O}(L\chi^3)$
- **缺点**: 需选择合适 $\chi$，可能有截断误差

### 变分优化

后续项目2将学习DMRG算法优化MPS。

## 参考文献

1. **Schollwöck (2011)** - *Ann. Phys. 326, 96*
   MPS和DMRG综述

2. **Calabrese & Cardy (2004)** - *J. Stat. Mech. P06002*
   纠缠熵与CFT

3. **Eisert et al. (2010)** - *Rev. Mod. Phys. 82, 277*
   面积律综述

4. **Sachdev (2011)** - *Quantum Phase Transitions*
   量子相变教材

5. **Vidal (2003)** - *Phys. Rev. Lett. 91, 147902*
   高效经典模拟

---

**下一步**: 理解这些概念后，运行代码验证理论预测！
