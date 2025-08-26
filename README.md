# 🚀 Tech Stocks Investment Analyzer

A comprehensive tech-focused investment analysis platform powered by Google's Gemini AI, providing real-time stock data analysis, technical indicators, and AI-powered investment recommendations specifically for technology stocks.
<img width="948" height="463" alt="Screenshot 2025-08-25 at 9 13 46 PM" src="https://github.com/user-attachments/assets/fe166e41-b6aa-4967-b45f-612160e6312f" />
<img width="936" height="476" alt="Screenshot 2025-08-25 at 9 13 53 PM" src="https://github.com/user-attachments/assets/ede25ed7-fdb2-4520-9e12-47a5391fd3db" />


## ✨ Features

- **Tech Stocks Focus**: Specialized analysis for technology sector stocks
- **Real-time Stock Data**: Fetch live stock prices and market data
- **Technical Analysis**: Calculate and display key technical indicators (RSI, MACD, Moving Averages, Bollinger Bands)
- **AI-Powered Analysis**: Get intelligent buy/sell recommendations using Google's Gemini AI
- **News Integration**: Latest tech market news and company-specific updates
- **Interactive Charts**: Beautiful price charts with technical indicators
- **Market Sentiment**: AI analysis of overall market sentiment
- **Congress Trading Signals**: Nancy Pelosi's trading activity analysis
- **Demo Mode**: Works without API keys using mock data for demonstration

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Gemini API key (optional for demo mode)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Xuan-1998/tech-stocks-investment-analyzer.git
   cd tech-stocks-investment-analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key (Optional)**
   
   **Option 1: In-app setup (Recommended)**
   - Run the application
   - Enter your API key when prompted
   - The key will be stored securely in session state
   
   **Option 2: Environment variable**
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```
   
   **Option 3: .env file**
   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

4. **Run the application**
   ```bash
   python3 -m streamlit run app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - The application will guide you through the setup process

## 📊 How to Use

### 1. API Key Setup
- If you don't have an API key, the app will show setup instructions
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey) to get a free API key
- Enter the key in the app interface

### 2. Stock Selection
- Choose from popular tech stocks in the sidebar
- Select analysis depth and news time range
- Click on any stock to view detailed analysis

### 3. Analysis Features
- **Real-time Data**: Current price, 52-week range, market cap
- **Technical Indicators**: RSI, MACD, moving averages, Bollinger Bands
- **Price Charts**: Interactive candlestick charts with volume
- **AI Recommendations**: Buy/sell/hold recommendations with target prices
- **Risk Assessment**: Risk levels and detailed risk warnings
- **News Analysis**: Latest company and market news

### 4. Market Overview
- View popular tech stocks at a glance
- Analyze overall market sentiment
- Track major market indices

## 🔧 Configuration

### Tech Stocks List
Edit `config.py` to customize the default tech stocks list:
```python
DEFAULT_TECH_STOCKS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
    'NVDA', 'AMD', 'INTC', 'CRM', 'ADBE',
    'META', 'NFLX', 'PYPL', 'SQ', 'UBER'
]
```

### Analysis Settings
- **Analysis Depth**: Quick, Detailed, or Deep analysis
- **News Range**: Last 3, 7, or 30 days
- **Technical Indicators**: Customizable calculation parameters

## 📁 Project Structure

```
ai-stock-recommendation-system/
├── app.py                 # Main Streamlit application
├── config.py              # Configuration and settings
├── stock_data.py          # Stock data fetching and analysis
├── news_collector.py      # News collection and processing
├── gemini_analyzer.py     # AI analysis using Gemini
├── requirements.txt       # Python dependencies
├── run.sh                 # Quick start script
└── README.md             # This file
```

## 🛠️ Technical Details

### Data Sources
- **Stock Data**: Yahoo Finance API (yfinance)
- **News**: Multiple sources with fallback to mock data
- **AI Analysis**: Google Gemini AI (gemini-1.5-flash model)

### Key Features
- **Robust Error Handling**: Graceful fallbacks when APIs fail
- **Mock Data Support**: Demo mode works without real data
- **Real-time Updates**: Live stock prices and market data
- **Responsive Design**: Works on desktop and mobile devices

### Performance Optimizations
- **Caching**: Session state caching for API responses
- **Rate Limiting**: Built-in delays to avoid API limits
- **Concurrent Requests**: Efficient data fetching for multiple stocks

## 🔒 Security & Privacy

- API keys are stored securely in session state
- No data is uploaded or stored permanently
- All analysis is performed locally or through secure APIs
- Mock data is used when real data is unavailable

## 🚨 Troubleshooting

### Common Issues

**1. API Key Not Working**
- Verify your API key at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Ensure you have quota available
- Check if the key has proper permissions

**2. Stock Data Not Loading**
- Check your internet connection
- The app will use mock data if real data is unavailable
- Try refreshing the page

**3. Application Won't Start**
- Ensure Python 3.8+ is installed
- Install all dependencies: `pip install -r requirements.txt`
- Check if port 8501 is available

**4. Performance Issues**
- Close other applications using the same port
- Restart the application
- Check system resources

### Getting Help

1. **Check the logs** in the terminal for error messages
2. **Verify API key** using the test function in the sidebar
3. **Try demo mode** if API key issues persist
4. **Check network connection** for data fetching issues

## 📈 Demo Mode

The application includes a comprehensive demo mode that works without any API keys:

- **Mock Stock Data**: Realistic stock prices and technical indicators
- **Demo AI Analysis**: Sample investment recommendations
- **Mock News**: Simulated market news and company updates
- **Full Functionality**: All features work in demo mode

To use demo mode:
1. Start the application without setting an API key
2. The app will automatically use mock data
3. All analysis features will work with simulated data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent analysis capabilities
- **Yahoo Finance** for real-time stock data
- **Streamlit** for the beautiful web interface
- **Plotly** for interactive charts and visualizations

## 📞 Support

For support and questions:
- Check the troubleshooting section above
- Review the application logs
- Ensure all dependencies are properly installed

---

**Note**: This application is for educational and demonstration purposes. Always do your own research and consult with financial advisors before making investment decisions.
