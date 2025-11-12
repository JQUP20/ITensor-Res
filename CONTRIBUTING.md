# 贡献指南

感谢你对本项目感兴趣！本文档说明如何为项目做出贡献。

## 行为准则

- 尊重所有贡献者
- 建设性讨论
- 专注于科学严谨性

## 如何贡献

### 报告Bug

提交Issue时请包含:
1. 问题描述
2. 复现步骤
3. 预期 vs 实际行为
4. 环境信息 (Python版本, 操作系统等)

### 建议新功能

提交Issue说明:
1. 功能描述
2. 使用场景
3. 可能的实现方法

### 提交代码

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. Push到分支 (`git push origin feature/amazing-feature`)
5. 开启Pull Request

### 代码规范

**Python:**
- 遵循PEP 8
- 使用Black格式化
- 添加类型注解
- 编写docstrings

**C++:**
- 遵循ITensor风格
- 添加注释
- 使用有意义的变量名

### 测试

- 添加单元测试
- 确保所有测试通过: `pytest`

## 项目结构

```
ITensor-Res/
├── project{1-6}*/     # 各研究项目
├── common/            # 共享代码
├── docs/              # 文档
└── scripts/           # 工具脚本
```

## 开发设置

```bash
# 安装开发依赖
pip install -r requirements.txt
pip install pytest black flake8

# 运行测试
pytest

# 代码检查
black .
flake8 .
```

## 文档

- 代码中添加清晰注释
- 更新相关README
- 必要时添加Jupyter notebook示例

## 联系方式

问题或建议? 联系项目维护者或提交Issue。

感谢你的贡献! 🙏
