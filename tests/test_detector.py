"""
Unit Tests for SensitiveWordDetector
High-quality test suite with comprehensive coverage
"""

import os
import sys
import unittest
from typing import List

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensitive_word import SensitiveWordDetector


class TestSensitiveWordDetector(unittest.TestCase):
    """Test suite for SensitiveWordDetector class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = SensitiveWordDetector()
        self.test_words = ['敏感词', '作弊', '赌博', '色情', '外挂', '诈骗']
        for word in self.test_words:
            self.detector.add_word(word)
    
    def tearDown(self):
        """Clean up after tests"""
        # Remove any test files created
        test_files = ['test_wordlist.txt', 'test_output.txt']
        for f in test_files:
            if os.path.exists(f):
                os.remove(f)
    
    # ============ Basic Detection Tests ============
    
    def test_basic_detection(self):
        """Test basic sensitive word detection"""
        test_cases = [
            ('这是正常文本', False, 0),
            ('包含敏感词的内容', True, 1),
            ('使用外挂软件作弊', True, 2),
            ('赌博网站诈骗', True, 2),
        ]
        
        for text, expected_has, expected_count in test_cases:
            result = self.detector.detect(text)
            actual_has = len(result) > 0
            actual_count = len(result)
            
            with self.subTest(text=text):
                self.assertEqual(actual_has, expected_has, 
                    f"has_sensitive mismatch for '{text}'")
                self.assertEqual(actual_count, expected_count,
                    f"count mismatch for '{text}'")
    
    def test_no_false_positives(self):
        """Test that normal text doesn't trigger false positives"""
        normal_texts = [
            '今天天气真好',
            'Python是一门很好的编程语言',
            '开源项目让世界更美好',
            '学习算法和数据结构很重要',
            '',
        ]
        
        for text in normal_texts:
            with self.subTest(text=text):
                result = self.detector.detect(text)
                self.assertEqual(len(result), 0,
                    f"False positive for normal text: '{text}'")
    
    def test_partial_match_prevention(self):
        """Test that partial matches don't cause issues"""
        # Word containing sensitive word as substring but not equal
        self.detector.add_word('测试')
        result = self.detector.detect('这是一个测试用例')
        # Should match '测试' at position
        self.assertTrue(len(result) > 0)
        self.assertEqual(result[0]['word'], '测试')
    
    # ============ Case Sensitivity Tests ============
    
    def test_case_sensitivity_default(self):
        """Test case sensitivity by default (insensitive)"""
        detector = SensitiveWordDetector()
        detector.add_word('TestWord')
        
        # Default: case insensitive
        result1 = detector.detect('This is TestWord')
        result2 = detector.detect('This is testword')
        
        self.assertTrue(len(result1) > 0, "Should detect 'TestWord'")
        self.assertTrue(len(result2) > 0, "Should detect 'testword'")
    
    # ============ Replacement Tests ============
    
    def test_replace_basic(self):
        """Test basic word replacement"""
        text = "这是一个包含敏感词的测试"
        result = self.detector.replace(text, '*', show_count=True)
        
        # Sensitive word should be replaced
        self.assertNotIn('敏感词', result)
        self.assertIn('*', result)
    
    def test_replace_no_show_count(self):
        """Test replacement without showing count"""
        text = "敏感词"
        result = self.detector.replace(text, '*', show_count=False)
        
        self.assertEqual(result, '***')
    
    def test_replace_show_count(self):
        """Test replacement with count shown"""
        text = "敏感词"
        result = self.detector.replace(text, '*', show_count=True)
        
        self.assertEqual(result, '*')
    
    def test_replace_preserves_surrounding(self):
        """Test that replacement preserves surrounding text"""
        text = "前缀敏感词后缀"
        result = self.detector.replace(text)
        
        self.assertTrue(result.startswith('前缀'))
        self.assertTrue(result.endswith('后缀'))
        self.assertNotIn('敏感词', result)
    
    def test_replace_multiple_words(self):
        """Test replacing multiple different words"""
        text = "赌博和作弊都是违规行为"
        result = self.detector.replace(text)
        
        # Both words should be replaced
        self.assertNotIn('赌博', result)
        self.assertNotIn('作弊', result)
    
    def test_replace_no_sensitive_words(self):
        """Test replacing text with no sensitive words"""
        text = "这是一段正常文本"
        result = self.detector.replace(text)
        
        self.assertEqual(result, text)
    
    # ============ Has Sensitive Tests ============
    
    def test_has_sensitive_true(self):
        """Test has_sensitive returns True when sensitive word present"""
        self.assertTrue(self.detector.has_sensitive('包含敏感词的文本'))
    
    def test_has_sensitive_false(self):
        """Test has_sensitive returns False when no sensitive word"""
        self.assertFalse(self.detector.has_sensitive('这是一段正常文本'))
    
    def test_has_sensitive_empty(self):
        """Test has_sensitive with empty text"""
        self.assertFalse(self.detector.has_sensitive(''))
    
    # ============ Word List Management Tests ============
    
    def test_add_word(self):
        """Test adding words programmatically"""
        detector = SensitiveWordDetector()
        detector.add_word('新词')
        
        self.assertTrue(detector.has_sensitive('新词'))
    
    def test_add_empty_word(self):
        """Test adding empty word is handled gracefully"""
        detector = SensitiveWordDetector()
        detector.add_word('')
        detector.add_word('   ')
        
        # Should not raise error
        self.assertEqual(detector.get_stats()['total_words'], 0)
    
    def test_get_all_words(self):
        """Test getting all sensitive words"""
        words = self.detector.get_all_words()
        
        self.assertIsInstance(words, list)
        for word in self.test_words:
            self.assertIn(word, words)
    
    def test_save_and_load_words(self):
        """Test saving and loading word list"""
        # Create detector with words
        detector1 = SensitiveWordDetector()
        detector1.add_word('词1')
        detector1.add_word('词2')
        detector1.add_word('词3')
        
        # Save to file
        test_file = 'test_wordlist.txt'
        detector1.save_words(test_file)
        
        # Load into new detector
        detector2 = SensitiveWordDetector(test_file)
        
        # Verify
        self.assertEqual(len(detector2.get_all_words()), 3)
        self.assertIn('词1', detector2.get_all_words())
        
        # Cleanup
        os.remove(test_file)
    
    def test_load_from_file(self):
        """Test loading words from existing file"""
        # Create a test wordlist file
        test_file = 'test_wordlist.txt'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('# Test wordlist\n')
            f.write('加载词\n')
            f.write('测试词\n')
        
        detector = SensitiveWordDetector(test_file)
        words = detector.get_all_words()
        
        self.assertEqual(len(words), 2)
        self.assertIn('加载词', words)
        
        os.remove(test_file)
    
    def test_load_with_comments(self):
        """Test loading wordlist with comments and empty lines"""
        test_file = 'test_wordlist.txt'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('# Comment line\n')
            f.write('\n')  # Empty line
            f.write('有效词\n')
            f.write('# Another comment\n')
            f.write('另一个词\n')
        
        detector = SensitiveWordDetector(test_file)
        words = detector.get_all_words()
        
        self.assertEqual(len(words), 2)
        self.assertNotIn('# Comment line', words)
        
        os.remove(test_file)
    
    # ============ Statistics Tests ============
    
    def test_get_stats(self):
        """Test getting word list statistics"""
        detector = SensitiveWordDetector()
        detector.add_word('短')
        detector.add_word('中等词')
        detector.add_word('这是一个比较长的词组')
        
        stats = detector.get_stats()
        
        self.assertEqual(stats['total_words'], 3)
        self.assertEqual(stats['min_length'], 2)  # '短' is 1 char
        self.assertGreater(stats['max_length'], 5)
    
    def test_stats_empty_detector(self):
        """Test statistics for empty detector"""
        detector = SensitiveWordDetector()
        stats = detector.get_stats()
        
        self.assertEqual(stats['total_words'], 0)
        self.assertEqual(stats['min_length'], 0)
        self.assertEqual(stats['max_length'], 0)
    
    # ============ Position Detection Tests ============
    
    def test_detect_position(self):
        """Test that detection returns correct positions"""
        text = "前缀敏感词后缀"
        result = self.detector.detect(text)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['word'], '敏感词')
        self.assertEqual(result[0]['start'], 2)
        self.assertEqual(result[0]['end'], 5)
    
    def test_detect_multiple_positions(self):
        """Test detecting multiple sensitive words at different positions"""
        text = "赌博在开头敏感词在中间"
        result = self.detector.detect(text)
        
        self.assertEqual(len(result), 2)
        # Should be sorted by position
        self.assertEqual(result[0]['word'], '赌博')
        self.assertEqual(result[1]['word'], '敏感词')
    
    def test_detect_start_position(self):
        """Test detecting sensitive word at start of text"""
        text = "敏感词在开头"
        result = self.detector.detect(text)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['start'], 0)
    
    def test_detect_end_position(self):
        """Test detecting sensitive word at end of text"""
        text = "在结尾敏感词"
        result = self.detector.detect(text)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['end'], len(text))
    
    # ============ Edge Cases ============
    
    def test_empty_text(self):
        """Test with empty text"""
        result = self.detector.detect('')
        self.assertEqual(result, [])
    
    def test_unicode_handling(self):
        """Test handling of Unicode characters"""
        text = "中文敏感词 English test 数字123"
        self.assertEqual(len(self.detector.detect(text)), 1)
    
    def test_overlapping_sensitive_words(self):
        """Test text with overlapping sensitive words"""
        detector = SensitiveWordDetector()
        detector.add_word('敏感')
        detector.add_word('敏感词')
        
        text = "敏感词测试"
        result = detector.detect(text)
        
        # Should detect both
        words_found = [r['word'] for r in result]
        self.assertIn('敏感', words_found)
        self.assertIn('敏感词', words_found)
    
    def test_chinese_punctuation(self):
        """Test handling of Chinese punctuation"""
        text = "敏感词，测试！敏感词？"
        result = self.detector.detect(text)
        
        # Should detect both occurrences
        self.assertEqual(len(result), 2)
    
    def test_repeated_sensitive_word(self):
        """Test detecting repeated same sensitive word"""
        text = "敏感词敏感词敏感词"
        result = self.detector.detect(text)
        
        # Should detect all occurrences
        self.assertEqual(len(result), 3)
    
    # ============ Integration Tests ============
    
    def test_full_workflow(self):
        """Test complete workflow: create, add, detect, replace, save"""
        # Create detector
        detector = SensitiveWordDetector()
        
        # Add words
        detector.add_word('敏感词')
        detector.add_word('违禁')
        
        # Detect
        text = "这是包含敏感词的测试"
        has = detector.has_sensitive(text)
        self.assertTrue(has)
        
        # Replace
        safe_text = detector.replace(text)
        self.assertNotIn('敏感词', safe_text)
        
        # Verify replaced text is safe
        self.assertFalse(detector.has_sensitive(safe_text))
    
    def test_file_based_workflow(self):
        """Test workflow using file-based word list"""
        # Create wordlist file
        test_file = 'test_wordlist.txt'
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write('文件词1\n')
            f.write('文件词2\n')
        
        # Create detector from file
        detector = SensitiveWordDetector(test_file)
        
        # Verify loaded
        self.assertEqual(detector.get_stats()['total_words'], 2)
        
        # Detect
        self.assertTrue(detector.has_sensitive('这是文件词1的内容'))
        
        # Add more words
        detector.add_word('动态词')
        
        # Verify both exist
        words = detector.get_all_words()
        self.assertEqual(len(words), 3)
        
        # Save
        output_file = 'test_output.txt'
        detector.save_words(output_file)
        
        # Verify saved
        with open(output_file, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        self.assertIn('文件词1', saved_content)
        
        # Cleanup
        os.remove(test_file)
        os.remove(output_file)


class TestEdgeCases(unittest.TestCase):
    """Additional edge case tests"""
    
    def test_very_long_text(self):
        """Test with very long text"""
        detector = SensitiveWordDetector()
        detector.add_word('敏感')
        
        # Create 10000 character text with sensitive word in middle
        text = 'a' * 5000 + '敏感' + 'a' * 5000
        result = detector.detect(text)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['start'], 5000)
    
    def test_very_long_word(self):
        """Test with very long sensitive word"""
        detector = SensitiveWordDetector()
        long_word = '敏感' + '词' * 1000
        detector.add_word(long_word)
        
        text = '前缀' + long_word + '后缀'
        result = detector.detect(text)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['word'], long_word)
    
    def test_special_characters(self):
        """Test handling of special characters"""
        detector = SensitiveWordDetector()
        detector.add_word('敏感')
        
        text = "敏感！@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = detector.detect(text)
        
        self.assertEqual(len(result), 1)
    
    def test_mixed_chinese_english(self):
        """Test mixed Chinese and English text"""
        detector = SensitiveWordDetector()
        detector.add_word('敏感词')
        
        text = "Chinese敏感词English测试"
        result = detector.detect(text)
        
        self.assertEqual(len(result), 1)
    
    def test_whitespace_handling(self):
        """Test handling of various whitespace"""
        detector = SensitiveWordDetector()
        detector.add_word('敏感词')
        
        texts = [
            "敏感词 with space",
            "敏感词\twith tab",
            "敏感词\nwith newline",
            " 敏感词 with padding ",
        ]
        
        for text in texts:
            with self.subTest(text=text):
                result = detector.detect(text)
                self.assertGreater(len(result), 0)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
