import google.generativeai as genai
from config import GEMINI_API_KEY, ANALYSIS_PROMPT, ENHANCED_ANALYSIS_PROMPT, NANCY_PELOSI_TRADES
import json
import re

class GeminiAnalyzer:
    def __init__(self, api_key=None):
        """Initialize Gemini API"""
        self.api_key = api_key or GEMINI_API_KEY
        
        if not self.api_key:
            raise ValueError("Gemini API key not set")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_stock(self, stock_data, news_data):
        """Analyze stock data and provide recommendations"""
        try:
            # Prepare technical analysis summary
            tech_analysis = stock_data['technical_analysis']
            tech_summary = f"""
            RSI: {tech_analysis['rsi']}
            MACD: {tech_analysis['macd']}
            20-Day MA: ${tech_analysis['sma_20']}
            50-Day MA: ${tech_analysis['sma_50']}
            200-Day MA: ${tech_analysis['sma_200']}
            Technical Signals: {', '.join(tech_analysis['signals'])}
            """
            
            # Prepare news summary
            news_summary = ""
            if news_data:
                news_summary = "\n".join([
                    f"- {news['title']} ({news['source']})"
                    for news in news_data[:5]
                ])
            else:
                news_summary = "No recent news available"
            
            # Get Nancy Pelosi trading activity
            pelosi_analysis = self._get_pelosi_analysis(stock_data['symbol'])
            
            # Create enhanced analysis prompt
            prompt = ENHANCED_ANALYSIS_PROMPT.format(
                current_price=stock_data['current_price'],
                high_52w=stock_data['high_52w'],
                low_52w=stock_data['low_52w'],
                pe_ratio=stock_data['pe_ratio'],
                market_cap=stock_data['market_cap'],
                technical_indicators=tech_summary,
                news_summary=news_summary,
                pelosi_analysis=pelosi_analysis
            )
            
            # Generate analysis
            response = self.model.generate_content(prompt)
            analysis_text = response.text
            
            # Parse the response
            return self._parse_analysis_response(analysis_text, stock_data)
            
        except Exception as e:
            print(f"Error in stock analysis: {e}")
            return self._get_default_analysis(stock_data)
    
    def _get_pelosi_analysis(self, symbol):
        """Get Nancy Pelosi's trading activity for a specific stock"""
        if symbol in NANCY_PELOSI_TRADES:
            trade_data = NANCY_PELOSI_TRADES[symbol]
            return f"""
Nancy Pelosi Trading Activity for {symbol}:
- Last Action: {trade_data['last_action']}
- Date: {trade_data['last_date']}
- Amount: {trade_data['amount']}
- Return: {trade_data['return']}
- Sentiment: {trade_data['sentiment']}

Note: Nancy Pelosi's trading strategy has shown +740.83% return since 2014, significantly outperforming the market (+243.16%).
"""
        else:
            return f"""
Nancy Pelosi Trading Activity for {symbol}:
No recent trading activity found for this stock.

Note: Nancy Pelosi's trading strategy has shown +740.83% return since 2014, significantly outperforming the market (+243.16%).
"""
    
    def get_market_sentiment(self, news_data):
        """Analyze market sentiment based on news"""
        try:
            # Prepare news summary
            news_summary = "\n".join([
                f"- {news['title']} ({news['source']})"
                for news in news_data[:10]
            ])
            
            prompt = f"""
            As a market analyst, analyze the following tech market news and provide a comprehensive market sentiment analysis:
            
            Recent Tech Market News:
            {news_summary}
            
            Please provide:
            1. Overall market sentiment (Bullish/Bearish/Neutral)
            2. Key factors driving the sentiment
            3. Impact on tech stocks
            4. Key risks for investors to watch
            
            Format your response clearly with headers and bullet points.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Error in market sentiment analysis: {e}")
            return """
            **Market Sentiment Analysis**
            
            Unable to analyze market sentiment due to technical issues.
            Please try again later or check your API key configuration.
            """
    
    def _parse_analysis_response(self, response_text, stock_data):
        """Parse AI analysis response"""
        try:
            # Extract key information using regex
            action_match = re.search(r'recommendation[:\s]*(\w+)', response_text, re.IGNORECASE)
            action = action_match.group(1).title() if action_match else 'Hold'
            
            # Extract target price
            price_match = re.search(r'target\s*price[:\s]*\$?([\d,]+\.?\d*)', response_text, re.IGNORECASE)
            target_price = f"${price_match.group(1)}" if price_match else f"${stock_data['current_price'] * 1.05:.2f}"
            
            # Extract risk level
            risk_match = re.search(r'risk\s*level[:\s]*(\w+)', response_text, re.IGNORECASE)
            risk_level = risk_match.group(1).title() if risk_match else 'Medium'
            
            # Extract reasoning and risks
            sections = response_text.split('\n\n')
            reasoning = ""
            risks = ""
            
            for section in sections:
                if 'rationale' in section.lower() or 'reason' in section.lower():
                    reasoning = section
                elif 'risk' in section.lower() and 'warning' in section.lower():
                    risks = section
            
            if not reasoning:
                reasoning = "Analysis based on technical indicators and market conditions."
            if not risks:
                risks = "Market volatility and economic uncertainty are key risks to consider."
            
            return {
                'action': action,
                'target_price': target_price,
                'risk_level': risk_level,
                'reasoning': reasoning,
                'risks': risks,
                'raw_response': response_text
            }
            
        except Exception as e:
            print(f"Error parsing analysis response: {e}")
            return self._get_default_analysis(stock_data)
    
    def _get_default_analysis(self, stock_data):
        """Get default analysis when parsing fails"""
        return {
            'action': 'Hold',
            'target_price': f"${stock_data['current_price'] * 1.05:.2f}",
            'risk_level': 'Medium',
            'reasoning': f"Based on current market conditions and technical indicators, {stock_data['symbol']} shows moderate growth potential with balanced risk-reward profile.",
            'risks': "Market volatility, economic uncertainty, and industry competition are key risks to consider.",
            'raw_response': f"Default analysis for {stock_data['symbol']}: Hold recommendation with medium risk level."
        }
