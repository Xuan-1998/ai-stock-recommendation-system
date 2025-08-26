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

# Nancy Pelosi trading activity analysis
NANCY_PELOSI_TRADES = {
    'AAPL': {
        'last_action': 'Sale',
        'last_date': '2025-01-17',
        'amount': '$5M-$25M',
        'return': '-18.92%',
        'sentiment': 'Bearish'
    },
    'NVDA': {
        'last_action': 'Purchase',
        'last_date': '2025-01-17',
        'amount': '$250K-$500K',
        'return': '+26.11%',
        'sentiment': 'Bullish'
    },
    'MSFT': {
        'last_action': 'Sale',
        'last_date': '2024-07-30',
        'amount': '$1M-$5M',
        'return': '+0.51%',
        'sentiment': 'Neutral'
    },
    'GOOGL': {
        'last_action': 'Purchase',
        'last_date': '2025-01-17',
        'amount': '$250K-$500K',
        'return': '-0.43%',
        'sentiment': 'Neutral'
    },
    'AMZN': {
        'last_action': 'Purchase',
        'last_date': '2025-01-17',
        'amount': '$250K-$500K',
        'return': '-5.68%',
        'sentiment': 'Neutral'
    },
    'TSLA': {
        'last_action': 'Sale',
        'last_date': '2024-07-02',
        'amount': '$250K-$500K',
        'return': '+71.80%',
        'sentiment': 'Bullish'
    },
    'AVGO': {
        'last_action': 'Purchase',
        'last_date': '2025-07-09',
        'amount': '$1M-$5M',
        'return': '+9.85%',
        'sentiment': 'Bullish'
    }
}

# Enhanced analysis prompt including Nancy Pelosi's trading activity
ENHANCED_ANALYSIS_PROMPT = """
As a professional stock analyst, please provide buy/sell recommendations for tech stocks based on the following information:

Stock Information:
Current Price: ${current_price}
52-Week High: ${high_52w}
52-Week Low: ${low_52w}
P/E Ratio: {pe_ratio}
Market Cap: {market_cap}

Technical Indicators:
{technical_indicators}

Related News and Analysis:
{news_summary}

Nancy Pelosi Trading Activity:
{pelosi_analysis}

Please provide:
1. Buy/Sell/Hold recommendation
2. Target price
3. Risk level (Low/Medium/High)
4. Investment rationale
5. Risk warnings
6. Impact of Nancy Pelosi's trading activity on this stock

Please answer in English with clear formatting.
"""
