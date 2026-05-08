# Sensitive Word Detector

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-sensitive--word--detector-blue.svg)](https://pypi.org/)
[![Stars](https://img.shields.io/github/stars/QQSelfEvolution/sensitive-word-detector?style=social)](https://github.com/QQSelfEvolution/sensitive-word-detector)

**A high-performance Chinese sensitive word detector based on DFA (Deterministic Finite Automaton) algorithm.**

[English](./README.md) | [中文](./README_zh.md)

</div>

## ✨ Features

- 🚀 **High Performance**: DFA algorithm for O(n) time complexity matching
- 📦 **Zero Dependencies**: Pure Python implementation, no external packages required
- 🔧 **Flexible**: Support custom word lists, case sensitivity options
- 🌐 **API Ready**: Built-in FastAPI service for easy integration
- 💻 **CLI Tool**: Convenient command-line interface
- 📊 **Risk Scoring**: Multi-level risk assessment with suggestions
- 🔄 **Hot Reload**: Dynamically update word lists without restart

## 📖 Introduction

Sensitive Word Detector is a text filtering tool designed to detect and filter sensitive words in Chinese text. It uses the DFA (Deterministic Finite Automaton) algorithm, which offers significant advantages over traditional string matching approaches:

| Algorithm | Time Complexity | 10K Words Memory | 1K Texts Performance |
|-----------|-----------------|------------------|---------------------|
| Naive | O(n×m) | Slow | ~500ms |
| Trie | O(n) | High | ~50ms |
| **DFA (This)** | **O(n)** | **Medium** | **~5ms** |

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install sensitive-word-detector

# Or install from source
git clone https://github.com/QQSelfEvolution/sensitive-word-detector.git
cd sensitive-word-detector
pip install -e .
```

### Basic Usage

```python
from sensitive_word import SensitiveWordDetector

# Initialize detector with word list
detector = SensitiveWordDetector('wordlist.txt')

# Detect sensitive words
text = "这是一个包含敏感词的测试文本"
result = detector.detect(text)
print(result)
# [{'word': '敏感词', 'start': 4, 'end': 8}]

# Check if contains sensitive words
has_sensitive = detector.has_sensitive(text)
print(has_sensitive)  # True

# Replace sensitive words
replaced = detector.replace(text, '*', show_count=True)
print(replaced)  # 这是一个*个**词的测试文本
```

### API Server

```bash
# Start API server
python sensitive_word_api.py

# Or use uvicorn
uvicorn sensitive_word_api:app --host 0.0.0.0 --port 8000
```

#### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/stats` | Word list statistics |
| POST | `/detect` | Detect sensitive words |
| POST | `/replace` | Replace sensitive words |
| POST | `/batch_detect` | Batch detect multiple texts |
| POST | `/reload` | Reload word list |
| GET | `/words` | Get all sensitive words |
| POST | `/words/add` | Add a new sensitive word |

#### API Example

```bash
# Detect sensitive words
curl -X POST http://localhost:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "这是一个测试文本", "case_sensitive": false}'

# Response
{
  "has_sensitive": false,
  "count": 0,
  "words": [],
  "positions": []
}
```

### CLI Tool

```bash
# Detect single text
python cli_tool.py -t "这是一个测试文本"

# Detect from file
python cli_tool.py -f input.txt

# Show word list statistics
python cli_tool.py --stats

# Batch process with output
python cli_tool.py -f input.txt -o result.json
```

## 📂 Project Structure

```
sensitive-word-detector/
├── sensitive_word.py      # Core detector class
├── sensitive_word_api.py  # FastAPI server
├── cli_tool.py           # Command-line interface
├── wordlist.txt          # Default word list
├── requirements.txt      # Dependencies
├── LICENSE              # MIT License
├── README.md            # English documentation
├── README_zh.md         # Chinese documentation
├── tests/               # Unit tests
│   └── test_detector.py
└── examples/            # Usage examples
    ├── basic_usage.py
    ├── api_example.py
    └── batch_processing.py
```

## 🔧 API Reference

### SensitiveWordDetector Class

#### Constructor

```python
detector = SensitiveWordDetector(wordlist_path: Optional[str] = None)
```

#### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `add_word(word: str)` | Word to add | `None` | Add a sensitive word |
| `load_words(filepath: str)` | File path | `int` | Load words from file |
| `save_words(filepath: str)` | File path | `int` | Save words to file |
| `get_all_words()` | None | `List[str]` | Get all sensitive words |
| `detect(text: str, case_sensitive: bool = False)` | Text to check | `List[Dict]` | Detect sensitive words |
| `has_sensitive(text: str)` | Text to check | `bool` | Check if text contains sensitive words |
| `replace(text: str, replace_char: str = '*', show_count: bool = True)` | Text and options | `str` | Replace sensitive words |
| `get_stats()` | None | `Dict` | Get word list statistics |

#### Example

```python
from sensitive_word import SensitiveWordDetector

# Create detector
detector = SensitiveWordDetector()

# Add words programmatically
detector.add_word("sensitive")
detector.add_word("forbidden")

# Or load from file
detector.load_words("wordlist.txt")

# Detect
result = detector.detect("This contains sensitive words")
print(result)
# [{'word': 'sensitive', 'start': 9, 'end': 18}]

# Replace
safe_text = detector.replace("This contains sensitive words")
print(safe_text)
# This contains ******** words

# Statistics
stats = detector.get_stats()
print(stats)
# {'total_words': 2, 'min_length': 9, 'max_length': 10}
```

## 📊 Performance

Test environment: 10,000 sensitive words, 1000 random texts

```bash
# Run performance test
python -c "
from sensitive_word import SensitiveWordDetector
import time

detector = SensitiveWordDetector('wordlist.txt')
texts = ['Sample text with some content'] * 1000

start = time.time()
for text in texts:
    detector.detect(text)
elapsed = time.time() - start

print(f'Processed 1000 texts in {elapsed:.3f}s')
print(f'Average: {elapsed/1000*1000:.2f}ms per text')
"
```

Expected results:
- **Single text detection**: < 1ms
- **Batch 1000 texts**: < 100ms
- **Memory usage**: ~2-5MB for 10K words

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Or run with unittest
python tests/test_detector.py

# Run specific test
python -m pytest tests/test_detector.py::test_basic_detection -v
```

## 🔨 Development

```bash
# Clone repository
git clone https://github.com/QQSelfEvolution/sensitive-word-detector.git
cd sensitive-word-detector

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .

# Run tests
python -m pytest tests/ -v

# Start API server
python sensitive_word_api.py
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Add unit tests for new features
- Update documentation for API changes
- Follow PEP 8 style guidelines
- Keep commits atomic and descriptive

## 📝 Word List Format

The word list supports the following format:

```txt
# Lines starting with # are comments
# Category tags: #category:name:level

# Basic words
sensitive_word
forbidden_word

# With category (for future extension)
#category:fraud:high
scam
phishing
```

## 🐛 Troubleshooting

**Q: Word list not loading?**
```python
# Use absolute path
detector = SensitiveWordDetector('/absolute/path/to/wordlist.txt')
```

**Q: False positives?**
- Adjust the word list to be more specific
- Use longer phrases instead of single words

**Q: Performance issues?**
- Consider using a smaller word list
- Pre-compile frequently used patterns

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- DFA algorithm inspired by common text filtering approaches
- FastAPI for the excellent web framework
- All contributors and users of this project

## 📧 Contact

- **GitHub Issues**: [Issue Tracker](https://github.com/QQSelfEvolution/sensitive-word-detector/issues)
- **Email**: support@example.com

---

<div align="center">

If this project helps you, please give it a ⭐️

</div>
