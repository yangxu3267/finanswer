from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from transformers import DistilBertTokenizer, TFDistilBertForSequenceClassification
import numpy as np
import os
import re
from collections import Counter

app = Flask(__name__)
CORS(app)  # Enable CORS for Chrome extension

# Load the model and tokenizer
model_path = "../models/finbert"  # Path to the model directory
tokenizer = DistilBertTokenizer.from_pretrained(model_path)
model = TFDistilBertForSequenceClassification.from_pretrained(model_path)

# Label mapping
label_map = {
    0: "LABEL_0",  # Negative
    1: "LABEL_1",  # Neutral
    2: "LABEL_2"   # Positive
}

# Financial keywords for analysis
FINANCIAL_KEYWORDS = {
    'positive': ['growth', 'profit', 'gain', 'increase', 'rise', 'surge', 'jump', 'boost', 'recovery', 'success'],
    'negative': ['loss', 'decline', 'fall', 'drop', 'crash', 'plunge', 'decrease', 'risk', 'concern', 'worry'],
    'neutral': ['report', 'quarter', 'annual', 'forecast', 'expectation', 'analysis', 'data', 'figure', 'result']
}

def extract_key_phrases(text):
    """Extract key financial phrases from text"""
    # Clean text
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()
    
    # Find financial terms
    financial_terms = []
    for word in words:
        if any(term in word for term in ['earn', 'revenue', 'profit', 'stock', 'market', 'price', 'share', 'dividend']):
            financial_terms.append(word)
    
    # Get most common terms
    if financial_terms:
        counter = Counter(financial_terms)
        return [term for term, count in counter.most_common(3)]
    
    return ['market', 'financial', 'analysis']

def generate_summary(text, sentiment, confidence):
    """Generate a smart summary based on sentiment and content"""
    # Clean and split text into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if not sentences:
        return "Unable to extract meaningful content for summary."
    
    # Extract key phrases and entities
    key_phrases = extract_key_phrases(text)
    
    # Find the most relevant sentence based on sentiment
    relevant_sentence = find_most_relevant_sentence(sentences, sentiment, key_phrases)
    
    # Extract company names, numbers, and key metrics
    companies = extract_companies(text)
    numbers = extract_numbers(text)
    
    # Generate context-aware summary
    if sentiment == "LABEL_2":  # Positive
        if confidence > 0.8:
            summary = f"📈 Strong positive sentiment: {relevant_sentence}"
            if companies:
                summary += f" {companies[0]} shows promising performance"
            if numbers:
                summary += f" with {numbers[0]} growth"
            summary += ". The analysis suggests optimistic market conditions."
        else:
            summary = f"📊 Moderately positive outlook: {relevant_sentence}"
            summary += ". Consider monitoring for stronger confirmation signals."
    
    elif sentiment == "LABEL_0":  # Negative
        if confidence > 0.8:
            summary = f"📉 Strong negative sentiment: {relevant_sentence}"
            if companies:
                summary += f" {companies[0]} faces challenges"
            if numbers:
                summary += f" with {numbers[0]} decline"
            summary += ". The analysis suggests potential risks ahead."
        else:
            summary = f"⚠️ Moderately negative outlook: {relevant_sentence}"
            summary += ". Exercise caution and monitor developments."
    
    else:  # Neutral
        summary = f"📊 Balanced analysis: {relevant_sentence}"
        if companies:
            summary += f" {companies[0]} presents mixed signals"
        summary += ". The article requires careful consideration."
    
    return summary

def find_most_relevant_sentence(sentences, sentiment, key_phrases):
    """Find the most relevant sentence based on sentiment and key phrases"""
    if not sentences:
        return "The article discusses market developments."
    
    # Score sentences based on relevance
    sentence_scores = []
    for sentence in sentences:
        score = 0
        sentence_lower = sentence.lower()
        
        # Score based on key phrases
        for phrase in key_phrases:
            if phrase.lower() in sentence_lower:
                score += 2
        
        # Score based on sentiment indicators
        if sentiment == "LABEL_2":  # Positive
            positive_words = ['growth', 'profit', 'gain', 'increase', 'rise', 'surge', 'success', 'positive']
            score += sum(1 for word in positive_words if word in sentence_lower)
        elif sentiment == "LABEL_0":  # Negative
            negative_words = ['loss', 'decline', 'fall', 'drop', 'crash', 'risk', 'concern', 'negative']
            score += sum(1 for word in negative_words if word in sentence_lower)
        
        # Prefer sentences with numbers (metrics)
        if re.search(r'\d+%|\d+\.\d+', sentence):
            score += 1
        
        sentence_scores.append((score, sentence))
    
    # Return the highest scoring sentence, or first sentence if no clear winner
    sentence_scores.sort(reverse=True)
    return sentence_scores[0][1] if sentence_scores[0][0] > 0 else sentences[0]

def extract_companies(text):
    """Extract company names from text"""
    # Common company patterns
    company_patterns = [
        r'\b[A-Z][a-z]+ (Inc|Corp|Ltd|LLC|Company|Co)\b',
        r'\b[A-Z]{2,}\b',  # All caps words (like AAPL, GOOGL)
        r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'  # Two word companies
    ]
    
    companies = []
    for pattern in company_patterns:
        matches = re.findall(pattern, text)
        companies.extend(matches)
    
    # Remove duplicates and common false positives
    companies = list(set(companies))
    false_positives = ['The', 'This', 'That', 'They', 'When', 'What', 'Where', 'Why', 'How']
    companies = [c for c in companies if c not in false_positives]
    
    return companies[:3]  # Return top 3 companies

def extract_numbers(text):
    """Extract significant numbers from text"""
    # Find percentages, currency amounts, and other metrics
    number_patterns = [
        r'\d+\.?\d*%',  # Percentages
        r'\$\d+\.?\d*[MBK]?',  # Currency amounts
        r'\d+\.?\d*[MBK]',  # Numbers with M/B/K suffixes
    ]
    
    numbers = []
    for pattern in number_patterns:
        matches = re.findall(pattern, text)
        numbers.extend(matches)
    
    return numbers[:2]  # Return top 2 numbers

def generate_investment_advice(scores, sentiment, confidence, text):
    """Generate investment advice based on sentiment analysis"""
    # Extract market context
    has_earnings = 'earnings' in text.lower() or 'revenue' in text.lower()
    has_stock = 'stock' in text.lower() or 'share' in text.lower()
    has_market = 'market' in text.lower() or 'trading' in text.lower()
    
    advice = ""
    
    if confidence < 0.6:
        advice = "⚠️ Low confidence analysis. Consider gathering additional information from multiple sources before making investment decisions."
    
    elif sentiment == "LABEL_2":  # Positive
        if scores['positive'] > 0.85:
            advice = "🚀 Strong bullish signals detected. Consider increasing exposure to related assets while maintaining proper risk management and stop-loss orders."
        elif scores['positive'] > 0.7:
            advice = "📈 Positive market sentiment suggests favorable conditions. Monitor for technical confirmation and consider gradual position building."
        else:
            advice = "📊 Moderately positive outlook. Maintain current positions and watch for stronger confirmation signals."
    
    elif sentiment == "LABEL_0":  # Negative
        if scores['negative'] > 0.85:
            advice = "🔻 Strong bearish signals detected. Consider defensive positions, hedging strategies, or reducing exposure to related assets."
        elif scores['negative'] > 0.7:
            advice = "📉 Negative sentiment suggests caution. Review portfolio risk exposure and consider protective measures."
        else:
            advice = "⚠️ Moderately negative outlook. Exercise caution and avoid aggressive positions until sentiment improves."
    
    else:  # Neutral
        advice = "⚖️ Neutral sentiment indicates mixed signals. Focus on fundamental analysis, technical indicators, and wait for clearer directional signals."
    
    # Add context-specific advice
    if has_earnings:
        advice += " Pay attention to upcoming earnings reports and analyst expectations."
    if has_stock:
        advice += " Monitor stock-specific news and technical levels."
    if has_market:
        advice += " Consider broader market trends and sector performance."
    
    return advice

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Tokenize the text
        inputs = tokenizer(
            text,
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="tf"
        )
        
        # Get model predictions
        outputs = model(inputs)
        logits = outputs.logits
        
        # Convert to probabilities
        probabilities = tf.nn.softmax(logits, axis=-1)
        scores = probabilities.numpy()[0]
        
        # Get predicted label and confidence
        predicted_label_id = np.argmax(scores)
        confidence = float(scores[predicted_label_id])
        predicted_label = label_map[predicted_label_id]
        
        # Generate summary and investment advice
        summary = generate_summary(text, predicted_label, confidence)
        investment_advice = generate_investment_advice(
            {
                'negative': float(scores[0]),
                'neutral': float(scores[1]),
                'positive': float(scores[2])
            },
            predicted_label,
            confidence,
            text
        )
        
        result = {
            'label': predicted_label,
            'confidence': confidence,
            'scores': {
                'negative': float(scores[0]),
                'neutral': float(scores[1]),
                'positive': float(scores[2])
            },
            'summary': summary,
            'investment_advice': investment_advice
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': True})

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Handle user feedback for model improvement"""
    try:
        feedback_data = request.get_json()
        
        # 验证必要字段
        required_fields = ['text', 'predicted_sentiment', 'user_feedback', 'timestamp']
        for field in required_fields:
            if field not in feedback_data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # 保存反馈数据到文件（简单实现，生产环境应该用数据库）
        save_feedback_to_file(feedback_data)
        
        # 分析反馈数据用于模型改进
        analyze_feedback_for_improvement(feedback_data)
        
        return jsonify({
            "status": "success", 
            "message": "Feedback received successfully",
            "feedback_id": generate_feedback_id()
        })
        
    except Exception as e:
        print(f"Error processing feedback: {e}")
        return jsonify({"error": "Failed to process feedback"}), 500

def save_feedback_to_file(feedback_data):
    """保存反馈数据到文件"""
    import json
    from datetime import datetime
    
    # 创建反馈数据目录
    feedback_dir = "feedback_data"
    if not os.path.exists(feedback_dir):
        os.makedirs(feedback_dir)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{feedback_dir}/feedback_{timestamp}.json"
    
    # 保存数据
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(feedback_data, f, indent=2, ensure_ascii=False)
    
    print(f"Feedback saved to {filename}")

def analyze_feedback_for_improvement(feedback_data):
    """分析反馈数据，识别模型改进机会"""
    predicted = feedback_data['predicted_sentiment']
    user_feedback = feedback_data['user_feedback']
    confidence = feedback_data.get('predicted_confidence', 0)
    
    # 识别错误模式
    if user_feedback == 'inaccurate':
        print(f"🚨 Model error detected:")
        print(f"   - Predicted: {predicted}")
        print(f"   - Confidence: {confidence:.2f}")
        print(f"   - Text preview: {feedback_data['text'][:100]}...")
        
        # 可以在这里添加更复杂的分析逻辑
        # 例如：识别特定领域的错误模式
        
        # 如果置信度高但用户反馈错误，这是重要的改进信号
        if confidence > 0.8:
            print(f"   ⚠️ High confidence error - priority for model improvement")
    
    # 统计反馈数据
    update_feedback_statistics(feedback_data)

def update_feedback_statistics(feedback_data):
    """更新反馈统计信息"""
    import json
    
    stats_file = "feedback_data/statistics.json"
    
    try:
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                stats = json.load(f)
        else:
            stats = {
                "total_feedback": 0,
                "accurate_predictions": 0,
                "inaccurate_predictions": 0,
                "accuracy_rate": 0.0,
                "high_confidence_errors": 0,
                "sentiment_distribution": {"LABEL_0": 0, "LABEL_1": 0, "LABEL_2": 0}
            }
        
        # 更新统计
        stats["total_feedback"] += 1
        
        if feedback_data['user_feedback'] == 'accurate':
            stats["accurate_predictions"] += 1
        else:
            stats["inaccurate_predictions"] += 1
            
            # 检查高置信度错误
            confidence = feedback_data.get('predicted_confidence', 0)
            if confidence > 0.8:
                stats["high_confidence_errors"] += 1
        
        # 更新准确率
        stats["accuracy_rate"] = stats["accurate_predictions"] / stats["total_feedback"]
        
        # 更新情感分布
        sentiment = feedback_data['predicted_sentiment']
        if sentiment in stats["sentiment_distribution"]:
            stats["sentiment_distribution"][sentiment] += 1
        
        # 保存统计
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
            
        print(f"📊 Updated feedback statistics - Accuracy: {stats['accuracy_rate']:.2%}")
        
    except Exception as e:
        print(f"Error updating statistics: {e}")

def generate_feedback_id():
    """生成反馈ID"""
    import uuid
    return str(uuid.uuid4())[:8]

if __name__ == '__main__':
    print("Starting Finanswer Sentiment Analysis Server...")
    print("Model loaded successfully!")
    print("Server running on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True) 