import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import time
import os

from stock_data import StockDataFetcher
from news_collector import NewsCollector
from gemini_analyzer import GeminiAnalyzer
from config import DEFAULT_TECH_STOCKS, GEMINI_API_KEY

# Page configuration
st.set_page_config(
    page_title="AI Stock Recommendation System",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styles
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .recommendation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    .buy {
        border-left: 4px solid #28a745;
        background-color: #d4edda;
    }
    .sell {
        border-left: 4px solid #dc3545;
        background-color: #f8d7da;
    }
    .hold {
        border-left: 4px solid #ffc107;
        background-color: #fff3cd;
    }
    .api-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_api_key():
    """Check if API key is valid"""
    api_key = st.session_state.get('gemini_api_key', GEMINI_API_KEY)
    return api_key and api_key.strip() != ''

def setup_api_key():
    """Setup API key"""
    # Check if API key exists
    current_api_key = st.session_state.get('gemini_api_key', GEMINI_API_KEY)
    
    # If no API key, show input interface
    if not current_api_key:
        st.markdown("## 🔑 Welcome to AI Stock Recommendation System")
        st.markdown("### First-time setup requires Gemini API key")
        
        st.info("""
        **Steps to get API key:**
        1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Sign in to your Google account
        3. Click "Create API Key" to create a new API key
        4. Copy the API key and paste it in the input box below
        """)
        
        # Main interface API key input
        api_key = st.text_input(
            "Enter your Gemini API key:",
            type="password",
            placeholder="AIzaSyC...",
            help="Your API key will be stored securely and won't be uploaded anywhere"
        )
        
        if st.button("🔑 Set API Key", type="primary"):
            if api_key and len(api_key) > 10:
                # Test API key
                with st.spinner("Validating API key..."):
                    try:
                        import google.generativeai as genai
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content("Hello")
                        st.session_state.gemini_api_key = api_key
                        st.success("✅ API key validation successful! System is ready.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ API key validation failed: {str(e)}")
                        st.error("Please check if the API key is correct, or visit https://makersuite.google.com/app/apikey to get a new API key")
            else:
                st.error("Please enter a valid API key")
        
        st.stop()  # Stop execution, wait for user input
    
    # Sidebar API settings
    st.sidebar.markdown("## 🔑 API Settings")
    
    # Show current API key status
    if current_api_key:
        st.sidebar.success("✅ API key is set")
        if st.sidebar.button("🔄 Change API Key"):
            st.session_state.gemini_api_key = ""
            st.rerun()
    
    # Test API connection
    if st.sidebar.button("🧪 Test API Connection"):
        try:
            import google.generativeai as genai
            genai.configure(api_key=current_api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Hello")
            st.sidebar.success("✅ API connection successful!")
        except Exception as e:
            st.sidebar.error(f"❌ API connection failed: {str(e)}")
    
    return current_api_key

class StockRecommendationApp:
    def __init__(self):
        self.stock_fetcher = StockDataFetcher()
        self.news_collector = NewsCollector()
        self.gemini_analyzer = None  # Lazy initialization
        
    def get_analyzer(self):
        """Get analyzer instance"""
        if self.gemini_analyzer is None:
            api_key = st.session_state.get('gemini_api_key', GEMINI_API_KEY)
            if api_key:
                try:
                    self.gemini_analyzer = GeminiAnalyzer(api_key)
                except Exception as e:
                    st.error(f"Failed to initialize AI analyzer: {e}")
                    return None
            else:
                st.error("Please set Gemini API key first")
                return None
        return self.gemini_analyzer
        
    def run(self):
        # Setup API key
        api_key = setup_api_key()
        
        # Main title
        st.markdown('<h1 class="main-header">🤖 AI Stock Recommendation System</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Intelligent stock analysis platform powered by Gemini AI</p>', unsafe_allow_html=True)
        
        # Sidebar
        self.sidebar()
        
        # Main content area
        if 'selected_stock' in st.session_state and st.session_state.selected_stock:
            self.analyze_single_stock(st.session_state.selected_stock)
        else:
            self.dashboard()
    
    def sidebar(self):
        """Sidebar configuration"""
        st.sidebar.markdown("## 📊 Stock Selection")
        
        # Stock selection
        stock_symbol = st.sidebar.selectbox(
            "Select stock to analyze:",
            ["Select Stock"] + DEFAULT_TECH_STOCKS,
            key="stock_selector"
        )
        
        if stock_symbol != "Select Stock":
            st.session_state.selected_stock = stock_symbol
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("## ⚙️ Settings")
        
        # Analysis depth selection
        analysis_depth = st.sidebar.selectbox(
            "Analysis depth:",
            ["Quick Analysis", "Detailed Analysis", "Deep Analysis"]
        )
        
        # News time range
        news_range = st.sidebar.selectbox(
            "News time range:",
            ["Last 3 days", "Last 7 days", "Last 30 days"]
        )
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 📈 Market Overview")
        
        # Show market indices
        if st.sidebar.button("🔄 Refresh Market Data"):
            self.show_market_overview()
    
    def dashboard(self):
        """Main dashboard"""
        st.markdown("## 📈 Popular Tech Stocks Overview")
        
        # Get all stock data
        with st.spinner("Fetching stock data..."):
            stocks_data = self.stock_fetcher.get_multiple_stocks_data(DEFAULT_TECH_STOCKS[:6])
            
            # If unable to get real data, show warning
            if not stocks_data:
                st.warning("⚠️ Unable to fetch real-time stock data, please check network connection")
                return
        
        if stocks_data:
            # Create stock card grid
            cols = st.columns(3)
            for i, stock in enumerate(stocks_data):
                with cols[i % 3]:
                    self.display_stock_card(stock)
        
        st.markdown("---")
        
        # Market sentiment analysis
        st.markdown("## 🧠 Market Sentiment Analysis")
        if st.button("Analyze Market Sentiment"):
            with st.spinner("Analyzing market sentiment..."):
                tech_news = self.news_collector.get_tech_market_news(use_mock=True)  # Use mock data
                analyzer = self.get_analyzer()
                if analyzer:
                    sentiment = analyzer.get_market_sentiment(tech_news)
                    st.markdown(sentiment)
                else:
                    # Show mock market sentiment analysis
                    st.info("🔧 Demo mode: Showing mock market sentiment analysis")
                    st.markdown("""
                    **Market Sentiment Analysis Results:**
                    
                    **Overall Market Sentiment:** Neutral to Bullish
                    
                    **Key Drivers:**
                    - AI technology development driving tech stock gains
                    - Strong earnings from chip manufacturers
                    - Continued growth in cloud computing services
                    
                    **Impact on Tech Stocks:**
                    - Large tech stocks performing steadily
                    - AI-related stocks attracting investor attention
                    - Semiconductor sector expected to continue strong performance
                    
                    **Key Risks for Investors to Watch:**
                    - Regulatory policy changes
                    - Interest rate environment uncertainty
                    - Geopolitical risks
                    """)
    
    def analyze_single_stock(self, symbol):
        """Analyze single stock"""
        st.markdown(f"## 📊 {symbol} Detailed Analysis")
        
        # Get stock data
        with st.spinner(f"Fetching {symbol} data..."):
            stock_data = self.stock_fetcher.get_stock_data(symbol)
        
        if not stock_data:
            st.error(f"Unable to fetch {symbol} data")
            return
        
        # Display basic information
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Current Price",
                f"${stock_data['current_price']}",
                f"{stock_data['price_change_pct']:.2f}%"
            )
        
        with col2:
            st.metric("52-Week High", f"${stock_data['high_52w']}")
        
        with col3:
            st.metric("52-Week Low", f"${stock_data['low_52w']}")
        
        with col4:
            st.metric("Market Cap", stock_data['market_cap'])
        
        # Price chart
        self.display_price_chart(stock_data)
        
        # Technical indicators
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Technical Indicators")
            tech_analysis = stock_data['technical_analysis']
            
            metrics_df = pd.DataFrame([
                ["20-Day MA", f"${tech_analysis['sma_20']}"],
                ["50-Day MA", f"${tech_analysis['sma_50']}"],
                ["200-Day MA", f"${tech_analysis['sma_200']}"],
                ["RSI", f"{tech_analysis['rsi']}"],
                ["MACD", f"{tech_analysis['macd']}"],
                ["Bollinger Upper", f"${tech_analysis['bollinger_upper']}"],
                ["Bollinger Lower", f"${tech_analysis['bollinger_lower']}"]
            ], columns=["Indicator", "Value"])
            
            st.dataframe(metrics_df, use_container_width=True)
            
            if tech_analysis['signals']:
                st.markdown("#### 🚦 Technical Signals")
                for signal in tech_analysis['signals']:
                    st.markdown(f"- {signal}")
        
        with col2:
            st.markdown("### 📰 Related News")
            with st.spinner("Fetching related news..."):
                news_data = self.news_collector.get_stock_specific_news(
                    symbol, stock_data['name'], use_mock=True  # Use mock data to avoid network issues
                )
            
            if news_data:
                for i, news in enumerate(news_data[:5]):
                    st.markdown(f"""
                    **{i+1}. {news['title']}**
                    
                    *Source: {news['source']} | {news['date'].strftime('%Y-%m-%d')}*
                    
                    {news.get('summary', '')[:100]}...
                    
                    {f"[Read More]({news['link']})" if news.get('link') else "Read More (Demo)"}
                    
                    ---
                    """)
            else:
                st.markdown("No related news available")
        
        # AI analysis
        st.markdown("---")
        st.markdown("## 🤖 AI Recommendation Analysis")
        
        if not check_api_key():
            st.error("Please set Gemini API key in the sidebar to enable AI analysis")
            return
        
        if st.button("Start AI Analysis", type="primary"):
            with st.spinner("AI is analyzing stock data..."):
                # Get news data (if not already)
                if 'news_data' not in locals():
                    news_data = self.news_collector.get_stock_specific_news(
                        symbol, stock_data['name'], use_mock=True  # Use mock data
                    )
                
                # Perform AI analysis
                analyzer = self.get_analyzer()
                if analyzer:
                    analysis_result = analyzer.analyze_stock(stock_data, news_data)
                    
                    # Display analysis results
                    self.display_analysis_result(analysis_result, stock_data)
                else:
                    # Use demo mode
                    st.info("🔧 Demo mode: Showing mock AI analysis results")
                    analysis_result = self.get_demo_analysis(stock_data)
                    self.display_analysis_result(analysis_result, stock_data)
    
    def get_demo_analysis(self, stock_data):
        """Get demo mode AI analysis results"""
        symbol = stock_data['symbol']
        current_price = stock_data['current_price']
        
        # Generate different demo analysis based on stock code
        demo_analyses = {
            'AAPL': {
                'action': 'Buy',
                'target_price': f'${current_price * 1.15:.2f}',
                'risk_level': 'Medium',
                'reasoning': 'Apple Inc. as a tech giant shows strong performance in smartphones, services business, and wearable devices. The company has strong brand value and stable cash flow with good long-term growth prospects.',
                'risks': 'Faces regulatory risks, supply chain disruption risks, and intensified market competition risks. Global economic uncertainty may affect consumer spending.',
                'raw_response': f"""
Based on the analysis of {symbol}, we provide the following investment recommendation:

**Recommendation: Buy**
**Target Price: {current_price * 1.15:.2f}**
**Risk Level: Medium**

**Investment Rationale:**
- Strong brand value and market position
- Rapid growth in services business, improving profit margins
- Continuous innovation in product lines
- Stable cash flow and financial condition

**Risk Warnings:**
- Regulatory environment changes may bring challenges
- Supply chain risks need attention
- Market competition is increasingly fierce
- Global economic uncertainty affects demand
                """
            },
            'MSFT': {
                'action': 'Hold',
                'target_price': f'${current_price * 1.08:.2f}',
                'risk_level': 'Low',
                'reasoning': 'Microsoft performs excellently in cloud computing and enterprise software, with strong Azure business growth. The company has stable financial condition and is a relatively safe investment choice.',
                'risks': 'Intense competition in cloud computing market, regulatory review may strengthen. Technology changes may affect existing business models.',
                'raw_response': f"""
Based on the analysis of {symbol}, we provide the following investment recommendation:

**Recommendation: Hold**
**Target Price: {current_price * 1.08:.2f}**
**Risk Level: Low**

**Investment Rationale:**
- Strong growth in Azure cloud computing business
- Leadership position in enterprise software market
- Stable subscription revenue model
- Strong R&D investment

**Risk Warnings:**
- Intensified cloud computing market competition
- Regulatory review may strengthen
- Technology change risks
- Macroeconomic impacts
                """
            },
            'GOOGL': {
                'action': 'Buy',
                'target_price': f'${current_price * 1.12:.2f}',
                'risk_level': 'Medium',
                'reasoning': 'Google dominates the search and advertising market with rapid AI technology development. YouTube and cloud business have huge growth potential.',
                'risks': 'Cyclical fluctuations in advertising market, increasing regulatory pressure, intense AI competition.',
                'raw_response': f"""
Based on the analysis of {symbol}, we provide the following investment recommendation:

**Recommendation: Buy**
**Target Price: {current_price * 1.12:.2f}**
**Risk Level: Medium**

**Investment Rationale:**
- Dominant position in search advertising market
- Leading advantage in AI technology
- Strong YouTube business growth
- Diversified revenue sources

**Risk Warnings:**
- Cyclical risks in advertising market
- Continuously increasing regulatory pressure
- Intense competition in AI field
- Privacy protection challenges
                """
            }
        }
        
        # Return default analysis or specific stock analysis
        return demo_analyses.get(symbol, {
            'action': 'Hold',
            'target_price': f'${current_price * 1.05:.2f}',
            'risk_level': 'Medium',
            'reasoning': f'{symbol} as a tech stock has long-term growth potential, but market volatility and industry competition need attention.',
            'risks': 'Market volatility risks, intensified industry competition, macroeconomic uncertainty.',
            'raw_response': f"""
Based on the analysis of {symbol}, we provide the following investment recommendation:

**Recommendation: Hold**
**Target Price: {current_price * 1.05:.2f}**
**Risk Level: Medium**

**Investment Rationale:**
- Long-term growth prospects in tech industry
- Stable company fundamentals
- Relatively stable industry position

**Risk Warnings:**
- Market volatility risks
- Intensified industry competition
- Macroeconomic uncertainty
            """
        })
    
    def display_stock_card(self, stock):
        """Display stock card"""
        change_color = "green" if stock['price_change_pct'] >= 0 else "red"
        
        st.markdown(f"""
        <div class="metric-card">
            <h4>{stock['symbol']} - {stock['name']}</h4>
            <p><strong>${stock['current_price']}</strong></p>
            <p style="color: {change_color};">{stock['price_change_pct']:+.2f}%</p>
            <p>Market Cap: {stock['market_cap']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def display_price_chart(self, stock_data):
        """Display price chart"""
        hist = stock_data['price_history']
        
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3]
        )
        
        # Price and moving averages
        fig.add_trace(
            go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name='Price'
            ),
            row=1, col=1
        )
        
        # Add moving averages
        sma_20 = hist['Close'].rolling(window=20).mean()
        sma_50 = hist['Close'].rolling(window=50).mean()
        
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=sma_20,
                name='20-Day MA',
                line=dict(color='orange')
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=hist.index,
                y=sma_50,
                name='50-Day MA',
                line=dict(color='purple')
            ),
            row=1, col=1
        )
        
        # Volume
        fig.add_trace(
            go.Bar(
                x=hist.index,
                y=hist['Volume'],
                name='Volume',
                marker_color='lightblue'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title=f"{stock_data['symbol']} Price Chart",
            xaxis_rangeslider_visible=False,
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_analysis_result(self, analysis_result, stock_data):
        """Display AI analysis results"""
        # Determine color theme
        action = analysis_result['action']
        if action == 'Buy':
            theme_class = 'buy'
            icon = '🟢'
        elif action == 'Sell':
            theme_class = 'sell'
            icon = '🔴'
        else:
            theme_class = 'hold'
            icon = '🟡'
        
        # Recommendation card
        st.markdown(f"""
        <div class="recommendation-card">
            <h3>{icon} AI Recommendation: {action}</h3>
            <p><strong>Target Price:</strong> {analysis_result['target_price']}</p>
            <p><strong>Risk Level:</strong> {analysis_result['risk_level']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Analysis details
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💡 Investment Rationale")
            st.markdown(analysis_result['reasoning'])
        
        with col2:
            st.markdown("### ⚠️ Risk Warnings")
            st.markdown(analysis_result['risks'])
        
        # Complete analysis
        with st.expander("📋 Complete Analysis Report"):
            st.markdown(analysis_result['raw_response'])
    
    def show_market_overview(self):
        """Show market overview"""
        st.markdown("## 📊 Market Indices")
        
        # Get major index data
        indices = ['^GSPC', '^IXIC', '^DJI']  # S&P500, NASDAQ, Dow Jones
        
        for index in indices:
            try:
                data = self.stock_fetcher.get_stock_data(index, period='5d')
                if data:
                    st.metric(
                        f"{index} Index",
                        f"{data['current_price']:.2f}",
                        f"{data['price_change_pct']:.2f}%"
                    )
            except:
                continue

if __name__ == "__main__":
    app = StockRecommendationApp()
    app.run()
