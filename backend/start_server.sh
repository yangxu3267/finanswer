#!/bin/bash

echo "🚀 Starting FinBERT Sentiment Analysis Server..."
echo "📦 Installing dependencies..."

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Please install Python and pip first."
    exit 1
fi

# Install dependencies
pip install -r requirements.txt

echo "✅ Dependencies installed successfully!"
echo "🔧 Starting Flask server..."

# Start the server
python server.py 