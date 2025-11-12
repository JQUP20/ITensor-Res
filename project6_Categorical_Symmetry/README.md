# 项目6: 范畴对称的张量网络表示

## 目标

将**范畴对称**嵌入张量网络，研究**非可逆缺陷**。

## 理论背景

**Wen 2020+**: 对称 = 高维拓扑序边界

```
Symmetry ≡ Topological order in one-higher dimension
```

## 核心概念

### 融合高阶范畴
- 0-form对称: 群作用
- 1-form对称: 弦算符
- 2-category: 缺陷融合

### 非可逆对称
```
A × B ≠ B × A  (braiding)
A × A ≠ 1      (non-invertible)
```

## 任务清单

- [ ] 构建fusion 2-category
- [ ] 定义缺陷线为TN指标
- [ ] 计算缺陷融合规则
- [ ] 验证异常匹配
- [ ] 研究对称破缺机制
- [ ] 连接到SymTFT

## 示例系统

### ℤ₂ 1-form对称
```
2D Ising ←→ 2D Ising dual
```

缺陷线: Kramers-Wannier对偶墙

### 代数框架
```python
class CategoricalSymmetry:
    def __init__(self, category):
        self.objects = category.objects
        self.morphisms = category.morphisms
        self.F_symbols = category.F_moves

    def defect_fusion(self, D1, D2):
        # 计算缺陷融合
        return fusion_result
```

## 前沿方向

- SymTFT (Symmetry Topological Field Theory)
- 非可逆对称破缺
- 异常边界理论

## 博士论文级工作

这是**核心创新**，直接推进Wen组前沿！

## 预期成果

- 博士论文第一章
- 投稿 *Reviews of Modern Physics*
- 多篇PRL/PRB

## 参考文献

- Wen, *Phys. Rev. Research 5, 033118 (2023)*
- Kong et al., *arXiv:2307.xxxxx*
- Bhardwaj et al., *SciPost Phys. 14, 007 (2023)*

---

**难度**: ⭐⭐⭐⭐⭐ | **时间**: 8-12个月 | **产出**: 博士论文 + RMP
