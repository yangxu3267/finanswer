#!/usr/bin/env python3
"""
Advanced test script to demonstrate enhanced FinBERT features
"""

import requests
import json
import time

def test_advanced_features():
    """Test the enhanced FinBERT features"""
    
    # Realistic financial news test cases
    test_cases = [
        {
            "title": "Positive Earnings Report",
            "text": "Apple Inc. reported exceptional quarterly earnings with revenue growth of 15% year-over-year. The company's iPhone sales exceeded analyst expectations, and the services division showed strong performance. CEO Tim Cook expressed optimism about future growth prospects, citing strong demand in emerging markets and successful product launches."
        },
        {
            "title": "Market Crash Concerns",
            "text": "Global markets experienced significant volatility as concerns about inflation and rising interest rates intensified. Major indices declined sharply, with the S&P 500 dropping 3.2% in a single trading session. Analysts warn of potential further declines as economic uncertainty persists and central banks signal more aggressive monetary policy."
        },
        {
            "title": "Neutral Market Analysis",
            "text": "The Federal Reserve released its monthly economic report, showing mixed signals about the current state of the economy. While employment numbers remain strong, inflation continues to be a concern. Market participants are closely monitoring upcoming policy decisions and their potential impact on various sectors."
        }
    ]
    
    print("🚀 Testing Enhanced FinBERT Features")
    print("=" * 60)
    
    # Check if server is running
    try:
        health_response = requests.get('http://localhost:5001/health', timeout=5)
        if health_response.status_code == 200:
            print("✅ Server is running and healthy")
        else:
            print("❌ Server is not responding properly")
            return
    except requests.exceptions.RequestException:
        print("❌ Server is not running. Please start the server first:")
        print("   python server.py")
        return
    
    print("\n📊 Testing Enhanced Analysis...")
    print("-" * 60)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {case['title']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                'http://localhost:5001/analyze',
                json={'text': case['text']},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display sentiment analysis
                label = result['label']
                confidence = result['confidence']
                scores = result['scores']
                
                label_map = {
                    'LABEL_0': 'Negative',
                    'LABEL_1': 'Neutral',
                    'LABEL_2': 'Positive'
                }
                
                readable_label = label_map.get(label, label)
                confidence_percent = confidence * 100
                
                print(f"📈 Sentiment: {readable_label} ({confidence_percent:.1f}%)")
                print(f"📊 Scores - Negative: {scores['negative']:.3f}, Neutral: {scores['neutral']:.3f}, Positive: {scores['positive']:.3f}")
                
                # Display summary
                if 'summary' in result:
                    print(f"\n📰 Summary:")
                    print(f"   {result['summary']}")
                
                # Display investment advice
                if 'investment_advice' in result:
                    print(f"\n💡 Investment Advice:")
                    print(f"   {result['investment_advice']}")
                
                # Visual sentiment meter
                print(f"\n🎯 Sentiment Meter:")
                meter_position = calculate_meter_position(scores, readable_label)
                meter_display = "[" + " " * int(meter_position/2) + "●" + " " * (50 - int(meter_position/2)) + "]"
                print(f"   Negative {meter_display} Positive")
                print(f"   {' ' * int(meter_position/2)}↑")
                
            else:
                print(f"❌ Test {i} failed: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Test {i} failed: {e}")
        
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 60)
    print("✅ Advanced testing completed!")
    print("\n🎉 Features demonstrated:")
    print("   • Real-time sentiment analysis")
    print("   • Intelligent news summarization")
    print("   • Context-aware investment advice")
    print("   • Visual sentiment meter")
    print("   • Confidence scoring")

def calculate_meter_position(scores, label):
    """Calculate position for visual sentiment meter"""
    if label == 'Negative':
        return scores['negative'] * 25  # 0-25
    elif label == 'Neutral':
        return 25 + (scores['neutral'] * 25)  # 25-50
    else:
        return 50 + (scores['positive'] * 25)  # 50-75

if __name__ == "__main__":
    test_advanced_features() 