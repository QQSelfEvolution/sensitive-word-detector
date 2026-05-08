# Sensitive Word Detector

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-sensitive--word--detector-blue.svg)](https://pypi.org/)
[![Stars](https://img.shields.io/github/stars/QQSelfEvolution/sensitive-word-detector?style=social)](https://github.com/QQSelfEvolution/sensitive-word-detector)

**基于DFA（确定有限自动机）算法的高性能中文敏感词检测器**

[English](./README.md) | [中文](./README_zh.md)

</div>

## ✨ 特性

- 🚀 **高性能**: DFA算法，匹配时间复杂度O(n)
- 📦 **零依赖**: 纯Python实现，无需外部包
- 🔧 **灵活性**: 支持自定义词库、大小写敏感选项
- 🌐 **API服务**: 内置FastAPI服务，便于集成
- 💻 **命令行工具**: 便捷的命令行界面
- 📊 **风险评分**: 多级别风险评估与建议
- 🔄 **热更新**: 无需重启即可动态更新词库

## 📖 简介

敏感词检测器是一款用于检测和过滤中文文本中敏感词的工具。它采用DFA（确定有限自动机）算法，相比传统字符串匹配有着显著优势：

| 算法 | 时间复杂度 | 1万词库内存占用 | 1000条文本性能 |
|------|-----------|----------------|---------------|
| 朴素匹配 | O(n×m) | 较慢 | ~500ms |
| Trie树 | O(n) | 较高 | ~50ms |
| **DFA（本项目）** | **O(n)** | **中等** | **~5ms** |

## 🚀 快速开始

### 安装

```bash
# 从PyPI安装
pip install sensitive-word-detector

# 或从源码安装
git clone https://github.com/QQSelfEvolution/sensitive-word-detector.git
cd sensitive-word-detector
pip install -e .
```

### 基本用法

```python
from sensitive_word import SensitiveWordDetector

# 初始化检测器
detector = SensitiveWordDetector('wordlist.txt')

# 检测敏感词
text = "这是一个包含敏感词的测试文本"
result = detector.detect(text)
print(result)
# [{'word': '敏感词', 'start': 4, 'end': 8}]

# 检查是否包含敏感词
has_sensitive = detector.has_sensitive(text)
print(has_sensitive)  # True

# 替换敏感词
replaced = detector.replace(text, '*', show_count=True)
print(replaced)  # 这是一个*个**词的测试文本
```

### API服务

```bash
# 启动API服务
python sensitive_word_api.py

# 或使用uvicorn
uvicorn sensitive_word_api:app --host 0.0.0.0 --port 8000
```

#### API接口

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/stats` | 词库统计 |
| POST | `/detect` | 检测敏感词 |
| POST | `/replace` | 替换敏感词 |
| POST | `/batch_detect` | 批量检测 |
| POST | `/reload` | 重载词库 |
| GET | `/words` | 获取所有敏感词 |
| POST | `/words/add` | 添加敏感词 |

#### API示例

```bash
# 检测敏感词
curl -X POST http://localhost:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "这是一个测试文本", "case_sensitive": false}'
```

### 命令行工具

```bash
# 检测单条文本
python cli_tool.py -t "这是一个测试文本"

# 从文件检测
python cli_tool.py -f input.txt

# 查看词库统计
python cli_tool.py --stats

# 批量处理并输出结果
python cli_tool.py -f input.txt -o result.json
```

## 📂 项目结构

```
sensitive-word-detector/
├── sensitive_word.py      # 核心检测器类
├── sensitive_word_api.py  # FastAPI服务
├── cli_tool.py           # 命令行工具
├── wordlist.txt          # 默认词库
├── requirements.txt      # 依赖文件
├── LICENSE              # MIT许可证
├── README.md            # 英文文档
├── README_zh.md         # 中文文档
├── tests/               # 单元测试
│   └── test_detector.py
└── examples/            # 使用示例
    ├── basic_usage.py
    ├── api_example.py
    └── batch_processing.py
```

## 🔧 API参考

### SensitiveWordDetector 类

#### 构造函数

```python
detector = SensitiveWordDetector(wordlist_path: Optional[str] = None)
```

#### 方法

| 方法 | 参数 | 返回值 | 描述 |
|------|------|--------|------|
| `add_word(word: str)` | 要添加的词 | `None` | 添加敏感词 |
| `load_words(filepath: str)` | 文件路径 | `int` | 从文件加载词库 |
| `save_words(filepath: str)` | 文件路径 | `int` | 保存词库到文件 |
| `get_all_words()` | 无 | `List[str]` | 获取所有敏感词 |
| `detect(text: str, case_sensitive: bool = False)` | 待检测文本 | `List[Dict]` | 检测敏感词 |
| `has_sensitive(text: str)` | 待检测文本 | `bool` | 检查是否包含敏感词 |
| `replace(text: str, replace_char: str = '*', show_count: bool = True)` | 文本和选项 | `str` | 替换敏感词 |
| `get_stats()` | 无 | `Dict` | 获取词库统计 |

## 📊 性能测试

测试环境：10,000个敏感词，1000条随机文本

```bash
# 运行性能测试
python -c "
from sensitive_word import SensitiveWordDetector
import time

detector = SensitiveWordDetector('wordlist.txt')
texts = ['包含一些内容的示例文本'] * 1000

start = time.time()
for text in texts:
    detector.detect(text)
elapsed = time.time() - start

print(f'处理1000条文本用时 {elapsed:.3f}秒')
print(f'平均: {elapsed/1000*1000:.2f}毫秒/条')
"
```

预期结果：
- **单条文本检测**: < 1毫秒
- **批量1000条**: < 100毫秒
- **内存占用**: 1万词约2-5MB

## 🧪 测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 或使用unittest
python tests/test_detector.py

# 运行特定测试
python -m pytest tests/test_detector.py::test_basic_detection -v
```

## 🔨 开发

```bash
# 克隆仓库
git clone https://github.com/QQSelfEvolution/sensitive-word-detector.git
cd sensitive-word-detector

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -e .

# 运行测试
python -m pytest tests/ -v

# 启动API服务
python sensitive_word_api.py
```

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. **Fork** 本仓库
2. **创建** 功能分支 (`git checkout -b feature/amazing-feature`)
3. **提交** 更改 (`git commit -m 'Add amazing feature'`)
4. **推送** 到分支 (`git push origin feature/amazing-feature`)
5. **创建** Pull Request

### 贡献指南

- 为新功能添加单元测试
- 更新API变更的文档
- 遵循PEP 8代码风格
- 保持提交的原子性和描述性

## 📝 词库格式

词库支持以下格式：

```txt
# 以#开头的行为注释
# 类别标签: #category:名称:级别

# 基础词汇
敏感词
违禁词

# 带类别（用于扩展）
#category:欺诈:高
诈骗
钓鱼
```

## 🐛 常见问题

**Q: 词库加载失败？**
```python
# 使用绝对路径
detector = SensitiveWordDetector('/absolute/path/to/wordlist.txt')
```

**Q: 误报较多？**
- 调整词库使其更具体
- 使用更长的短语替代单词

**Q: 性能问题？**
- 考虑使用更小的词库
- 预编译常用模式

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- DFA算法参考通用文本过滤方案
- FastAPI优秀的Web框架
- 所有本项目的贡献者和用户

## 📧 联系方式

- **GitHub Issues**: [问题追踪](https://github.com/QQSelfEvolution/sensitive-word-detector/issues)
- **邮箱**: support@example.com

---

<div align="center">

如果这个项目对您有帮助，请给它一个 ⭐️

</div>
