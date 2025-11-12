# 项目5: 弦网液体的TN实现

## 目标

用张量网络编码**Wen的弦网凝聚态**，实现任意子物理。

## 理论基础

**Levin-Wen模型** (基于融合范畴)

```
H = -Σ_{vertices} Q_v - Σ_{plaquettes} B_p
```

输入: 融合范畴 𝒞 (如Fibonacci)

## 融合范畴示例

### Fibonacci Anyon
```
τ × τ = 1 + τ
```

量子维数: d_τ = φ = (1+√5)/2

### F-符号
```
     j          k
     |          |
  i--●--l = Σ  F^{ij}_{kl;m} i--●--l
     |    m         |
     k              j
```

## 任务清单

- [ ] 编码融合规则到张量
- [ ] 构建弦网PEPS
- [ ] 计算地面态简并
- [ ] 实现任意子激发
- [ ] 模拟编织过程
- [ ] 研究任意子凝聚相变

## 创新点

1. **自动微分优化F-符号**
2. **可调融合范畴**
3. **数值验证模型独立性**

## 实现策略

```python
class FusionCategory:
    def __init__(self, fusion_rules, F_symbols):
        self.N = fusion_rules  # N^k_{ij}
        self.F = F_symbols     # F矩阵

    def check_pentagon(self):
        # 验证五边形方程
        pass
```

## 预期突破

- 首次完整TN实现弦网液体
- 任意子统计数值验证
- **论文**: *Nature Physics*

## Wen组核心方向

直接对接XG Wen的理论工作！

## 参考文献

- Levin & Wen, *Phys. Rev. B 71, 045110 (2005)*
- Buerschaper et al., *Ann. Phys. 351, 447 (2014)*

---

**难度**: ⭐⭐⭐⭐⭐ | **时间**: 6-8个月 | **产出**: Nature Physics潜力
