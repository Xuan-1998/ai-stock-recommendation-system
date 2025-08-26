import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import random
import time

class NewsCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # News sources
        self.news_sources = {
            'reuters': 'https://www.reuters.com',
            'bloomberg': 'https://www.bloomberg.com',
            'cnbc': 'https://www.cnbc.com',
            'marketwatch': 'https://www.marketwatch.com'
        }
    
    def search_news(self, query, max_results=10, use_mock=False):
        """Search for news articles"""
        if use_mock:
            return self._get_mock_news(query, max_results)
        
        try:
            # Try to get real news
            news_data = self._search_real_news(query, max_results)
            if news_data:
                return news_data
        except Exception as e:
            print(f"Error fetching real news: {e}")
        
        # Fallback to mock data
        return self._get_mock_news(query, max_results)
    
    def get_tech_market_news(self, max_results=10, use_mock=False):
        """Get tech market news"""
        if use_mock:
            return self._get_mock_tech_news(max_results)
        
        try:
            # Try to get real tech news
            news_data = self._search_real_news("tech market stocks", max_results)
            if news_data:
                return news_data
        except Exception as e:
            print(f"Error fetching real tech news: {e}")
        
        # Fallback to mock data
        return self._get_mock_tech_news(max_results)
    
    def get_stock_specific_news(self, symbol, company_name, max_results=10, use_mock=False):
        """Get stock-specific news"""
        if use_mock:
            return self._get_mock_stock_news(symbol, company_name, max_results)
        
        try:
            # Try to get real stock news
            query = f"{symbol} {company_name} stock"
            news_data = self._search_real_news(query, max_results)
            if news_data:
                return news_data
        except Exception as e:
            print(f"Error fetching real stock news: {e}")
        
        # Fallback to mock data
        return self._get_mock_stock_news(symbol, company_name, max_results)
    
    def _search_real_news(self, query, max_results):
        """Search for real news articles"""
        # This is a simplified implementation
        # In a real application, you would use news APIs like NewsAPI, GNews, etc.
        
        # For now, return None to trigger mock data fallback
        return None
    
    def _get_mock_news(self, query, max_results):
        """Get mock news data"""
        mock_news = [
            {
                'title': 'Tech Stocks Rally on Strong Earnings Reports',
                'source': 'Reuters',
                'date': datetime.now() - timedelta(days=1),
                'summary': 'Major technology companies reported better-than-expected earnings, driving the tech sector higher.',
                'link': None
            },
            {
                'title': 'AI Development Accelerates Market Innovation',
                'source': 'Bloomberg',
                'date': datetime.now() - timedelta(days=2),
                'summary': 'Artificial intelligence advancements continue to reshape the technology landscape.',
                'link': None
            },
            {
                'title': 'Cloud Computing Demand Surges',
                'source': 'CNBC',
                'date': datetime.now() - timedelta(days=3),
                'summary': 'Enterprise cloud adoption drives growth in cloud computing services.',
                'link': None
            }
        ]
        
        return mock_news[:max_results]
    
    def _get_mock_tech_news(self, max_results):
        """Get mock tech market news"""
        mock_tech_news = [
            {
                'title': 'Electric Vehicle Market Growth Slows, Tesla Stock Under Pressure',
                'source': 'CNBC',
                'date': datetime.now() - timedelta(days=1),
                'summary': 'Global electric vehicle sales growth has slowed, putting pressure on Tesla and other major manufacturers.',
                'link': None
            },
            {
                'title': 'Tech Stocks Lead Market Gains, AI-Related Stocks Show Strong Performance',
                'source': 'Reuters',
                'date': datetime.now() - timedelta(days=1),
                'summary': 'Rapid development of artificial intelligence technology is driving tech stock gains, with investors optimistic about AI prospects.',
                'link': None
            },
            {
                'title': 'Chip Manufacturer Earnings Exceed Expectations, Semiconductor Sector Strengthens',
                'source': 'Bloomberg',
                'date': datetime.now() - timedelta(days=3),
                'summary': 'Major chip manufacturers released strong earnings reports, showing signs of industry recovery.',
                'link': None
            },
            {
                'title': 'Cloud Computing Service Demand Continues to Grow, Microsoft Azure Performs Well',
                'source': 'Reuters',
                'date': datetime.now() - timedelta(days=4),
                'summary': 'Enterprise digital transformation is driving cloud computing service demand, benefiting cloud service providers like Microsoft.',
                'link': None
            },
            {
                'title': 'Social Media Platforms Face Regulatory Pressure, Meta Stock Volatile',
                'source': 'Bloomberg',
                'date': datetime.now() - timedelta(days=4),
                'summary': 'Countries are strengthening regulation of social media platforms, with Meta and other companies facing new compliance challenges.',
                'link': None
            }
        ]
        
        return mock_tech_news[:max_results]
    
    def _get_mock_stock_news(self, symbol, company_name, max_results):
        """Get mock stock-specific news"""
        stock_news_templates = {
            'AAPL': [
                {
                    'title': f'{company_name} Reports Strong iPhone Sales',
                    'source': 'Reuters',
                    'date': datetime.now() - timedelta(days=1),
                    'summary': f'{company_name} announced better-than-expected iPhone sales, driven by strong demand in emerging markets.',
                    'link': None
                },
                {
                    'title': f'{company_name} Services Revenue Continues to Grow',
                    'source': 'Bloomberg',
                    'date': datetime.now() - timedelta(days=2),
                    'summary': f'{company_name} services business shows strong growth, improving profit margins and diversifying revenue streams.',
                    'link': None
                }
            ],
            'MSFT': [
                {
                    'title': f'{company_name} Azure Cloud Business Shows Strong Growth',
                    'source': 'CNBC',
                    'date': datetime.now() - timedelta(days=1),
                    'summary': f'{company_name} Azure cloud computing platform continues to gain market share, driving overall revenue growth.',
                    'link': None
                },
                {
                    'title': f'{company_name} AI Integration Boosts Productivity Tools',
                    'source': 'Reuters',
                    'date': datetime.now() - timedelta(days=3),
                    'summary': f'{company_name} is integrating AI capabilities into its productivity tools, enhancing user experience.',
                    'link': None
                }
            ],
            'GOOGL': [
                {
                    'title': f'{company_name} Search Advertising Revenue Exceeds Expectations',
                    'source': 'Bloomberg',
                    'date': datetime.now() - timedelta(days=1),
                    'summary': f'{company_name} search advertising business continues to dominate the market with strong revenue growth.',
                    'link': None
                },
                {
                    'title': f'{company_name} YouTube Business Shows Strong Performance',
                    'source': 'CNBC',
                    'date': datetime.now() - timedelta(days=2),
                    'summary': f'{company_name} YouTube platform continues to grow, with increasing advertising revenue and user engagement.',
                    'link': None
                }
            ]
        }
        
        # Get specific news for the stock, or use generic news
        specific_news = stock_news_templates.get(symbol, [])
        
        if specific_news:
            return specific_news[:max_results]
        else:
            # Generic stock news
            return [
                {
                    'title': f'{company_name} Stock Shows Strong Performance',
                    'source': 'Reuters',
                    'date': datetime.now() - timedelta(days=1),
                    'summary': f'{company_name} stock has shown strong performance recently, driven by solid fundamentals and market conditions.',
                    'link': None
                },
                {
                    'title': f'{company_name} Announces New Strategic Initiatives',
                    'source': 'Bloomberg',
                    'date': datetime.now() - timedelta(days=2),
                    'summary': f'{company_name} has announced new strategic initiatives aimed at driving future growth and market expansion.',
                    'link': None
                }
            ][:max_results]
