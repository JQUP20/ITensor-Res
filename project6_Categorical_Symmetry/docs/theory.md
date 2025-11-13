# 范畴对称性与SymTFT理论

## 广义对称性简介

### 传统对称性的局限

**传统对称性**（0-form对称性）：
- 全局对称性：U(1), SO(3), etc.
- 作用在点上
- 由群描述

**局限**：
- 无法描述拓扑缺陷
- 忽略了高形式对称性
- 没有捕捉非可逆对称性

### 广义对称性

**现代观点**：对称性是**范畴**，而非群！

包括：
1. **高形式对称性**：作用在扩展对象上（弦、膜...）
2. **非可逆对称性**：对称性算符不可逆
3. **对称性的分数化**：在拓扑序中

## 范畴对称性

### 什么是范畴对称性？

对称性由**融合范畴** $\mathcal{C}$ 描述：

- **对象**：对称性算符
- **态射**：算符间的关系
- **融合**：算符的"乘法"

### Fibonacci对称性示例

**对象**：{1, τ}

**融合**：
- $1 \times a = a$
- $τ \times τ = 1 + τ$

这是**非可逆**对称性！（τ没有逆元）

### 与传统对称性的比较

| 特性 | 群对称性 | 范畴对称性 |
|------|---------|-----------|
| 可逆性 | 总是 | 不一定 |
| 对象 | 群元素 | 范畴对象 |
| 乘法 | 群乘法 | 融合规则 |
| 单位元 | e | 1 |
| 阿贝尔性 | 可能 | 一般不满足 |

## SymTFT（对称性拓扑场论）

### 核心思想

**SymTFT**将d维理论的对称性编码为(d+1)维拓扑场论。

```
     (d+1)D SymTFT
    ┌──────────────┐
    │              │
    │  Topological │
    │     Field    │
    │    Theory    │
    │              │
    └──────────────┘
           │
         边界
           │
    ┌──────────────┐
    │   d-dim      │
    │   Theory     │
    └──────────────┘
```

### 数学构造

对于对称性范畴 $\mathcal{C}$：

$$
\text{SymTFT}[\mathcal{C}] = \text{Drinfeld Center } Z(\mathcal{C})
$$

Drinfeld中心包含：
- $\mathcal{C}$ 的所有对象
- 加上编织结构

### 边界条件

不同的边界条件 → 不同的物理理论

**对称性破缺**：选择边界条件

## 对称性缺陷

### 拓扑缺陷线

在2D理论中，对称性算符是**缺陷线**：

```
    |
    |  ← 缺陷线（对称性算符）
    |
──────────────
  物理系统
──────────────
```

### 融合规则

缺陷线可以融合：

```
  |    |        |
  a    b   →    c
  |    |        |
```

满足：$c \in a \times b$

### 端点

缺陷线的端点 = **对称性荷**

```
    ●  ← 端点（荷）
    |
    a
    |
```

## 对称性富集拓扑序 (SET)

### 定义

**对称性 + 拓扑序**：

系统同时具有：
1. 全局对称性 $\mathcal{C}$
2. 拓扑序（基本上的）

### 分数化

对称性可以**分数化**在任意子上：

- 任意子携带对称性荷的分数
- 不同分数化 → 不同相

### 例子：Z₂拓扑序 + Z₂对称性

**Z₂拓扑序**：任意子 {1, e, m, ψ}

**Z₂对称性作用**：

可能的分数化：
1. 所有任意子偶性 → 平凡
2. e带奇荷，m偶 → 分数化I
3. e偶，m奇 → 分数化II
4. ...

## 反常 (Anomaly)

### 什么是反常？

对称性**不能**在同维度单独实现，需要更高维"bulk"。

### 反常匹配

**边界反常 = 体反常**

SymTFT自动实现反常匹配！

### 例子：手征中心荷

**2D CFT**：
- 左移中心荷 $c_L$
- 右移中心荷 $c_R$

**反常**：$c_L - c_R \neq 0$ (手征)

需要3D bulk来实现！

## 对偶性

### Kramers-Wannier对偶

**经典例子**：2D Ising模型

- 高温 ↔ 低温
- 自旋 ↔ 涡旋

### SymTFT观点

对偶 = **不同边界条件**

```
    SymTFT
    ┌─────┐
    │     │
  边界A  边界B
    │     │
 理论A   理论B
 (对偶)
```

### 非可逆对偶

范畴对称性允许**非可逆对偶**：

不是一一对应，而是多对一映射！

## 数值实现

### 张量网络实现对称性

**对称张量**：

```python
# U(1)对称性
T[i, j, k, s]  # 守恒：i + j = k + charge(s)
```

**融合树表示**：

每个张量指标带融合树标签

### 缺陷张量网络

插入缺陷线：

```
    ──T──T──T──
      │  D  │    ← D = 缺陷张量
    ──T──T──T──
```

### 计算对称性荷

测量端点算符：

$$
Q = \text{Tr}[\text{缺陷端点}]
$$

## 应用

### 1. 相分类

**不同对称性破缺模式**：

每个边界条件 → 一个相

### 2. 相变

**拓扑相变**：

改变拓扑序类型

**对称性破缺相变**：

改变边界条件

### 3. 对偶性发现

SymTFT系统地找到新对偶！

### 4. 反常计算

自动匹配边界和体反常

## 前沿研究

### 1. 非可逆对称性

**例子**：
- Fibonacci对称性
- Haagerup对称性
- 某些共形场论

### 2. 高形式对称性

**1-form对称性**：
- 作用在闭合弦上
- Wilson线的守恒

**2-form对称性**：
- 作用在膜上
- 't Hooft算符

### 3. SymTFT与全息

**AdS/CFT连接**：

(d+1)D SymTFT ↔ (d+2)D引力理论？

### 4. 量子计算

**非可逆对称性**：
- 新型拓扑量子计算？
- 容错机制

## 数学工具

### Drinfeld中心

对融合范畴 $\mathcal{C}$：

$$
Z(\mathcal{C}) = \{(a, β_a) : a \in \mathcal{C}, β_a \text{ 是半辫子}\}
$$

**性质**：
- $Z(\mathcal{C})$ 总是辫子化的
- 模张量范畴（在良好情况）

### 辫子化

**半辫子** $β_a$：$a$ 与所有对象的辫子

$$
β_a : a \otimes - \to - \otimes a
$$

满足自然性和六边形公理

### 模不变量

**S矩阵**：

$$
S_{ab} = \text{Tr}[R_{a,b} R_{b,a}]
$$

**T矩阵**：

$$
T_a = \theta_a  \text{ (扭转因子)}
$$

## 实际例子

### 例1：Ising CFT

**对称性**：Z₂

**SymTFT**：Toric Code (D(Z₂))

**边界条件**：
- Dirichlet → Ising CFT
- Neumann → 平凡CFT

### 例2：SU(2)_k WZW

**对称性**：SU(2)_k

**SymTFT**：D(SU(2)_k)

**边界**：各种共形边界条件

### 例3：分数量子霍尔

**对称性**：U(1)×反演

**SymTFT**：Chern-Simons理论

## 计算技术

### 缺陷张量收缩

```python
def contract_with_defect(TN, defect_line, position):
    # 在指定位置插入缺陷
    for i in position:
        TN[i] = apply_defect(TN[i], defect_line)

    # 收缩
    return contract(TN)
```

### 对称性检验

验证守恒定律：

```python
def check_symmetry(state, operator):
    # 应用对称性
    state_transformed = apply(operator, state)

    # 检查不变性
    return norm(state - state_transformed) < epsilon
```

## 常见范畴对称性

| 对称性 | 类型 | 可逆 | 应用 |
|--------|------|------|------|
| Z_N | 阿贝尔群 | 是 | 传统对称性 |
| U(1) | 李群 | 是 | 电荷守恒 |
| Fibonacci | 融合范畴 | 否 | TQC, CFT |
| Rep(G) | 群表示 | 是 | 规范理论 |
| Haagerup | 子因子 | 否 | 数学物理 |

## 参考文献

### 综述

1. **Gaiotto, D. et al.** (2015)
   *Generalized Global Symmetries*
   JHEP

2. **Freed, D. & Moore, G.** (2013)
   *Twisted equivariant matter*
   Annales Henri Poincaré

### SymTFT

3. **Freed, D. et al.** (2022)
   *Topological symmetry in quantum field theory*
   arXiv

4. **Apruzzi, F. et al.** (2021)
   *Symmetry TFTs from String Theory*
   arXiv

### 非可逆对称性

5. **Bhardwaj, L. & Schafer-Nameki, S.** (2023)
   *Generalized Charges, Part I*
   arXiv

---

**下一步**: 实现缺陷张量网络，探索非可逆对称性！
