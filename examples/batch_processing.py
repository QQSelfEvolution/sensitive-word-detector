"""
Batch Processing Examples for SensitiveWordDetector
"""

from sensitive_word import SensitiveWordDetector
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
import time


def batch_detect_simple(texts: List[str], wordlist_path: str = None) -> List[Dict]:
    """
    Simple batch detection
    
    Args:
        texts: List of texts to check
        wordlist_path: Path to word list file
        
    Returns:
        List of detection results
    """
    detector = SensitiveWordDetector(wordlist_path) if wordlist_path else SensitiveWordDetector()
    
    results = []
    for text in texts:
        result = detector.detect(text)
        results.append({
            'text': text,
            'has_sensitive': len(result) > 0,
            'words': result
        })
    
    return results


def batch_detect_with_stats(texts: List[str]) -> Dict:
    """
    Batch detection with statistics
    
    Args:
        texts: List of texts to check
        
    Returns:
        Dictionary with results and statistics
    """
    detector = SensitiveWordDetector()
    detector.add_word('敏感词')
    detector.add_word('违禁')
    detector.add_word('作弊')
    detector.add_word('赌博')
    detector.add_word('色情')
    detector.add_word('外挂')
    
    start_time = time.time()
    
    results = []
    safe_count = 0
    risky_count = 0
    all_sensitive_words = set()
    
    for text in texts:
        detected = detector.detect(text)
        
        if detected:
            risky_count += 1
            for w in detected:
                all_sensitive_words.add(w['word'])
        else:
            safe_count += 1
        
        results.append({
            'text': text[:50] + '...' if len(text) > 50 else text,
            'has_sensitive': len(detected) > 0,
            'count': len(detected)
        })
    
    elapsed = time.time() - start_time
    
    return {
        'total': len(texts),
        'safe': safe_count,
        'risky': risky_count,
        'all_detected_words': list(all_sensitive_words),
        'detection_rate': risky_count / len(texts) * 100 if texts else 0,
        'time_elapsed': elapsed,
        'results': results
    }


def parallel_batch_detect(texts: List[str], max_workers: int = 4) -> List[Dict]:
    """
    Parallel batch detection using multiple threads
    
    Args:
        texts: List of texts to check
        max_workers: Maximum number of worker threads
        
    Returns:
        List of detection results
    """
    detector = SensitiveWordDetector()
    detector.add_word('敏感词')
    detector.add_word('违禁')
    detector.add_word('作弊')
    
    def detect_text(text: str) -> Dict:
        result = detector.detect(text)
        return {
            'text': text,
            'has_sensitive': len(result) > 0,
            'words': result
        }
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(detect_text, texts))
    
    return results


def file_batch_processing(input_file: str, output_file: str = None):
    """
    Process texts from a file
    
    Args:
        input_file: Input file path (one text per line)
        output_file: Output file path for results
    """
    detector = SensitiveWordDetector()
    detector.add_word('敏感词')
    detector.add_word('违禁')
    detector.add_word('作弊')
    detector.add_word('赌博')
    
    # Read texts from file
    with open(input_file, 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f if line.strip()]
    
    print(f"Loaded {len(texts)} texts from {input_file}")
    
    # Process
    start_time = time.time()
    results = batch_detect_with_stats(texts)
    elapsed = time.time() - start_time
    
    # Print summary
    print(f"\nProcessing completed in {elapsed:.2f}s")
    print(f"Total texts: {results['total']}")
    print(f"Safe: {results['safe']} ({100-results['detection_rate']:.1f}%)")
    print(f"Risky: {results['risky']} ({results['detection_rate']:.1f}%)")
    print(f"Unique sensitive words found: {len(results['all_detected_words'])}")
    
    # Save results if output file specified
    if output_file:
        import json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to {output_file}")
    
    return results


def example_usage():
    """Example usage of batch processing functions"""
    
    print("=" * 60)
    print("Batch Processing Examples")
    print("=" * 60)
    
    # Sample texts
    test_texts = [
        "这是一段正常的文本内容",
        "这是一个包含敏感词的测试",
        "正常文本不包含任何敏感词",
        "使用外挂作弊会被处罚",
        "赌博网站是违法的",
        "Python编程很有趣",
        "敏感词和违禁内容",
        "这是一段纯文本",
    ]
    
    # Example 1: Simple batch detection
    print("\n1. Simple Batch Detection")
    results = batch_detect_simple(test_texts)
    for r in results:
        status = "⚠️ RISKY" if r['has_sensitive'] else "✓ SAFE"
        print(f"  {status}: {r['text'][:40]}...")
    
    # Example 2: Batch with statistics
    print("\n2. Batch Detection with Statistics")
    stats = batch_detect_with_stats(test_texts)
    print(f"  Total: {stats['total']}")
    print(f"  Safe: {stats['safe']}")
    print(f"  Risky: {stats['risky']}")
    print(f"  Detection rate: {stats['detection_rate']:.1f}%")
    print(f"  Time: {stats['time_elapsed']:.3f}s")
    
    # Example 3: Parallel processing
    print("\n3. Parallel Batch Detection")
    large_texts = test_texts * 100  # Simulate large dataset
    start = time.time()
    parallel_results = parallel_batch_detect(large_texts, max_workers=4)
    elapsed = time.time() - start
    print(f"  Processed {len(large_texts)} texts in {elapsed:.2f}s")
    risky = sum(1 for r in parallel_results if r['has_sensitive'])
    print(f"  Found {risky} risky texts")


if __name__ == '__main__':
    example_usage()
