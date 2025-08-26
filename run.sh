#!/bin/bash

# AI Stock Recommendation System - Quick Start Script
# This script checks dependencies and starts the application

echo "🚀 Tech Stocks Investment Analyzer"
echo "=================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    echo "Please install pip3 and try again"
    exit 1
fi

echo "✅ pip3 found"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    echo "Please ensure you're in the correct directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Check API key status
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  Warning: GEMINI_API_KEY environment variable not set"
    echo "The application will work in demo mode"
    echo "To enable full AI features, set your API key:"
    echo "export GEMINI_API_KEY=your_api_key_here"
    echo ""
else
    echo "✅ GEMINI_API_KEY is set"
fi

# Check if .env file exists
if [ -f ".env" ]; then
    echo "✅ .env file found"
else
    echo "ℹ️  No .env file found (optional)"
    echo "You can create one with: echo 'GEMINI_API_KEY=your_key' > .env"
fi

echo ""
echo "🚀 Starting Tech Stocks Investment Analyzer..."
echo "The application will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""

# Start the application
python3 -m streamlit run app.py
