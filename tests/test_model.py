#!/usr/bin/env python3
"""
Test script to verify FinBERT model functionality
"""

import requests
import json

def test_model():
    """Test the FinBERT sentiment analysis model"""
    
    # Test cases
    test_texts = [
        "The stock market is performing exceptionally well with record-breaking gains.",
        "Company profits are declining rapidly due to poor management decisions.",
        "The quarterly earnings report shows stable growth in revenue.",
        "Investors are concerned about the market volatility and economic uncertainty.",
        "The new product launch exceeded all expectations and boosted sales significantly."
    ]
    
    print("🧪 Testing FinBERT Sentiment Analysis Model")
    print("=" * 50)
    
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
    
    print("\n📊 Testing sentiment analysis...")
    print("-" * 50)
    
    for i, text in enumerate(test_texts, 1):
        try:
            response = requests.post(
                'http://localhost:5001/analyze',
                json={'text': text},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                label = result['label']
                confidence = result['confidence']
                
                # Map labels to readable text
                label_map = {
                    'LABEL_0': 'Negative',
                    'LABEL_1': 'Neutral',
                    'LABEL_2': 'Positive'
                }
                
                readable_label = label_map.get(label, label)
                confidence_percent = confidence * 100
                
                print(f"Test {i}: {readable_label} ({confidence_percent:.1f}%)")
                print(f"   Text: {text[:80]}...")
                print()
            else:
                print(f"❌ Test {i} failed: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Test {i} failed: {e}")
    
    print("✅ Testing completed!")

if __name__ == "__main__":
    test_model() 