#!/usr/bin/env python3

from stock_data import StockDataFetcher

def test_stock_data():
    fetcher = StockDataFetcher()
    
    # 测试获取GOOGL数据
    print("正在获取GOOGL股票数据...")
    data = fetcher.get_stock_data('GOOGL')
    
    if data:
        print(f"✅ 成功获取GOOGL数据:")
        print(f"   当前价格: ${data['current_price']}")
        print(f"   价格变化: ${data['price_change']} ({data['price_change_pct']:.2f}%)")
        print(f"   52周高: ${data['high_52w']}")
        print(f"   52周低: ${data['low_52w']}")
        print(f"   市值: {data['market_cap']}")
        print(f"   成交量: {data['volume']:,}")
        return True
    else:
        print("❌ 获取GOOGL数据失败")
        return False

if __name__ == "__main__":
    test_stock_data()
