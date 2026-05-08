"""
敏感词检测器 - DFA算法实现
基于确定有限自动机的高效敏感词匹配
"""

import re
from typing import List, Dict, Set, Optional
from pathlib import Path


class SensitiveWordDetector:
    """敏感词检测器"""
    
    def __init__(self, wordlist_path: Optional[str] = None):
        """
        初始化敏感词检测器
        
        Args:
            wordlist_path: 敏感词库文件路径
        """
        self.word_dict: Dict = {}  # DFA词库树
        self.min_match_len = float('inf')  # 最短匹配长度
        self.max_match_len = 0  # 最长匹配长度
        
        if wordlist_path:
            self.load_words(wordlist_path)
    
    def add_word(self, word: str) -> None:
        """
        添加敏感词到DFA树
        
        Args:
            word: 敏感词
        """
        if not word or not word.strip():
            return
        
        word = word.strip().lower()  # 统一转小写
        current_dict = self.word_dict
        
        for char in word:
            if char not in current_dict:
                current_dict[char] = {'is_end': False}
            current_dict = current_dict[char]
        
        current_dict['is_end'] = True
        self.max_match_len = max(self.max_match_len, len(word))
        self.min_match_len = min(self.min_match_len, len(word))
    
    def load_words(self, filepath: str) -> int:
        """
        从文件加载敏感词库
        
        Args:
            filepath: 词库文件路径
            
        Returns:
            加载的词数
        """
        self.word_dict = {}
        self.min_match_len = float('inf')
        self.max_match_len = 0
        
        count = 0
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word and not word.startswith('#'):  # 跳过空行和注释
                        self.add_word(word)
                        count += 1
        except FileNotFoundError:
            print(f"词库文件不存在: {filepath}")
        
        return count
    
    def save_words(self, filepath: str) -> int:
        """
        保存词库到文件
        
        Args:
            filepath: 保存路径
            
        Returns:
            保存的词数
        """
        words = self.get_all_words()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(words))
        return len(words)
    
    def get_all_words(self) -> List[str]:
        """获取所有敏感词"""
        words = []
        
        def _search(d, path):
            for char, next_dict in d.items():
                if char == 'is_end':
                    continue
                new_path = path + char
                if next_dict.get('is_end'):
                    words.append(new_path)
                _search(next_dict, new_path)
        
        _search(self.word_dict, '')
        return words
    
    def detect(self, text: str, case_sensitive: bool = False) -> List[Dict]:
        """
        检测文本中的敏感词
        
        Args:
            text: 待检测文本
            case_sensitive: 是否区分大小写
            
        Returns:
            检测到的敏感词列表 [{'word': '敏感词', 'start': 0, 'end': 3}, ...]
        """
        if not text:
            return []
        
        # 统一转小写进行匹配
        check_text = text.lower() if not case_sensitive else text
        
        found_words = []
        text_len = len(check_text)
        
        # 滑动窗口，从短到长匹配
        for start in range(text_len):
            current_dict = self.word_dict
            match_end = start
            
            for i in range(start, text_len):
                char = check_text[i]
                
                if char not in current_dict:
                    break
                
                current_dict = current_dict[char]
                match_end = i + 1
                
                # 遇到词尾，记录匹配
                if current_dict.get('is_end'):
                    word = text[start:match_end] if case_sensitive else text[start:match_end]
                    found_words.append({
                        'word': word,
                        'start': start,
                        'end': match_end
                    })
        
        # 去重并按位置排序
        seen = set()
        unique_words = []
        for w in found_words:
            key = (w['word'], w['start'])
            if key not in seen:
                seen.add(key)
                unique_words.append(w)
        
        return sorted(unique_words, key=lambda x: x['start'])
    
    def has_sensitive(self, text: str) -> bool:
        """
        检查是否包含敏感词
        
        Args:
            text: 待检测文本
            
        Returns:
            是否包含敏感词
        """
        return len(self.detect(text)) > 0
    
    def replace(self, text: str, replace_char: str = '*', show_count: bool = True) -> str:
        """
        替换文本中的敏感词
        
        Args:
            text: 待处理文本
            replace_char: 替换字符
            show_count: 是否显示字数
            
        Returns:
            替换后的文本
        """
        if not text:
            return text
        
        words = self.detect(text)
        if not words:
            return text
        
        result = list(text)
        
        # 从后往前替换，避免位置偏移
        for word_info in reversed(words):
            start, end = word_info['start'], word_info['end']
            word_len = end - start
            
            if show_count:
                result[start:start + 1] = [replace_char] * min(word_len, 1)
                if word_len > 1:
                    result[start + 1:end] = [replace_char] * (word_len - 1)
            else:
                result[start:end] = [replace_char] * word_len
        
        return ''.join(result)
    
    def get_stats(self) -> Dict:
        """获取词库统计信息"""
        return {
            'total_words': len(self.get_all_words()),
            'min_length': self.min_match_len if self.min_match_len != float('inf') else 0,
            'max_length': self.max_match_len
        }


# 单元测试
if __name__ == '__main__':
    # 创建检测器
    detector = SensitiveWordDetector()
    
    # 添加测试敏感词
    test_words = ['敏感词', '违禁', '作弊', '作弊软件', '赌博', '色情']
    for word in test_words:
        detector.add_word(word)
    
    print(f"词库统计: {detector.get_stats()}")
    
    # 测试检测
    test_texts = [
        '这是一个正常的测试文本',
        '包含敏感词的内容',
        '这是一个作弊软件的广告',
        '含有赌博信息的链接',
    ]
    
    print("\n=== 敏感词检测测试 ===")
    for text in test_texts:
        result = detector.detect(text)
        has = len(result) > 0
        print(f"\n文本: {text}")
        print(f"包含敏感词: {has}")
        if result:
            print(f"检测到: {[w['word'] for w in result]}")
    
    # 测试替换
    print("\n=== 敏感词替换测试 ===")
    test_text = "这是一个包含敏感词的测试"
    print(f"原文: {test_text}")
    print(f"替换: {detector.replace(test_text)}")
