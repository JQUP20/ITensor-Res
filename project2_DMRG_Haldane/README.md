# 项目2: DMRG精确求解Haldane链

## 目标

使用密度矩阵重整化群(DMRG)算法验证**SPT相的边缘四重简并**。

## 研究系统

**自旋-1 AKLT链** (Affleck-Kennedy-Lieb-Tasaki Chain)

```
H = Σᵢ [𝐒ᵢ·𝐒ᵢ₊₁ + (1/3)(𝐒ᵢ·𝐒ᵢ₊₁)²]
```

## 核心物理

- **Haldane相**: 对称保护拓扑(SPT)相
- **边缘态**: 开放边界下四重简并
- **弦序参数**: 长程拓扑序参数 O_z(i,j) → 0.374

## 任务清单

- [ ] 实现自旋-1算符
- [ ] 构建AKLT哈密顿量MPO
- [ ] DMRG优化基态
- [ ] 计算能量谱(开放/周期边界)
- [ ] 验证四重简并
- [ ] 计算弦序参数
- [ ] 研究对称破缺场效应

## 关键代码

```python
# TeNPy实现
from tenpy.models.spins import SpinChain

model_params = {
    'L': 40,
    'S': 1.0,  # 自旋-1
    'bc_MPS': 'finite',
    'Jx': 1.0, 'Jy': 1.0, 'Jz': 1.0,
    'biquadratic': 1.0/3.0  # AKLT项
}
```

## 预期结果

1. **开放边界**: 4个简并基态 (拓扑保护)
2. **弦序参数**: O_z → 0.374
3. **纠缠谱**: 双重简并

## 参考文献

- Affleck et al., *Phys. Rev. Lett. 59, 799 (1987)*
- Pollmann et al., *Phys. Rev. B 81, 064439 (2010)*

---

**难度**: ⭐⭐⭐☆☆ | **时间**: 2-3个月 | **产出**: PRB短文
