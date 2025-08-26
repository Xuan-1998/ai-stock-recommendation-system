#!/bin/bash

# Deployment script for Tech Stocks Investment Analyzer
# This script ensures proper environment setup for deployment

echo "🚀 Starting deployment preparation..."

# Check if we're in a deployment environment
if [ -n "$PORT" ]; then
    echo "✅ Detected deployment environment (PORT: $PORT)"
else
    echo "ℹ️  Local development environment detected"
fi

# Set Python version constraint
export PYTHON_VERSION="3.11.18"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "🔍 Current Python version: $python_version"

# Install dependencies with specific versions for compatibility
echo "📦 Installing dependencies..."

# Upgrade pip first
pip install --upgrade pip

# Install numpy first (often needed for pandas)
pip install "numpy>=1.24.0,<2.0.0"

# Install pandas with specific version for Python 3.11 compatibility
pip install "pandas>=2.2.0,<3.0.0"

# Install other dependencies
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Check if all required packages are available
echo "🔍 Verifying package installations..."
python3 -c "
import sys
import importlib

required_packages = [
    'streamlit', 'pandas', 'yfinance', 'requests', 
    'beautifulsoup4', 'lxml', 'plotly', 'numpy',
    'matplotlib', 'seaborn', 'google.generativeai'
]

missing_packages = []
for package in required_packages:
    try:
        importlib.import_module(package.replace('-', '_'))
        print(f'✅ {package}')
    except ImportError:
        missing_packages.append(package)
        print(f'❌ {package}')

if missing_packages:
    print(f'\\n❌ Missing packages: {missing_packages}')
    sys.exit(1)
else:
    print('\\n✅ All packages successfully installed!')
"

if [ $? -ne 0 ]; then
    echo "❌ Error: Some packages failed to install"
    exit 1
fi

echo "🚀 Deployment preparation completed successfully!"
echo "📊 Application is ready to start"

# Start the application if not in a deployment environment
if [ -z "$PORT" ]; then
    echo "🌐 Starting Streamlit application..."
    streamlit run app.py --server.port=8501 --server.address=0.0.0.0
fi
