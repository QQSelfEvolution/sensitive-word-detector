"""
Basic Usage Examples for SensitiveWordDetector
"""

from sensitive_word import SensitiveWordDetector


def basic_detection_example():
    """Basic detection example"""
    print("=" * 60)
    print("Basic Detection Example")
    print("=" * 60)
    
    # Initialize detector
    detector = SensitiveWordDetector()
    
    # Add sensitive words
    sensitive_words = ['敏感词', '违禁', '作弊', '赌博', '色情', '外挂']
    for word in sensitive_words:
        detector.add_word(word)
    
    # Test texts
    test_texts = [
        '这是一段正常的文本',
        '包含敏感词的内容',
        '使用外挂软件作弊是不对的',
        '赌博网站是违法的',
    ]
    
    for text in test_texts:
        result = detector.detect(text)
        has_sensitive = len(result) > 0
        
        print(f"\n原文: {text}")
        print(f"包含敏感词: {'是' if has_sensitive else '否'}")
        
        if result:
            words = [w['word'] for w in result]
            print(f"检测到的敏感词: {words}")


def replacement_example():
    """Word replacement example"""
    print("\n" + "=" * 60)
    print("Word Replacement Example")
    print("=" * 60)
    
    detector = SensitiveWordDetector()
    detector.add_word('敏感词')
    detector.add_word('赌博')
    
    # Original text
    text = "这是一个包含敏感词的测试，赌博网站"
    
    print(f"\n原文: {text}")
    
    # Replace with asterisk
    result = detector.replace(text, '*', show_count=True)
    print(f"替换后: {result}")
    
    # Replace with custom character
    result2 = detector.replace(text, '#', show_count=False)
    print(f"全替换: {result2}")


def wordlist_file_example():
    """Word list file operations example"""
    print("\n" + "=" * 60)
    print("Word List File Example")
    print("=" * 60)
    
    # Save current word list
    detector = SensitiveWordDetector()
    detector.add_word('词1')
    detector.add_word('词2')
    detector.add_word('词3')
    
    save_path = 'example_wordlist.txt'
    count = detector.save_words(save_path)
    print(f"\n已保存 {count} 个词到 {save_path}")
    
    # Load from file
    detector2 = SensitiveWordDetector(save_path)
    print(f"从文件加载了 {detector2.get_stats()['total_words']} 个词")
    print(f"词库内容: {detector2.get_all_words()}")
    
    # Clean up
    import os
    os.remove(save_path)
    print("已清理临时文件")


def statistics_example():
    """Statistics example"""
    print("\n" + "=" * 60)
    print("Statistics Example")
    print("=" * 60)
    
    detector = SensitiveWordDetector()
    
    # Add various words
    words = ['短', '中等词', '这是一个比较长的词组', '更长的敏感词组']
    for word in words:
        detector.add_word(word)
    
    stats = detector.get_stats()
    
    print(f"\n词库统计:")
    print(f"  总词数: {stats['total_words']}")
    print(f"  最短词: {stats['min_length']} 字")
    print(f"  最长词: {stats['max_length']} 字")


def batch_processing_example():
    """Batch processing example"""
    print("\n" + "=" * 60)
    print("Batch Processing Example")
    print("=" * 60)
    
    detector = SensitiveWordDetector()
    detector.add_word('敏感词')
    detector.add_word('违禁')
    
    # Batch of texts
    texts = [
        '正常文本1',
        '包含敏感词的内容',
        '正常文本2',
        '违禁词汇',
        '也是正常的',
    ]
    
    print("\n批量检测结果:")
    for i, text in enumerate(texts, 1):
        result = detector.detect(text)
        status = "⚠️ 有敏感词" if len(result) > 0 else "✓ 安全"
        print(f"  {i}. {status}: {text}")


def main():
    """Run all examples"""
    print("Sensitive Word Detector - Usage Examples")
    print("=" * 60)
    
    basic_detection_example()
    replacement_example()
    wordlist_file_example()
    statistics_example()
    batch_processing_example()
    
    print("\n" + "=" * 60)
    print("All examples completed!")


if __name__ == '__main__':
    main()
