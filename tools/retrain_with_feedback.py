#!/usr/bin/env python3
"""
基于用户反馈的模型重训练脚本
利用收集的用户反馈数据来改进 FinBERT 模型
"""

import json
import os
import numpy as np
import tensorflow as tf
from transformers import DistilBertTokenizer, TFDistilBertForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
from datetime import datetime

class FeedbackBasedRetrainer:
    def __init__(self, model_path="../models/finbert", feedback_dir="../feedback_data"):
        self.model_path = model_path
        self.feedback_dir = feedback_dir
        self.tokenizer = None
        self.model = None
        self.feedback_data = []
        
    def load_model_and_tokenizer(self):
        """加载现有模型和分词器"""
        print("🔄 加载现有模型和分词器...")
        self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_path)
        self.model = TFDistilBertForSequenceClassification.from_pretrained(self.model_path)
        print("✅ 模型加载完成")
    
    def load_feedback_data(self):
        """加载用户反馈数据"""
        print("📊 加载用户反馈数据...")
        
        if not os.path.exists(self.feedback_dir):
            print(f"❌ 反馈数据目录不存在: {self.feedback_dir}")
            return False
            
        # 加载所有反馈文件
        for filename in os.listdir(self.feedback_dir):
            if filename.endswith('.json') and filename.startswith('feedback_'):
                filepath = os.path.join(self.feedback_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.feedback_data.append(data)
                except Exception as e:
                    print(f"⚠️ 无法读取文件 {filename}: {e}")
        
        print(f"📈 加载了 {len(self.feedback_data)} 条反馈数据")
        return len(self.feedback_data) > 0
    
    def prepare_training_data(self):
        """准备训练数据"""
        print("🔧 准备训练数据...")
        
        training_data = []
        
        for feedback in self.feedback_data:
            text = feedback.get('text', '').strip()
            if not text or len(text) < 10:  # 过滤太短的文本
                continue
                
            predicted_sentiment = feedback.get('predicted_sentiment')
            user_feedback = feedback.get('user_feedback')
            confidence = feedback.get('predicted_confidence', 0)
            
            # 只使用用户反馈为"inaccurate"的数据进行重训练
            if user_feedback == 'inaccurate':
                # 这里需要用户提供正确的标签
                # 在实际应用中，可能需要人工标注或使用其他方法
                # 暂时跳过这些样本
                continue
            
            # 使用用户反馈为"accurate"的数据作为正样本
            if user_feedback == 'accurate':
                # 将预测结果作为训练标签
                label_map = {
                    'LABEL_0': 0,  # Negative
                    'LABEL_1': 1,  # Neutral
                    'LABEL_2': 2   # Positive
                }
                
                if predicted_sentiment in label_map:
                    training_data.append({
                        'text': text,
                        'label': label_map[predicted_sentiment],
                        'confidence': confidence
                    })
        
        print(f"📚 准备了 {len(training_data)} 条训练数据")
        return training_data
    
    def create_dataset(self, training_data):
        """创建 TensorFlow 数据集"""
        if not training_data:
            print("❌ 没有足够的训练数据")
            return None, None
            
        texts = [item['text'] for item in training_data]
        labels = [item['label'] for item in training_data]
        
        # 分词
        encodings = self.tokenizer(
            texts,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="tf"
        )
        
        # 创建数据集
        dataset = tf.data.Dataset.from_tensor_slices((
            {
                'input_ids': encodings['input_ids'],
                'attention_mask': encodings['attention_mask']
            },
            labels
        ))
        
        # 分割训练集和验证集
        total_size = len(training_data)
        train_size = int(0.8 * total_size)
        
        train_dataset = dataset.take(train_size)
        val_dataset = dataset.skip(train_size)
        
        print(f"📊 训练集: {train_size} 样本")
        print(f"📊 验证集: {total_size - train_size} 样本")
        
        return train_dataset, val_dataset
    
    def retrain_model(self, train_dataset, val_dataset):
        """重训练模型"""
        if not train_dataset or not val_dataset:
            print("❌ 无法重训练：数据集为空")
            return False
            
        print("🚀 开始模型重训练...")
        
        # 设置训练参数
        training_args = TrainingArguments(
            output_dir="./retrained_model",
            num_train_epochs=3,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            warmup_steps=100,
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=10,
            evaluation_strategy="steps",
            eval_steps=50,
            save_steps=100,
            load_best_model_at_end=True,
            metric_for_best_model="accuracy"
        )
        
        # 创建训练器
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            tokenizer=self.tokenizer
        )
        
        # 开始训练
        try:
            trainer.train()
            print("✅ 模型重训练完成")
            return True
        except Exception as e:
            print(f"❌ 训练失败: {e}")
            return False
    
    def save_retrained_model(self):
        """保存重训练后的模型"""
        output_dir = f"./retrained_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"💾 保存重训练模型到: {output_dir}")
        
        try:
            self.model.save_pretrained(output_dir)
            self.tokenizer.save_pretrained(output_dir)
            print("✅ 模型保存成功")
            return output_dir
        except Exception as e:
            print(f"❌ 模型保存失败: {e}")
            return None
    
    def evaluate_model(self, test_data=None):
        """评估模型性能"""
        print("📊 评估模型性能...")
        
        if test_data is None:
            # 使用部分反馈数据作为测试集
            test_data = self.feedback_data[-min(50, len(self.feedback_data)):]
        
        if not test_data:
            print("❌ 没有测试数据")
            return
        
        correct = 0
        total = 0
        
        for feedback in test_data:
            text = feedback.get('text', '').strip()
            if not text:
                continue
                
            # 使用模型进行预测
            inputs = self.tokenizer(
                text,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="tf"
            )
            
            outputs = self.model(inputs)
            predictions = tf.nn.softmax(outputs.logits, axis=-1)
            predicted_label = tf.argmax(predictions, axis=-1).numpy()[0]
            
            # 检查预测是否正确（基于用户反馈）
            user_feedback = feedback.get('user_feedback')
            if user_feedback == 'accurate':
                correct += 1
            total += 1
        
        if total > 0:
            accuracy = correct / total
            print(f"📈 模型准确率: {accuracy:.2%} ({correct}/{total})")
        else:
            print("❌ 无法计算准确率")
    
    def generate_retraining_report(self, training_data, output_dir):
        """生成重训练报告"""
        report = {
            "retraining_date": datetime.now().isoformat(),
            "original_model_path": self.model_path,
            "retrained_model_path": output_dir,
            "total_feedback_data": len(self.feedback_data),
            "training_samples": len(training_data),
            "feedback_accuracy": self._calculate_feedback_accuracy(),
            "model_improvements": self._suggest_improvements()
        }
        
        # 保存报告
        report_file = f"{output_dir}/retraining_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📄 重训练报告已保存到: {report_file}")
        return report
    
    def _calculate_feedback_accuracy(self):
        """计算反馈数据的准确率"""
        if not self.feedback_data:
            return 0.0
            
        accurate = sum(1 for f in self.feedback_data if f.get('user_feedback') == 'accurate')
        return accurate / len(self.feedback_data)
    
    def _suggest_improvements(self):
        """建议改进措施"""
        suggestions = []
        
        # 分析反馈数据
        high_conf_errors = [
            f for f in self.feedback_data 
            if f.get('user_feedback') == 'inaccurate' and f.get('predicted_confidence', 0) > 0.8
        ]
        
        if high_conf_errors:
            suggestions.append(f"发现 {len(high_conf_errors)} 个高置信度错误，需要重点关注")
        
        # 分析情感分布
        sentiment_counts = {}
        for f in self.feedback_data:
            sentiment = f.get('predicted_sentiment')
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        if sentiment_counts:
            max_count = max(sentiment_counts.values())
            min_count = min(sentiment_counts.values())
            if max_count > min_count * 2:
                suggestions.append("情感分布不均衡，建议平衡训练数据")
        
        return suggestions

def main():
    """主函数"""
    print("🤖 FinKnows 模型重训练工具")
    print("=" * 50)
    
    retrainer = FeedbackBasedRetrainer()
    
    # 加载模型
    retrainer.load_model_and_tokenizer()
    
    # 加载反馈数据
    if not retrainer.load_feedback_data():
        print("❌ 无法加载反馈数据，退出")
        return
    
    # 准备训练数据
    training_data = retrainer.prepare_training_data()
    if not training_data:
        print("❌ 没有足够的训练数据，退出")
        return
    
    # 创建数据集
    train_dataset, val_dataset = retrainer.create_dataset(training_data)
    if not train_dataset or not val_dataset:
        print("❌ 无法创建数据集，退出")
        return
    
    # 重训练模型
    if retrainer.retrain_model(train_dataset, val_dataset):
        # 保存模型
        output_dir = retrainer.save_retrained_model()
        if output_dir:
            # 评估模型
            retrainer.evaluate_model()
            
            # 生成报告
            retrainer.generate_retraining_report(training_data, output_dir)
            
            print(f"\n🎉 模型重训练完成！")
            print(f"📁 新模型保存在: {output_dir}")
            print(f"📊 使用了 {len(training_data)} 条训练数据")
        else:
            print("❌ 模型保存失败")
    else:
        print("❌ 模型重训练失败")

if __name__ == "__main__":
    main() 