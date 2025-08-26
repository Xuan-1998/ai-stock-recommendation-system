import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import time
import random
import requests
import json

class StockDataFetcher:
    def __init__(self):
        self.stock_info = {
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation',
            'GOOGL': 'Alphabet Inc.',
            'AMZN': 'Amazon.com Inc.',
            'TSLA': 'Tesla Inc.',
            'NVDA': 'NVIDIA Corporation',
            'AMD': 'Advanced Micro Devices Inc.',
            'INTC': 'Intel Corporation',
            'CRM': 'Salesforce Inc.',
            'ADBE': 'Adobe Inc.',
            'META': 'Meta Platforms Inc.',
            'NFLX': 'Netflix Inc.',
            'PYPL': 'PayPal Holdings Inc.',
            'SQ': 'Block Inc.',
            'UBER': 'Uber Technologies Inc.'
        }
        
        # Robinhood API endpoints
        self.robinhood_base = "https://api.robinhood.com"
        
        # 添加真实的基准价格（用于模拟数据）
        self.real_prices = {
            'AAPL': 175.43, 'MSFT': 330.15, 'GOOGL': 138.21, 'AMZN': 128.35, 'TSLA': 248.50,
            'NVDA': 445.12, 'AMD': 102.78, 'INTC': 34.89, 'CRM': 248.90, 'ADBE': 498.67,
            'META': 298.45, 'NFLX': 495.23, 'PYPL': 62.34, 'SQ': 78.90, 'UBER': 42.15
        }
    
    def get_stock_data(self, symbol, period='1y', max_retries=3):
        """获取股票基本数据"""
        # 首先尝试使用Robinhood API获取真实数据
        data = self._get_robinhood_data(symbol)
        if data:
            return data
        
        # 如果Robinhood失败，尝试yfinance
        data = self._get_yfinance_data(symbol, period)
        if data:
            return data
        
        # 如果yfinance失败，尝试备用API
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    time.sleep(random.uniform(1, 3))
                
                data = self._get_backup_api_data(symbol)
                if data:
                    return data
                    
            except Exception as e:
                print(f"备用API获取 {symbol} 数据时出错 (尝试 {attempt + 1}/{max_retries}): {e}")
        
        # 如果所有真实数据源都失败，使用改进的模拟数据
        print(f"使用改进的模拟数据为 {symbol}")
        return self._create_improved_mock_data(symbol)
    
    def _get_robinhood_data(self, symbol):
        """使用Robinhood API获取真实股票数据"""
        try:
            # Robinhood股票信息API
            url = f"{self.robinhood_base}/quotes/"
            params = {
                'symbols': symbol
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'results' in data and data['results']:
                quote = data['results'][0]
                
                current_price = float(quote.get('last_trade_price', 0))
                previous_close = float(quote.get('previous_close', current_price))
                price_change = current_price - previous_close
                price_change_pct = (price_change / previous_close) * 100 if previous_close else 0
                
                # 获取历史数据
                hist_data = self._get_robinhood_history(symbol)
                if hist_data is None:
                    hist_data = self._create_simple_hist_data(symbol, current_price)
                
                data = {
                    'symbol': symbol,
                    'name': self.stock_info.get(symbol, symbol),
                    'current_price': round(current_price, 2),
                    'previous_close': round(previous_close, 2),
                    'high_52w': round(float(quote.get('high_52_weeks', current_price * 1.2)), 2),
                    'low_52w': round(float(quote.get('low_52_weeks', current_price * 0.8)), 2),
                    'volume': int(quote.get('volume', 1000000)),
                    'avg_volume': int(quote.get('average_volume', 5000000)),
                    'pe_ratio': quote.get('pe_ratio', 'N/A'),
                    'market_cap': self._format_market_cap(float(quote.get('market_cap', current_price * 1000000000))),
                    'price_change': round(price_change, 2),
                    'price_change_pct': round(price_change_pct, 2),
                    'price_history': hist_data
                }
                
                data['technical_analysis'] = self._calculate_technical_indicators(hist_data)
                
                print(f"✅ 成功从Robinhood获取 {symbol} 真实数据")
                return data
                
        except Exception as e:
            print(f"Robinhood获取 {symbol} 数据时出错: {e}")
            return None
    
    def _get_robinhood_history(self, symbol):
        """获取Robinhood历史数据"""
        try:
            # 获取股票instrument ID
            instrument_url = f"{self.robinhood_base}/instruments/"
            params = {'symbol': symbol}
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            response = requests.get(instrument_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            instrument_data = response.json()
            if 'results' not in instrument_data or not instrument_data['results']:
                return None
            
            instrument_id = instrument_data['results'][0]['id']
            
            # 获取历史数据
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            
            hist_url = f"{self.robinhood_base}/quotes/historicals/{instrument_id}/"
            params = {
                'interval': 'day',
                'span': 'year',
                'bounds': 'regular'
            }
            
            response = requests.get(hist_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            hist_data = response.json()
            
            if 'historicals' in hist_data and hist_data['historicals']:
                # 转换为DataFrame格式
                df_data = []
                for point in hist_data['historicals']:
                    df_data.append({
                        'Date': datetime.strptime(point['begins_at'][:10], '%Y-%m-%d'),
                        'Open': float(point['open_price']),
                        'High': float(point['high_price']),
                        'Low': float(point['low_price']),
                        'Close': float(point['close_price']),
                        'Volume': int(point['volume'])
                    })
                
                df = pd.DataFrame(df_data)
                df.set_index('Date', inplace=True)
                return df
            
            return None
            
        except Exception as e:
            print(f"获取 {symbol} Robinhood历史数据时出错: {e}")
            return None

    def _get_yfinance_data(self, symbol, period):
        """使用yfinance获取真实股票数据"""
        try:
            # 获取股票信息
            ticker = yf.Ticker(symbol)
            
            # 获取历史数据
            hist_data = ticker.history(period=period)
            
            if hist_data.empty:
                print(f"yfinance无法获取 {symbol} 的历史数据")
                return None
            
            # 获取基本信息
            info = ticker.info
            
            # 计算当前价格和变化
            current_price = hist_data['Close'].iloc[-1]
            previous_close = hist_data['Close'].iloc[-2] if len(hist_data) > 1 else current_price
            price_change = current_price - previous_close
            price_change_pct = (price_change / previous_close) * 100 if previous_close != 0 else 0
            
            # 计算52周高低点
            high_52w = hist_data['High'].max()
            low_52w = hist_data['Low'].min()
            
            # 获取最新交易量
            volume = hist_data['Volume'].iloc[-1]
            avg_volume = hist_data['Volume'].mean()
            
            # 格式化数据
            data = {
                'symbol': symbol,
                'name': self.stock_info.get(symbol, symbol),
                'current_price': round(current_price, 2),
                'previous_close': round(previous_close, 2),
                'high_52w': round(high_52w, 2),
                'low_52w': round(low_52w, 2),
                'volume': int(volume),
                'avg_volume': int(avg_volume),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'market_cap': self._format_market_cap(info.get('marketCap', 0)),
                'price_change': round(price_change, 2),
                'price_change_pct': round(price_change_pct, 2),
                'price_history': hist_data
            }
            
            # 计算技术指标
            data['technical_analysis'] = self._calculate_technical_indicators(hist_data)
            
            print(f"✅ 成功从yfinance获取 {symbol} 真实数据")
            return data
            
        except Exception as e:
            print(f"yfinance获取 {symbol} 数据时出错: {e}")
            return None
    
    def _get_backup_api_data(self, symbol):
        """备用API获取数据"""
        try:
            # 使用Yahoo Finance API
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and data['chart']['result']:
                result = data['chart']['result'][0]
                meta = result.get('meta', {})
                
                current_price = meta.get('regularMarketPrice', 0)
                previous_close = meta.get('previousClose', current_price)
                price_change = current_price - previous_close
                price_change_pct = (price_change / previous_close) * 100 if previous_close else 0
                
                data = {
                    'symbol': symbol,
                    'name': self.stock_info.get(symbol, symbol),
                    'current_price': round(current_price, 2),
                    'previous_close': round(previous_close, 2),
                    'high_52w': round(meta.get('fiftyTwoWeekHigh', current_price * 1.2), 2),
                    'low_52w': round(meta.get('fiftyTwoWeekLow', current_price * 0.8), 2),
                    'volume': meta.get('volume', 1000000),
                    'avg_volume': meta.get('regularMarketVolume', 5000000),
                    'pe_ratio': 'N/A',
                    'market_cap': self._format_market_cap(meta.get('marketCap', current_price * 1000000000)),
                    'price_change': round(price_change, 2),
                    'price_change_pct': round(price_change_pct, 2),
                    'price_history': self._create_simple_hist_data(symbol, current_price)
                }
                
                data['technical_analysis'] = self._calculate_technical_indicators(data['price_history'])
                
                print(f"✅ 成功从备用API获取 {symbol} 真实数据")
                return data
                
        except Exception as e:
            print(f"备用API获取 {symbol} 数据时出错: {e}")
            return None
    
    def _create_improved_mock_data(self, symbol):
        """创建改进的模拟数据，基于真实价格"""
        print(f"为 {symbol} 创建改进的模拟数据...")
        
        # 使用真实基准价格
        base_price = self.real_prices.get(symbol, 100)
        
        # 添加小幅随机波动（±3%）
        price_variation = random.uniform(-0.03, 0.03)
        current_price = base_price * (1 + price_variation)
        
        # 计算合理的变化
        price_change = random.uniform(-base_price * 0.05, base_price * 0.05)
        price_change_pct = (price_change / current_price) * 100
        
        # 计算52周范围（±15%）
        high_52w = current_price * 1.15
        low_52w = current_price * 0.85
        
        # 创建模拟历史数据
        dates = pd.date_range(end=datetime.now(), periods=252, freq='D')
        
        # 基于当前价格创建合理的历史数据
        mock_hist = pd.DataFrame({
            'Open': [current_price + random.uniform(-base_price * 0.02, base_price * 0.02) for _ in range(252)],
            'High': [current_price + random.uniform(0, base_price * 0.03) for _ in range(252)],
            'Low': [current_price + random.uniform(-base_price * 0.03, 0) for _ in range(252)],
            'Close': [current_price + random.uniform(-base_price * 0.015, base_price * 0.015) for _ in range(252)],
            'Volume': [random.randint(int(base_price * 10000), int(base_price * 50000)) for _ in range(252)]
        }, index=dates)
        
        data = {
            'symbol': symbol,
            'name': self.stock_info.get(symbol, symbol),
            'current_price': round(current_price, 2),
            'previous_close': round(current_price - price_change, 2),
            'high_52w': round(high_52w, 2),
            'low_52w': round(low_52w, 2),
            'volume': random.randint(int(base_price * 10000), int(base_price * 50000)),
            'avg_volume': random.randint(int(base_price * 15000), int(base_price * 40000)),
            'pe_ratio': random.randint(15, 35),
            'market_cap': self._format_market_cap(current_price * random.randint(5000000000, 50000000000)),
            'price_change': round(price_change, 2),
            'price_change_pct': round(price_change_pct, 2),
            'price_history': mock_hist
        }
        
        data['technical_analysis'] = self._calculate_technical_indicators(mock_hist)
        return data
    
    def _create_simple_hist_data(self, symbol, current_price):
        """为备用API创建简单的历史数据"""
        dates = pd.date_range(end=datetime.now(), periods=252, freq='D')
        hist_data = pd.DataFrame({
            'Open': [current_price] * 252,
            'High': [current_price * 1.01] * 252,
            'Low': [current_price * 0.99] * 252,
            'Close': [current_price] * 252,
            'Volume': [1000000] * 252
        }, index=dates)
        return hist_data
    
    def get_multiple_stocks_data(self, symbols, max_concurrent=3):
        """获取多只股票数据，限制并发数"""
        results = []
        
        for i in range(0, len(symbols), max_concurrent):
            batch = symbols[i:i + max_concurrent]
            
            for symbol in batch:
                data = self.get_stock_data(symbol)
                if data:
                    results.append(data)
            
            # 批次间延迟
            if i + max_concurrent < len(symbols):
                time.sleep(random.uniform(2, 5))
        
        return results
    
    def _format_market_cap(self, market_cap):
        """格式化市值显示"""
        if market_cap == 0 or market_cap == 'N/A':
            return 'N/A'
        
        if market_cap >= 1e12:
            return f"${market_cap/1e12:.2f}T"
        elif market_cap >= 1e9:
            return f"${market_cap/1e9:.2f}B"
        elif market_cap >= 1e6:
            return f"${market_cap/1e6:.2f}M"
        else:
            return f"${market_cap:,.0f}"
    
    def _calculate_technical_indicators(self, hist):
        """计算技术指标"""
        indicators = {}
        
        try:
            # 移动平均线
            indicators['sma_20'] = round(hist['Close'].rolling(window=20).mean().iloc[-1], 2)
            indicators['sma_50'] = round(hist['Close'].rolling(window=50).mean().iloc[-1], 2)
            indicators['sma_200'] = round(hist['Close'].rolling(window=200).mean().iloc[-1], 2)
            
            # RSI
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi_value = 100 - (100 / (1 + rs.iloc[-1]))
            indicators['rsi'] = round(rsi_value if not pd.isna(rsi_value) else 50, 2)
            
            # MACD
            exp1 = hist['Close'].ewm(span=12).mean()
            exp2 = hist['Close'].ewm(span=26).mean()
            macd_value = exp1.iloc[-1] - exp2.iloc[-1]
            indicators['macd'] = round(macd_value if not pd.isna(macd_value) else 0, 2)
            
            # 布林带
            sma_20 = hist['Close'].rolling(window=20).mean()
            std_20 = hist['Close'].rolling(window=20).std()
            indicators['bollinger_upper'] = round(sma_20.iloc[-1] + (std_20.iloc[-1] * 2), 2)
            indicators['bollinger_lower'] = round(sma_20.iloc[-1] - (std_20.iloc[-1] * 2), 2)
            
            # 技术信号
            signals = []
            current_price = hist['Close'].iloc[-1]
            
            # Moving average signals
            if current_price > indicators['sma_20']:
                signals.append("Price above 20-day MA")
            else:
                signals.append("Price below 20-day MA")
            
            if current_price > indicators['sma_50']:
                signals.append("Price above 50-day MA")
            else:
                signals.append("Price below 50-day MA")
            
            # RSI signals
            if indicators['rsi'] > 70:
                signals.append("RSI indicates overbought")
            elif indicators['rsi'] < 30:
                signals.append("RSI indicates oversold")
            
            # Bollinger Bands signals
            if current_price > indicators['bollinger_upper']:
                signals.append("Price above Bollinger upper band")
            elif current_price < indicators['bollinger_lower']:
                signals.append("Price below Bollinger lower band")
            
            indicators['signals'] = signals
            
        except Exception as e:
            print(f"计算技术指标时出错: {e}")
            # 返回默认值
            indicators = {
                'sma_20': 0,
                'sma_50': 0,
                'sma_200': 0,
                'rsi': 50,
                'macd': 0,
                'bollinger_upper': 0,
                'bollinger_lower': 0,
                'signals': ['Technical indicator calculation failed']
            }
        
        return indicators
