#!/bin/bash

echo "🚀 Starting StreamMe application..."

# Activate virtual environment (if using one)
if [ -d "venv" ]; then
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
fi

# Install required dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run Flask application
echo "✅ Running Flask server..."
python app.p
