# 张量网络研究工作流指南

本指南为博士生和研究人员提供使用本框架的最佳实践。

## 目录

1. [快速开始](#快速开始)
2. [研究流程](#研究流程)
3. [常见任务](#常见任务)
4. [高级功能](#高级功能)
5. [发表论文](#发表论文)
6. [故障排除](#故障排除)

---

## 快速开始

### 环境设置

```bash
# 1. 克隆仓库
git clone <repository-url>
cd ITensor-Res

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行测试
python tests/test_all.py

# 4. 尝试示例
python scripts/run_all_examples.py
```

### 15分钟教程

遵循 `QUICKSTART.md` 获取基础概述。

---

## 研究流程

### 第1阶段：理论学习（1-2个月）

#### Week 1-2: MPS基础
```bash
# 学习路径
1. 阅读 project1_MPS_basics/README.md
2. 运行 notebooks/01_MPS_introduction.ipynb
3. 完成练习题
4. 实现自己的MPS算法变体
```

**里程碑**：能够独立实现DMRG算法

#### Week 3-4: 拓扑序入门
```bash
1. 学习 project2_DMRG_Haldane/docs/theory.md
2. 理解SPT相和边缘态
3. 运行 notebooks/02_Haldane_phase.ipynb
4. 计算实际系统的弦序参数
```

**里程碑**：理解拓扑不变量

#### Week 5-8: 高级主题
- Project 3: PEPS与CTMRG
- Project 4: MERA与CFT
- Project 5: String-Net液体
- Project 6: 范畴对称性

### 第2阶段：数值实践（2-3个月）

#### 基准测试

```bash
# 运行性能基准
cd common/benchmarks
python performance_benchmark.py

# 优化代码
python gpu_acceleration.py  # 如果有GPU
```

#### 实际系统模拟

**示例：研究新的拓扑相**

```python
# my_research/new_topological_phase.py
import sys
sys.path.append('../project3_PEPS_Kitaev/src')

from ctmrg import CTMRG
from topological_entropy import TopologicalEntropy

# 定义你的哈密顿量
H = ...  # 你的模型

# 使用CTMRG求基态
ctmrg = CTMRG(peps_tensor, chi=30)
ctmrg.iterate(max_iter=100)

# 计算拓扑纠缠熵
topo_calc = TopologicalEntropy()
S_topo = topo_calc.kitaev_preskill(...)

print(f"拓扑纠缠熵: {S_topo}")
# 分析结果...
```

### 第3阶段：原创研究（3-6个月）

#### 研究主题示例

1. **新拓扑相发现**
   - 修改 Kitaev 模型
   - 使用 CTMRG 求基态
   - 计算拓扑不变量
   - 分类新相

2. **非阿贝尔任意子**
   - 从 Fibonacci 范畴开始
   - 实现编织算法
   - 验证融合规则
   - 探索TQC应用

3. **范畴对称性**
   - 研究非可逆对称性
   - 构造 SymTFT
   - 分类对偶性
   - 反常匹配

---

## 常见任务

### 任务1：计算纠缠熵

```python
# 使用 Project 1 工具
from project1_MPS_basics.src.entanglement import compute_entanglement_spectrum

# 获取MPS态
psi = run_dmrg(...)  # 你的DMRG代码

# 计算纠缠谱
spectrum = compute_entanglement_spectrum(psi, position=L//2)

# 计算熵
S = -np.sum(spectrum**2 * np.log(spectrum**2))
print(f"纠缠熵: {S}")
```

### 任务2：提取CFT数据

```python
# 使用 Project 4 工具
from project4_MERA_CFT.src.cft_analysis import CFTAnalyzer

analyzer = CFTAnalyzer()

# 从纠缠熵提取中心荷
L_values = np.array([10, 20, 30, 40, 50])
S_values = calculate_entanglement(L_values)

c, fit_data = analyzer.extract_central_charge(L_values, S_values)
print(f"中心荷 c = {c:.4f}")

# 绘图
analyzer.plot_central_charge_extraction(fit_data)
```

### 任务3：验证融合范畴

```python
# 使用 Project 5 工具
from project5_String-Net.src.f_symbol_verification import FSymbolVerifier
from project5_String-Net.src.levin_wen_model import FibonacciCategory

fib = FibonacciCategory()
verifier = FSymbolVerifier(fib)

# 综合验证
report = verifier.comprehensive_verification()

if report['unitarity']['verified']:
    print("✓ F-符号一致性验证通过")
```

### 任务4：PEPS优化

```python
# 使用 Project 3 CTMRG
from project3_PEPS_Kitaev.src.ctmrg import CTMRG

# 初始化PEPS
peps_tensor = initialize_peps(D=4, d=2)

# CTMRG优化
ctmrg = CTMRG(peps_tensor, chi=30)
result = ctmrg.iterate(max_iter=100, tol=1e-8)

print(f"收敛: {result['converged']}")
print(f"最终误差: {result['final_diff']:.2e}")
```

---

## 高级功能

### GPU加速

```python
# 使用 common/utils/gpu_acceleration.py
from common.utils.gpu_acceleration import GPUTensorOps

gpu_ops = GPUTensorOps()

# 在GPU上进行张量收缩
result = gpu_ops.contract_network(tensor_network, backend='jax')
```

### 并行计算

```python
# 使用多进程加速
from multiprocessing import Pool

def compute_for_parameter(param):
    # 计算单个参数点
    return result

# 并行扫描参数空间
with Pool(processes=8) as pool:
    results = pool.map(compute_for_parameter, parameter_values)
```

### 自动微分

```python
# 使用JAX进行自动微分
import jax.numpy as jnp
from jax import grad

def energy_function(params):
    # 定义能量函数
    return compute_energy(params)

# 计算梯度
energy_grad = grad(energy_function)
gradient = energy_grad(initial_params)
```

---

## 发表论文

### 生成发表级图表

```python
# 使用预设的matplotlib样式
import matplotlib.pyplot as plt

plt.style.use('publication')  # 如果有自定义样式

# 高分辨率保存
fig, ax = plt.subplots(figsize=(6, 4))
# ... 绘图代码 ...
plt.savefig('figure1.pdf', dpi=300, bbox_inches='tight')
```

### 数据导出

```python
# 导出数据为标准格式
import pandas as pd

data = {
    'L': L_values,
    'S': S_values,
    'error': error_bars
}

df = pd.DataFrame(data)
df.to_csv('results.csv', index=False)
```

### 可重现性

```bash
# 记录完整环境
pip freeze > requirements_exact.txt

# 记录随机种子
np.random.seed(42)

# 版本控制
git tag v1.0 -m "论文提交版本"
```

---

## 故障排除

### 问题1：内存不足

**症状**：运行大系统时内存溢出

**解决方案**：
```python
# 1. 减少键维度
chi = 20  # 而不是 100

# 2. 使用迭代器而不是一次性加载
for chunk in data_chunks:
    process(chunk)

# 3. 使用内存映射
import numpy as np
data = np.memmap('large_data.dat', dtype='float64', mode='r', shape=(N, M))
```

### 问题2：收敛慢

**症状**：DMRG/CTMRG不收敛

**解决方案**：
```python
# 1. 更好的初始猜测
psi_init = construct_better_initial_state()

# 2. 调整参数
ctmrg.iterate(max_iter=200, tol=1e-6)  # 放宽容差

# 3. 使用预条件
use_preconditioner = True
```

### 问题3：数值不稳定

**症状**：NaN或Inf值出现

**解决方案**：
```python
# 1. 检查归一化
psi = psi / np.linalg.norm(psi)

# 2. 使用更高精度
dtype = np.complex128  # 而不是 complex64

# 3. 正则化
result = compute_value() + 1e-10  # 避免除零
```

---

## 研究里程碑

### 第1个月
- [ ] 完成所有tutorials
- [ ] 运行所有examples
- [ ] 通过所有tests

### 第3个月
- [ ] 独立实现一个算法
- [ ] 重现一篇论文的结果
- [ ] 开始原创研究

### 第6个月
- [ ] 发现新结果
- [ ] 撰写第一篇论文草稿
- [ ] 准备组会报告

### 第12个月
- [ ] 投稿第一篇论文
- [ ] 参加会议
- [ ] 开始新课题

---

## 资源链接

### 内部文档
- [快速开始](QUICKSTART.md)
- [项目总结](PROJECT_SUMMARY.md)
- [参考文献](BIBLIOGRAPHY.md)
- [研究路线图](RESEARCH_ROADMAP.md)

### 外部资源
- [TeNPy文档](https://tenpy.readthedocs.io/)
- [ITensor教程](https://itensor.org/docs.cgi)
- [Wen Group Papers](http://dao.mit.edu/~wen/pub.html)

---

## 贡献指南

### 添加新功能

1. 创建新分支
```bash
git checkout -b feature/my-new-feature
```

2. 实现功能并测试
```python
# 在 tests/ 中添加测试
class TestMyFeature(unittest.TestCase):
    ...
```

3. 更新文档
```markdown
# 在相应README中添加说明
```

4. 提交PR
```bash
git commit -m "Add my new feature"
git push origin feature/my-new-feature
```

---

## 联系与支持

- **Issues**: 使用GitHub Issues报告问题
- **Discussions**: 加入讨论
- **Wiki**: 查看详细文档

---

**祝研究顺利！** 🚀
