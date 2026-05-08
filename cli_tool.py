#!/usr/bin/env python3
"""
敏感词检测工具 - 命令行界面 v2.0
快速检测文本中的敏感词，计算风险评分，提供替代词建议
"""

import argparse
import json
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(__file__).rsplit('/', 1)[0] if '/' in __file__ else '.')

from sensitive_word_v2 import SensitiveWordDetector, RISK_LEVELS


def get_risk_emoji(level):
    """获取风险等级对应的emoji"""
    return {
        'safe': '✅',
        'low': '🟢',
        'medium': '🟡',
        'high': '🟠',
        'critical': '🔴'
    }.get(level, '⚪')


def get_risk_color(level):
    """获取风险等级对应的颜色"""
    return {
        'safe': '\033[92m',      # 绿色
        'low': '\033[32m',       # 深绿
        'medium': '\033[33m',    # 黄色
        'high': '\033[91m',      # 红色
        'critical': '\033[95m'   # 洋红
    }.get(level, '\033[0m')


def colored(text, level):
    """输出带颜色的文本"""
    RESET = '\033[0m'
    color = get_risk_color(level)
    return f"{color}{text}{RESET}"


def check_text(detector, text, show_suggestions=True):
    """检测文本并输出结果"""
    print("\n" + "=" * 60)
    print(f"原文: {text}")
    print("=" * 60)
    
    # 风险评分
    result = detector.calculate_risk_score(text)
    
    # 输出风险评分
    emoji = get_risk_emoji(result['level'])
    risk_text = colored(f"[{result['level'].upper()}] {result['label']}", result['level'])
    
    print(f"\n{emoji} 风险评分: {result['score']}/100 {risk_text}")
    
    # 输出详细信息
    if result['details']['word_count'] > 0:
        print(f"\n📊 详细信息:")
        print(f"   敏感词数量: {result['details']['word_count']}")
        print(f"   敏感词密度: {result['details']['density']}%")
        
        if result['details']['category_breakdown']:
            cats = ', '.join([f"{k}({v})" for k, v in result['details']['category_breakdown'].items()])
            print(f"   类别分布: {cats}")
    
    # 输出检测到的敏感词
    detected = detector.detect(text)
    if detected:
        print(f"\n🚨 检测到的敏感词:")
        for w in detected:
            level_color = w['level']
            level_text = colored(f"[{w['level']}]", level_color)
            print(f"   • {w['word']} {level_text} (位置: {w['start']}-{w['end']})")
    
    # 输出替代建议
    if show_suggestions and result['suggestions']:
        print(f"\n💡 替代词建议:")
        for s in result['suggestions']:
            print(f"   {s['original']} → {s['suggestion']}")
    
    # 输出替换后的文本
    replaced = detector.replace(text, '*', show_count=True)
    if replaced != text:
        print(f"\n🔒 替换后文本:")
        print(f"   {replaced}")
    
    return result


def check_file(detector, filepath, output_file=None):
    """批量检测文件内容"""
    print(f"\n📁 检测文件: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ 文件不存在: {filepath}")
        return None
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return None
    
    results = []
    safe_count = 0
    risky_count = 0
    
    print(f"\n检测 {len(lines)} 行...")
    print("-" * 60)
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        result = detector.calculate_risk_score(line)
        emoji = get_risk_emoji(result['level'])
        
        status = "✅ 安全" if result['level'] == 'safe' else f"⚠️ {result['score']}分"
        print(f"{emoji} L{i:3d}: {status} | {line[:50]}{'...' if len(line) > 50 else ''}")
        
        if result['level'] == 'safe':
            safe_count += 1
        else:
            risky_count += 1
            # 显示替代建议
            if result['suggestions']:
                for s in result['suggestions']:
                    print(f"      💡 {s['original']} → {s['suggestion']}")
        
        results.append({
            'line': i,
            'text': line,
            'result': result
        })
    
    print("-" * 60)
    print(f"\n📊 统计: 安全 {safe_count} | 风险 {risky_count} | 总计 {len(results)}")
    
    # 保存结果
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n💾 详细结果已保存到: {output_file}")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='敏感词检测工具 v2.0 - 快速检测、风险评分、替代词建议',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s -t "这是一个测试文本"
  %(prog)s -t "赌博作弊诈骗" --no-suggestions
  %(prog)s -f input.txt
  %(prog)s -f input.txt -o result.json
  %(prog)s --stats
  %(prog)s --wordlist
        '''
    )
    
    parser.add_argument('-t', '--text', type=str, help='待检测的文本')
    parser.add_argument('-f', '--file', type=str, help='待检测的文件（每行一个文本）')
    parser.add_argument('-o', '--output', type=str, help='输出结果文件(JSON格式)')
    parser.add_argument('--no-suggestions', action='store_true', help='不显示替代词建议')
    parser.add_argument('--stats', action='store_true', help='显示词库统计信息')
    parser.add_argument('--wordlist', action='store_true', help='显示当前词库列表')
    parser.add_argument('-w', '--wordlist-file', type=str, 
                        default=str(Path(__file__).parent / 'wordlist.txt'),
                        help='词库文件路径')
    
    args = parser.parse_args()
    
    # 初始化检测器
    try:
        detector = SensitiveWordDetector(args.wordlist_file)
    except Exception as e:
        print(f"❌ 初始化检测器失败: {e}")
        sys.exit(1)
    
    # 显示词库统计
    if args.stats:
        stats = detector.get_stats()
        print("\n📊 词库统计信息:")
        print(f"   总词数: {stats['total_words']}")
        print(f"   最短词: {stats['min_length']} 字")
        print(f"   最长词: {stats['max_length']} 字")
        print(f"\n   等级分布:")
        for level, count in stats['level_distribution'].items():
            emoji = get_risk_emoji(level)
            print(f"      {emoji} {level}: {count}")
        print(f"\n   类别分布:")
        for cat, count in stats.get('category_distribution', {}).items():
            print(f"      • {cat}: {count}")
        return
    
    # 显示词库列表
    if args.wordlist:
        words = detector.get_all_words()
        print(f"\n📝 当前词库 ({len(words)} 个词):")
        for i, word in enumerate(words, 1):
            print(f"   {i:4d}. {word}")
        return
    
    # 检测文本
    if args.text:
        check_text(detector, args.text, show_suggestions=not args.no_suggestions)
        return
    
    # 批量检测文件
    if args.file:
        check_file(detector, args.file, args.output)
        return
    
    # 无参数时显示帮助
    parser.print_help()


if __name__ == '__main__':
    main()
