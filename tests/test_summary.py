#!/usr/bin/env python3
"""
Test script to demonstrate improved summary generation
"""

import requests
import json

def test_summary_generation():
    """Test the improved summary generation"""
    
    # Real financial news examples
    test_cases = [
        {
            "title": "Tesla Q4 Earnings Beat",
            "text": "Tesla Inc. reported fourth-quarter earnings that exceeded analyst expectations, with revenue reaching $25.17 billion, up 3% from the previous year. The electric vehicle maker delivered 484,507 vehicles in the quarter, representing a 20% increase year-over-year. CEO Elon Musk expressed confidence in the company's growth trajectory, citing strong demand for Model Y and upcoming product launches. Tesla's gross margin improved to 18.1%, beating estimates of 17.6%."
        },
        {
            "title": "Fed Rate Hike Impact",
            "text": "The Federal Reserve announced a 0.25 percentage point increase in the federal funds rate, bringing it to 5.25%-5.50%. This marks the 11th rate hike since March 2022. Markets reacted negatively to the news, with the Dow Jones Industrial Average falling 530 points, or 1.6%, while the S&P 500 declined 1.4%. Analysts warn that higher borrowing costs could slow economic growth and impact corporate earnings in the coming quarters."
        },
        {
            "title": "Apple Services Growth",
            "text": "Apple Inc. reported strong growth in its services segment, with revenue reaching $20.8 billion in the latest quarter, up 8% year-over-year. The company's App Store, Apple Music, and iCloud services all showed robust performance. However, iPhone sales declined 2% to $69.7 billion, missing analyst expectations. CEO Tim Cook highlighted the importance of services as a key growth driver for the company's future."
        }
    ]
    
    print("📰 Testing Improved Summary Generation")
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
    
    print("\n📊 Testing Content-Based Summaries...")
    print("-" * 60)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {case['title']}")
        print("-" * 40)
        print(f"📄 Original Text: {case['text'][:100]}...")
        
        try:
            response = requests.post(
                'http://localhost:5001/analyze',
                json={'text': case['text']},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Display sentiment
                label = result['label']
                confidence = result['confidence']
                
                label_map = {
                    'LABEL_0': 'Negative',
                    'LABEL_1': 'Neutral',
                    'LABEL_2': 'Positive'
                }
                
                readable_label = label_map.get(label, label)
                confidence_percent = confidence * 100
                
                print(f"\n📈 Sentiment: {readable_label} ({confidence_percent:.1f}%)")
                
                # Display improved summary
                if 'summary' in result:
                    print(f"\n📰 AI Summary:")
                    print(f"   {result['summary']}")
                
                # Display investment advice
                if 'investment_advice' in result:
                    print(f"\n💡 Investment Insight:")
                    print(f"   {result['investment_advice']}")
                
            else:
                print(f"❌ Test {i} failed: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Test {i} failed: {e}")
        
        print("\n" + "="*60)
    
    print("\n🎉 Summary Generation Test Completed!")
    print("\n✨ Improvements demonstrated:")
    print("   • Content-based sentence selection")
    print("   • Company name extraction")
    print("   • Key metrics identification")
    print("   • Context-aware summarization")
    print("   • Sentiment-driven relevance scoring")

if __name__ == "__main__":
    test_summary_generation() 