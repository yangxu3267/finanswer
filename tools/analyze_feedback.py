#!/usr/bin/env python3
"""
反馈数据分析脚本
用于分析用户反馈数据，识别模型改进机会
"""

import json
import os
import pandas as pd
from collections import Counter
import re
from datetime import datetime, timedelta

class FeedbackAnalyzer:
    def __init__(self, feedback_dir="feedback_data"):
        self.feedback_dir = feedback_dir
        self.feedback_files = []
        self.feedback_data = []
        
    def load_feedback_data(self):
        """加载所有反馈数据"""
        if not os.path.exists(self.feedback_dir):
            print(f"❌ 反馈数据目录不存在: {self.feedback_dir}")
            return
            
        # 获取所有反馈文件
        for filename in os.listdir(self.feedback_dir):
            if filename.endswith('.json') and filename.startswith('feedback_'):
                filepath = os.path.join(self.feedback_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        data['filename'] = filename
                        self.feedback_data.append(data)
                except Exception as e:
                    print(f"⚠️ 无法读取文件 {filename}: {e}")
        
        print(f"📊 加载了 {len(self.feedback_data)} 条反馈数据")
    
    def generate_report(self):
        """生成反馈分析报告"""
        if not self.feedback_data:
            print("❌ 没有反馈数据可分析")
            return
            
        print("\n" + "="*60)
        print("📈 FinKnows 反馈数据分析报告")
        print("="*60)
        
        # 基础统计
        self._basic_statistics()
        
        # 错误模式分析
        self._error_pattern_analysis()
        
        # 高置信度错误分析
        self._high_confidence_error_analysis()
        
        # 情感分布分析
        self._sentiment_distribution_analysis()
        
        # 文本特征分析
        self._text_feature_analysis()
        
        # 模型改进建议
        self._model_improvement_suggestions()
    
    def _basic_statistics(self):
        """基础统计信息"""
        print("\n📊 基础统计信息:")
        print("-" * 30)
        
        total = len(self.feedback_data)
        accurate = sum(1 for f in self.feedback_data if f.get('user_feedback') == 'accurate')
        inaccurate = total - accurate
        accuracy_rate = accurate / total if total > 0 else 0
        
        print(f"总反馈数: {total}")
        print(f"准确预测: {accurate}")
        print(f"错误预测: {inaccurate}")
        print(f"准确率: {accuracy_rate:.2%}")
        
        # 时间分布
        if self.feedback_data:
            timestamps = [f.get('timestamp') for f in self.feedback_data if f.get('timestamp')]
            if timestamps:
                try:
                    dates = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps]
                    date_range = f"{min(dates).strftime('%Y-%m-%d')} 到 {max(dates).strftime('%Y-%m-%d')}"
                    print(f"数据时间范围: {date_range}")
                except:
                    pass
    
    def _error_pattern_analysis(self):
        """错误模式分析"""
        print("\n🚨 错误模式分析:")
        print("-" * 30)
        
        errors = [f for f in self.feedback_data if f.get('user_feedback') == 'inaccurate']
        if not errors:
            print("✅ 没有发现错误预测")
            return
            
        # 按情感标签分析错误
        error_by_sentiment = Counter(f.get('predicted_sentiment') for f in errors)
        print("错误预测的情感分布:")
        for sentiment, count in error_by_sentiment.most_common():
            sentiment_name = {
                'LABEL_0': 'Negative',
                'LABEL_1': 'Neutral', 
                'LABEL_2': 'Positive'
            }.get(sentiment, sentiment)
            print(f"  {sentiment_name}: {count} 次")
    
    def _high_confidence_error_analysis(self):
        """高置信度错误分析"""
        print("\n⚠️ 高置信度错误分析:")
        print("-" * 30)
        
        high_conf_errors = [
            f for f in self.feedback_data 
            if f.get('user_feedback') == 'inaccurate' and f.get('predicted_confidence', 0) > 0.8
        ]
        
        if not high_conf_errors:
            print("✅ 没有高置信度错误")
            return
            
        print(f"发现 {len(high_conf_errors)} 个高置信度错误:")
        
        for error in high_conf_errors[:5]:  # 显示前5个
            sentiment = error.get('predicted_sentiment', 'Unknown')
            confidence = error.get('predicted_confidence', 0)
            text_preview = error.get('text', '')[:100] + '...' if len(error.get('text', '')) > 100 else error.get('text', '')
            
            print(f"  - {sentiment} (置信度: {confidence:.2%}): {text_preview}")
    
    def _sentiment_distribution_analysis(self):
        """情感分布分析"""
        print("\n📊 情感分布分析:")
        print("-" * 30)
        
        sentiment_counts = Counter(f.get('predicted_sentiment') for f in self.feedback_data)
        total = len(self.feedback_data)
        
        sentiment_names = {
            'LABEL_0': 'Negative',
            'LABEL_1': 'Neutral',
            'LABEL_2': 'Positive'
        }
        
        for sentiment, count in sentiment_counts.most_common():
            name = sentiment_names.get(sentiment, sentiment)
            percentage = count / total * 100
            print(f"{name}: {count} 次 ({percentage:.1f}%)")
    
    def _text_feature_analysis(self):
        """文本特征分析"""
        print("\n🔍 文本特征分析:")
        print("-" * 30)
        
        # 分析错误预测的文本特征
        errors = [f for f in self.feedback_data if f.get('user_feedback') == 'inaccurate']
        if not errors:
            return
            
        # 提取常见词汇
        all_error_texts = ' '.join([f.get('text', '').lower() for f in errors])
        words = re.findall(r'\b\w+\b', all_error_texts)
        
        # 过滤常见词汇
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        filtered_words = [word for word in words if word not in common_words and len(word) > 3]
        
        word_counts = Counter(filtered_words)
        print("错误预测中最常见的词汇:")
        for word, count in word_counts.most_common(10):
            print(f"  {word}: {count} 次")
    
    def _model_improvement_suggestions(self):
        """模型改进建议"""
        print("\n💡 模型改进建议:")
        print("-" * 30)
        
        suggestions = []
        
        # 分析错误率
        total = len(self.feedback_data)
        errors = len([f for f in self.feedback_data if f.get('user_feedback') == 'inaccurate'])
        error_rate = errors / total if total > 0 else 0
        
        if error_rate > 0.3:
            suggestions.append("🔴 错误率较高 (>30%)，建议重新训练模型或增加训练数据")
        elif error_rate > 0.2:
            suggestions.append("🟡 错误率中等 (20-30%)，建议优化模型参数或增加特定领域数据")
        else:
            suggestions.append("🟢 错误率较低 (<20%)，模型表现良好")
        
        # 分析高置信度错误
        high_conf_errors = len([
            f for f in self.feedback_data 
            if f.get('user_feedback') == 'inaccurate' and f.get('predicted_confidence', 0) > 0.8
        ])
        
        if high_conf_errors > 0:
            suggestions.append(f"⚠️ 发现 {high_conf_errors} 个高置信度错误，需要重点关注这些样本")
        
        # 分析情感分布偏差
        sentiment_counts = Counter(f.get('predicted_sentiment') for f in self.feedback_data)
        if sentiment_counts:
            max_count = max(sentiment_counts.values())
            min_count = min(sentiment_counts.values())
            if max_count > min_count * 3:
                suggestions.append("📊 情感分布不均衡，建议平衡训练数据")
        
        # 输出建议
        for suggestion in suggestions:
            print(suggestion)
        
        if not suggestions:
            print("✅ 模型表现良好，暂无改进建议")
    
    def export_analysis_report(self, filename="feedback_analysis_report.txt"):
        """导出分析报告到文件"""
        import sys
        from io import StringIO
        
        # 重定向输出
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        # 生成报告
        self.generate_report()
        
        # 获取输出内容
        report_content = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        # 保存到文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📄 分析报告已保存到: {filename}")

def main():
    """主函数"""
    analyzer = FeedbackAnalyzer()
    analyzer.load_feedback_data()
    analyzer.generate_report()
    
    # 询问是否导出报告
    try:
        export = input("\n是否导出分析报告到文件? (y/n): ").lower().strip()
        if export == 'y':
            analyzer.export_analysis_report()
    except:
        pass

if __name__ == "__main__":
    main() 