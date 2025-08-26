import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# If API key is not set, prompt user to set it
if not GEMINI_API_KEY or GEMINI_API_KEY == 'your_gemini_api_key_here':
    print("⚠️  Warning: Gemini API key not set")
    print("Please set API key through one of the following methods:")
    print("1. Create .env file and add: GEMINI_API_KEY=your_actual_api_key")
    print("2. Set environment variable: export GEMINI_API_KEY=your_actual_api_key")
    print("3. Enter API key when running the application")
    print("Get API key: https://makersuite.google.com/app/apikey")

# Stock configuration
DEFAULT_TECH_STOCKS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
    'NVDA', 'AMD', 'INTC', 'CRM', 'ADBE',
    'META', 'NFLX', 'PYPL', 'SQ', 'UBER'
]

# News sources configuration
NEWS_SOURCES = [
    'reuters.com',
    'bloomberg.com', 
    'cnbc.com',
    'marketwatch.com'
]

# Analysis configuration
ANALYSIS_PROMPT = """
As a professional stock analyst, please provide buy/sell recommendations for tech stocks based on the following information:

Stock Information:
{symbol} - {name}
Current Price: ${current_price}
52-Week High: ${high_52w}
52-Week Low: ${low_52w}
P/E Ratio: {pe_ratio}
Market Cap: {market_cap}

Technical Indicators:
{technical_analysis}

Related News and Analysis:
{news_summary}

Please provide:
1. Buy/Sell/Hold recommendation
2. Target price
3. Risk level (Low/Medium/High)
4. Investment rationale
5. Risk warnings

Please answer in English with clear formatting.
"""
