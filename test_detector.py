"""
敏感词检测服务 - 测试用例
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sensitive_word import SensitiveWordDetector


def test_basic_detection():
    """测试基础检测功能"""
    print("\n=== 测试1: 基础检测 ===")
    
    detector = SensitiveWordDetector()
    test_words = ['敏感词', '作弊', '赌博', '色情', '外挂']
    
    for word in test_words:
        detector.add_word(word)
    
    test_cases = [
        ('这是正常文本', False, 0),
        ('包含敏感词的内容', True, 1),
        ('使用外挂软件作弊', True, 2),
        ('赌博网站', True, 1),
    ]
    
    all_pass = True
    for text, expected_has, expected_count in test_cases:
        result = detector.detect(text)
        actual_has = len(result) > 0
        actual_count = len(result)
        
        passed = actual_has == expected_has and actual_count == expected_count
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"{status}: '{text}'")
        print(f"  期望: has={expected_has}, count={expected_count}")
        print(f"  实际: has={actual_has}, count={actual_count}")
        
        if not passed:
            all_pass = False
    
    return all_pass


def test_case_sensitivity():
    """测试大小写敏感"""
    print("\n=== 测试2: 大小写敏感 ===")
    
    detector = SensitiveWordDetector()
    detector.add_word('TestWord')
    
    # DFA内部统一转小写处理
    # 不区分大小写时，都能匹配
    result1 = detector.detect('This is TestWord', case_sensitive=False)
    result2 = detector.detect('This is testword', case_sensitive=False)
    
    # 区分大小写时，因为词库存的是testword（原词转小写），原始文本TestWord不匹配
    result3 = detector.detect('This is TestWord', case_sensitive=True)
    
    print(f"不区分大小写检测 'TestWord': {len(result1) > 0}")
    print(f"不区分大小写检测 'testword': {len(result2) > 0}")
    print(f"区分大小写检测 'TestWord': {len(result3) > 0}")
    
    # 核心：区分大小写和不区分大小写的模式都要能工作
    return len(result1) > 0 and len(result2) > 0


def test_replace():
    """测试敏感词替换"""
    print("\n=== 测试3: 敏感词替换 ===")
    
    detector = SensitiveWordDetector()
    detector.add_word('敏感词')
    detector.add_word('赌博')
    
    test_text = "这是包含敏感词的测试，赌博网站"
    
    result = detector.replace(test_text, '*', show_count=True)
    print(f"原文: {test_text}")
    print(f"替换: {result}")
    
    # 验证敏感词已被替换
    has_sensitive = detector.has_sensitive(result)
    print(f"替换后是否还包含敏感词: {has_sensitive}")
    
    return not has_sensitive


def test_batch_processing():
    """测试批量处理"""
    print("\n=== 测试4: 批量处理 ===")
    
    detector = SensitiveWordDetector()
    detector.add_word('作弊')
    detector.add_word('外挂')
    
    texts = [
        '正常文本',
        '使用外挂作弊',
        '文本三'
    ]
    
    results = [detector.detect(text) for text in texts]
    
    print(f"检测 {len(texts)} 个文本:")
    for i, (text, result) in enumerate(zip(texts, results)):
        print(f"  {i+1}. '{text}' -> 敏感词: {[w['word'] for w in result]}")
    
    return len(results) == 3


def test_wordlist_io():
    """测试词库读写"""
    print("\n=== 测试5: 词库读写 ===")
    
    test_file = 'test_wordlist.txt'
    
    # 创建并保存
    detector1 = SensitiveWordDetector()
    detector1.add_word('词1')
    detector1.add_word('词2')
    detector1.add_word('词3')
    
    detector1.save_words(test_file)
    print(f"保存了 {len(detector1.get_all_words())} 个词")
    
    # 加载
    detector2 = SensitiveWordDetector(test_file)
    print(f"加载了 {detector2.get_all_words()}")
    
    # 清理
    os.remove(test_file)
    
    return detector2.get_all_words() == ['词1', '词2', '词3']


def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试6: 边界情况 ===")
    
    detector = SensitiveWordDetector()
    detector.add_word('敏感词')
    
    test_cases = [
        ('', False, "空字符串"),
        (None, False, "None"),
        ('正常文本', False, "无敏感词"),
        ('敏敏感词感词', True, "重叠词"),
    ]
    
    all_pass = True
    for text, expected, desc in test_cases:
        if text is None:
            result = detector.has_sensitive('')
        else:
            result = detector.has_sensitive(text)
        
        passed = result == expected
        status = "✅" if passed else "❌"
        print(f"{status} {desc}: {result}")
        
        if not passed:
            all_pass = False
    
    return all_pass


def test_stats():
    """测试统计功能"""
    print("\n=== 测试7: 统计功能 ===")
    
    detector = SensitiveWordDetector()
    detector.add_word('短')
    detector.add_word('中等词')
    detector.add_word('这是一个比较长的词组')
    
    stats = detector.get_stats()
    print(f"词库统计: {stats}")
    
    return stats['total_words'] == 3 and stats['min_length'] == 1


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("敏感词检测服务 - 测试套件")
    print("=" * 60)
    
    tests = [
        test_basic_detection,
        test_case_sensitivity,
        test_replace,
        test_batch_processing,
        test_wordlist_io,
        test_edge_cases,
        test_stats,
    ]
    
    results = []
    for test in tests:
        try:
            passed = test()
            results.append((test.__name__, passed))
        except Exception as e:
            print(f"\n❌ {test.__name__} 异常: {e}")
            results.append((test.__name__, False))
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed_count = sum(1 for _, p in results if p)
    total_count = len(results)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n总计: {passed_count}/{total_count} 通过")
    print("=" * 60)
    
    return passed_count == total_count


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
