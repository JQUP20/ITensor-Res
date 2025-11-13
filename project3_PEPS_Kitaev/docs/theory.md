# Kitaev蜂窝模型与拓扑序理论

## Kitaev模型简介

### 哈密顿量

$$
H = -J_x \sum_{\langle ij \rangle_x} \sigma_i^x \sigma_j^x
    -J_y \sum_{\langle ij \rangle_y} \sigma_i^y \sigma_j^y
    -J_z \sum_{\langle ij \rangle_z} \sigma_i^z \sigma_j^z
$$

其中：
- $\langle ij \rangle_x, \langle ij \rangle_y, \langle ij \rangle_z$：三种不同方向的键
- 蜂窝格：每个格点有三个邻居

### 为什么重要？

1. **精确可解**: 可以精确对角化（Jordan-Wigner + Majorana费米子）
2. **拓扑序**: Z₂自旋液体相
3. **任意子**: 支持非阿贝尔任意子
4. **实验相关**: 可能在某些材料中实现

## 精确解

### Majorana费米子表示

每个自旋-1/2分解为四个Majorana费米子：

$$
\sigma_i^x = ib_i^x c_i, \\quad
\sigma_i^y = ib_i^y c_i, \\quad
\sigma_i^z = ib_i^z c_i
$$

其中 $b_i^\alpha, c_i$ 满足：
$$
\{b_i^\alpha, b_j^\beta\} = 2\delta_{ij}\delta^{\alpha\beta}, \\quad
\{c_i, c_j\} = 2\delta_{ij}
$$

### 守恒量

每个格点周围定义plaquette算符：

$$
W_p = \prod_{i \in p} \sigma_i^{\alpha(i)}
$$

所有 $W_p$ 都与H对易！

这些是**磁通守恒量** - 对应Z₂规范场的磁通。

## 拓扑相图

### 各向同性点

当 $J_x = J_y = J_z$：
- **基态**: Z₂自旋液体
- **能隙**: 有能隙
- **激发**: 任意子

### 不同相

1. **A相** ($J_x, J_y \ll J_z$): 类似Toric code
2. **B相** ($J_z \ll J_x, J_y$): 另一种拓扑相
3. **临界线**: 某些参数线上无能隙

### 相图

```
       Jx
        |
    A   |   B
  ------●------  Jy
        |
        |
       Jz
```

## 任意子

### 基本激发

1. **e**: electric charge (Z₂电荷)
2. **m**: magnetic vortex (Z₂磁通)
3. **ψ**: fermion (费米子)

### 融合规则

$$
e \times e = 1, \\quad m \times m = 1, \\quad ψ \times ψ = 1
$$

$$
e \times m = ψ, \\quad e \times ψ = m, \\quad m \times ψ = e
$$

这是**Z₂拓扑序**！

### 统计

- e: boson
- m: boson
- ψ: fermion

编织: e绕m一圈 → 相位π

## 拓扑纠缠熵

### Kitaev-Preskill构造

将系统分为三个区域A, B, C:

```
  A
 ╱ ╲
B   C
```

拓扑纠缠熵：

$$
S_{\text{topo}} = S_A + S_B + S_C - S_{AB} - S_{BC} - S_{AC} + S_{ABC}
$$

### 理论预测

$$
S_{\text{topo}} = \ln(\mathcal{D})
$$

其中 $\mathcal{D}$ 是总量子维数。

对于Z₂拓扑序：
$$
\mathcal{D} = \sqrt{\sum_a d_a^2} = \sqrt{1^2 + 1^2 + 1^2 + 1^2} = 2
$$

因此：
$$
S_{\text{topo}} = \ln 2 \approx 0.693
$$

## PEPS表示

### 为什么用PEPS？

MPS只适用于1D系统。2D需要PEPS！

### PEPS张量结构

每个格点一个张量：

```
    ↑
    |
←---●---→
    |
    ↓
```

张量形状: $(D, D, D, D, d)$
- 4个虚指标(D)
- 1个物理指标(d=2)

### 收缩困难

精确收缩PEPS是指数难的！

需要近似方法：
1. **简单更新(SU)**: 独立更新每个张量
2. **CTMRG**: 角转移矩阵重整化群
3. **全更新(FU)**: 考虑环境

## CTMRG算法

### 基本思想

用环境张量近似无限系统：

```
C----T----C
|    |    |
T----●----T
|    |    |
C----T----C
```

- C: 角张量(Corner)
- T: 边张量(Transfer)
- ●: PEPS张量

### 算法步骤

1. **初始化**: 随机C和T
2. **左移**: 插入一列,截断
3. **上移**: 插入一行,截断
4. **右移**: ...
5. **下移**: ...
6. **重复**: 直到收敛

### 关键技巧

- 对称化环境
- 控制χ(环境键维度)
- 监控收敛

## 数值挑战

### 符号问题

虽然Kitaev模型精确可解,但：
- PEPS优化可能陷入局部极小
- 符号问题难处理
- 需要好的初始猜测

### 解决方案

1. 从精确解构造初始PEPS
2. 使用对称性
3. 多次随机初始化

## 与Toric Code的关系

Kitaev模型在特定极限 → Toric code

### Toric Code

$$
H = -\sum_v A_v - \sum_p B_p
$$

- $A_v = \prod_{i \in v} \sigma_i^x$: 顶点算符
- $B_p = \prod_{i \in p} \sigma_i^z$: 格点算符

完全可解,同样的Z₂拓扑序！

## 实验实现

### 候选材料

1. **α-RuCl₃**: 可能的Kitaev材料
   - 蜂窝格
   - 强自旋轨道耦合
   - 实验证据不确定

2. **Na₂IrO₃**: 另一候选
   - 也是蜂窝格
   - 复杂磁序

### 挑战

真实材料总有额外相互作用！

$$
H = H_{\text{Kitaev}} + H_{\text{Heisenberg}} + H_{\text{other}}
$$

难以实现纯Kitaev模型。

## 量子计算应用

### 拓扑量子计算

非阿贝尔任意子(如Fibonacci任意子)可以用于：
- 拓扑保护的量子比特
- 容错量子门

Kitaev模型的e,m,ψ是阿贝尔任意子,但：
- 理解基础概念
- 推广到非阿贝尔情况

## 参考文献

### 原始论文

1. **Kitaev, A.** (2006)
   *Anyons in an exactly solved model and beyond*
   Annals of Physics **321**, 2-111

### PEPS方法

2. **Verstraete, F. & Cirac, J. I.** (2004)
   *Renormalization algorithms for Quantum-Many Body Systems*

3. **Jiang, H. C. et al.** (2008)
   *Accurate Determination of Tensor Network State*
   PRL **101**, 090603

### 拓扑纠缠熵

4. **Kitaev, A. & Preskill, J.** (2006)
   *Topological Entanglement Entropy*
   PRL **96**, 110404

5. **Levin, M. & Wen, X. G.** (2006)
   *Detecting Topological Order*
   PRL **96**, 110405

---

**下一步**: 运行PEPS代码,验证拓扑序！
