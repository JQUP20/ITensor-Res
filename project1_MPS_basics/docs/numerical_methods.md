# 数值方法详解

## MPS表示的实现

### 数据结构

MPS由一系列张量组成:

```python
class MPS:
    def __init__(self, L, d, chi):
        self.L = L          # 系统大小
        self.d = d          # 物理维度
        self.chi = chi      # 键维度
        self.tensors = []   # 张量列表
```

每个张量 `A[i]` 的形状:
- `A[0]`: `(1, chi[0], d)` - 左边界
- `A[i]`: `(chi[i-1], chi[i], d)` - 体
- `A[L-1]`: `(chi[L-2], 1, d)` - 右边界

### 标准型 (Canonical Form)

#### 左标准型 (Left-canonical)

$$
\sum_{s,\alpha} A^s_{\alpha\beta} (A^s_{\alpha\gamma})^* = \delta_{\beta\gamma}
$$

实现:
```python
def left_canonicalize(A):
    chi_l, chi_r, d = A.shape
    # Reshape: (chi_l, chi_r*d)
    mat = A.reshape(chi_l, chi_r*d)
    # QR分解
    Q, R = np.linalg.qr(mat)
    # 新张量
    A_new = Q.reshape(chi_l, -1, d)
    return A_new, R
```

#### 右标准型 (Right-canonical)

类似，使用RQ分解。

### 混合标准型

一般形式:

$$
|\psi\rangle = \sum_{s_1\ldots s_L} A^{s_1} \cdots A^{s_{i-1}} \Lambda^{[i]} B^{s_{i+1}} \cdots B^{s_L}
$$

其中:
- $A$: 左标准
- $B$: 右标准
- $\Lambda$: 对角矩阵（施密特值）

## 施密特分解算法

### 方法1: 直接SVD

```python
def schmidt_decomposition(psi, position):
    # 将MPS分为左右两部分
    left_part = contract_left(psi, position)   # (D_L, d^{pos})
    right_part = contract_right(psi, position)  # (d^{L-pos}, D_R)

    # 合并并reshape
    full_matrix = contract(left_part, right_part)  # (D_L * d^{pos}, D_R * d^{L-pos})

    # SVD
    U, S, Vt = np.linalg.svd(full_matrix, full_matrices=False)

    return U, S, Vt
```

**复杂度**: $\mathcal{O}(\chi^3 d^L)$ - 对大系统不可行！

### 方法2: 从MPS直接提取

如果MPS已经是混合标准型，施密特值直接在 $\Lambda^{[i]}$ 中！

```python
def get_schmidt_values_from_mps(mps, position):
    # 标准化到position
    mps.canonicalize_to(position)
    # 提取对角矩阵
    return mps.lambdas[position]
```

**复杂度**: $\mathcal{O}(L\chi^3)$ - 多项式！

## 纠缠熵计算

### 冯诺依曼熵

```python
def von_neumann_entropy(schmidt_values):
    # 归一化
    sv = schmidt_values / np.linalg.norm(schmidt_values)

    # 计算熵
    entropy = 0.0
    for s in sv:
        if s > 1e-14:  # 避免log(0)
            p = s**2
            entropy -= p * np.log(p)

    return entropy
```

### 数值稳定性

问题：小的施密特值可能导致 `log(0)`

解决方案:
1. 设置阈值过滤
2. 使用 `np.where` 避免条件分支
3. 重写为: $S = -\sum_\alpha p_\alpha \ln p_\alpha$ 其中 $p_\alpha = \lambda_\alpha^2$

```python
def von_neumann_entropy_stable(schmidt_values, threshold=1e-14):
    sv = schmidt_values / np.linalg.norm(schmidt_values)
    p = sv**2
    # 仅保留大于阈值的项
    p_filtered = p[p > threshold]
    return -np.sum(p_filtered * np.log(p_filtered))
```

## 截断误差控制

### 自适应截断

```python
def adaptive_truncate(schmidt_values, chi_max, svd_min=1e-12,
                     truncation_error_max=1e-10):
    # 方法1: 固定chi
    chi_trunc = min(chi_max, len(schmidt_values))

    # 方法2: 阈值
    mask = schmidt_values > svd_min
    chi_threshold = np.sum(mask)

    # 方法3: 截断误差
    cumsum = np.cumsum(schmidt_values[::-1]**2)[::-1]
    chi_error = np.searchsorted(cumsum, truncation_error_max)

    # 取最严格的
    chi_final = min(chi_trunc, chi_threshold, chi_error)

    return chi_final
```

### 截断误差定义

$$
\epsilon = 1 - \sum_{\alpha=1}^{\chi} \lambda_\alpha^2
$$

表示被截断的概率。

## TeNPy实现细节

### 模型定义

```python
from tenpy.models.tf_ising import TFIChain

model_params = {
    'L': 50,              # 长度
    'J': 1.0,             # 耦合
    'g': 0.5,             # 横场（注意：TeNPy用g不是h）
    'bc_MPS': 'finite',   # 边界条件
    'conserve': None      # 不保留对称性（可选：'parity'）
}

model = TFIChain(model_params)
```

### 初始态

```python
from tenpy.networks.mps import MPS

# 产品态
psi = MPS.from_product_state(
    model.lat.mps_sites(),
    ['up'] * L,           # 所有自旋向上
    bc='finite'
)

# 随机态
psi_random = MPS.from_product_state(
    model.lat.mps_sites(),
    np.random.choice(['up', 'down'], L),
    bc='finite'
)
```

### 纠缠熵提取

```python
# TeNPy自动维护标准型
entropies = psi.entanglement_entropy()

# 特定位置
S_10 = psi.entanglement_entropy()[10]

# 完整施密特谱
schmidt_values = psi.get_SL(10)  # 第10个键的施密特值
```

### 观测量计算

```python
# 局域期望值
magnetization = [psi.expectation_value('Sz', i) for i in range(L)]

# 关联函数
correlation = psi.correlation_function('Sz', 'Sz', [0], list(range(L)))
```

## 精确对角化对比

### 小系统ED

```python
def exact_diagonalization(L, J, h):
    # 构建哈密顿量
    H = build_hamiltonian_matrix(L, J, h)  # 2^L × 2^L

    # 对角化
    eigenvalues, eigenvectors = np.linalg.eigh(H)

    # 基态
    psi_gs = eigenvectors[:, 0]
    E_gs = eigenvalues[0]

    return psi_gs, E_gs

def entanglement_from_state_vector(psi, L, position):
    # Reshape为矩阵
    dim_L = 2**position
    dim_R = 2**(L - position)

    psi_matrix = psi.reshape(dim_L, dim_R)

    # SVD
    U, S, Vt = np.linalg.svd(psi_matrix, full_matrices=False)

    # 纠缠熵
    return von_neumann_entropy(S)
```

### 复杂度对比

| 方法 | 构建 | 对角化 | 纠缠熵 | 总计 |
|------|------|--------|--------|------|
| ED | $\mathcal{O}(L \cdot 2^{2L})$ | $\mathcal{O}(2^{3L})$ | $\mathcal{O}(2^{3L_{pos}})$ | $\mathcal{O}(2^{3L})$ |
| MPS | $\mathcal{O}(L)$ | $\mathcal{O}(L\chi^3)$ | $\mathcal{O}(\chi)$ | $\mathcal{O}(L\chi^3)$ |

ED限制: $L \lesssim 20$
MPS可达: $L \sim 10^3$ (如果 $\chi \sim 100$)

## CFT拟合算法

### 线性回归

```python
def fit_cft_central_charge(positions, entropies, fit_range=None):
    if fit_range is None:
        # 取中间50%
        start = len(positions) // 4
        end = 3 * len(positions) // 4
        fit_range = (start, end)

    start, end = fit_range
    log_pos = np.log(positions[start:end])
    ent = entropies[start:end]

    # 线性拟合 S = (c/6) log(l) + const
    p = np.polyfit(log_pos, ent, 1)

    c = 6 * p[0]       # 中心电荷
    const = p[1]       # 常数项

    # R²拟合优度
    residuals = ent - (p[0] * log_pos + p[1])
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((ent - np.mean(ent))**2)
    r_squared = 1 - (ss_res / ss_tot)

    return c, const, r_squared
```

### 有限尺寸修正

对于有限系统 $L$:

$$
S(l) = \frac{c}{6} \ln\left(\frac{L}{\pi} \sin\frac{\pi l}{L}\right) + s_0
$$

```python
def fit_finite_size_cft(positions, entropies, L):
    # 修正的x坐标
    x = (L / np.pi) * np.sin(np.pi * positions / L)
    log_x = np.log(x)

    # 拟合
    p = np.polyfit(log_x, entropies, 1)
    c = 6 * p[0]

    return c
```

## 性能优化

### 1. 向量化

避免Python循环:
```python
# 慢
for i in range(L):
    result[i] = compute_something(A[i])

# 快
result = np.vectorize(compute_something)(A)
```

### 2. 使用Numba

```python
from numba import jit

@jit(nopython=True)
def fast_contraction(A, B):
    # 快速张量收缩
    return np.tensordot(A, B, axes=([1], [0]))
```

### 3. 内存管理

- 重用数组而非重新分配
- 使用 `np.einsum` 进行复杂收缩
- 及时删除大数组

### 4. 并行化

```python
from multiprocessing import Pool

def compute_for_h(h):
    # 计算单个h值
    return run_dmrg(h)

# 并行扫描
with Pool(processes=4) as pool:
    results = pool.map(compute_for_h, h_values)
```

## 调试技巧

### 1. 检查归一化

```python
assert np.abs(np.linalg.norm(psi) - 1.0) < 1e-10
```

### 2. 验证对称性

```python
# 检查哈密顿量厄米性
assert np.allclose(H, H.conj().T)
```

### 3. 比较小系统

用ED验证 $L=8$ 的结果。

### 4. 收敛监控

```python
for sweep in range(max_sweeps):
    E_old = E
    E = dmrg_sweep(psi, H)

    if abs(E - E_old) < 1e-10:
        print(f"收敛于sweep {sweep}")
        break
```

## 常见陷阱

1. **未标准化MPS**: 导致错误的纠缠熵
2. **chi太小**: 临界点需要大chi
3. **边界效应**: 使用开放边界注意边缘
4. **浮点误差**: 施密特值排序可能不稳定

---

**实践建议**: 从小系统开始，验证正确性后再增大！
