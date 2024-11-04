import time
import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame


# Alpaca API keys
API_KEY = '...'
API_SECRET = '...'
BASE_URL = '...'


# Trading parameters
stock1 = 'VOO'
stock2 = 'QQQ'
Z_BUY = 1.7
Z_SELL = 2.4
WINDOW = 11
QUANTITY = 100


def spread_z_score(stock1_prices: pd.Series, stock2_prices: pd.Series, window=WINDOW):
    spread = stock1_prices - stock2_prices
    rolling_mean = spread.rolling(window=window).mean()
    rolling_std = spread.rolling(window=window).std()
    z_score = (spread - rolling_mean) / rolling_std
    return z_score.dropna()


def strategy(stock1_prices, stock2_prices):
    current_spread_score = spread_z_score(stock1_prices, stock2_prices).iloc[-1]
    if current_spread_score > Z_SELL:
        return -1
    if current_spread_score < Z_BUY:
        return 1
    return 0


def fetch_stock_data(data_client, symbol, timeframe, limit):
    request_params = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=timeframe,
        limit=limit
    )
    bars = data_client.get_stock_bars(request_params).df
    return bars['close']


def run():
    # Initialize Alpaca clients
    trading_client = TradingClient(API_KEY, API_SECRET, paper=True, url_override=BASE_URL)
    data_client = StockHistoricalDataClient(API_KEY, API_SECRET)
    # Account information
    account = trading_client.get_account()
    print(f'${account.cash} of cash.\n${account.buying_power} is available as buying power.')
    balance_change = float(account.equity) - float(account.last_equity)
    print(f'Today\'s portfolio balance change: ${balance_change}')
    # File to store trading data
    filename = 'trading_data.pkl'
    # Initialize DataFrame for storing data
    try:
        df = pd.read_pickle(filename)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['timestamp', 'stock1_price', 'stock2_price', 'spread_z_score', 'action'])

    while True:
        try:
            if time.time() % 60 == 0:
                # Fetch recent stock price data
                stock1_prices = fetch_stock_data(data_client, stock1, TimeFrame.Minute, WINDOW + 1)
                stock2_prices = fetch_stock_data(data_client, stock2, TimeFrame.Minute, WINDOW + 1)
                suggestion = strategy(stock1_prices, stock2_prices)
                timestamp = pd.Timestamp.now()
                if suggestion == 0:  # No action
                    df = df.append({'timestamp': timestamp, 'stock1_price':stock1_prices.iloc[-1],
                                    'stock2_price': stock2_prices.iloc[-1],
                                    'spread_z_score':spread_z_score(stock1_prices, stock2_prices).iloc[-1],
                                    'action': 'none'},ignore_index=True)
                    df.to_pickle(filename)
                    continue
                # Determine order sides
                stock1side = OrderSide.BUY if suggestion == 1 else OrderSide.SELL
                stock2side = OrderSide.SELL if suggestion == 1 else OrderSide.BUY
                # Create market orders
                stock1_morder = MarketOrderRequest(
                    symbol=stock1,
                    qty=QUANTITY,
                    side=stock1side,
                    time_in_force=TimeInForce.DAY
                )
                stock2_morder = MarketOrderRequest(
                    symbol=stock2,
                    qty=QUANTITY,
                    side=stock2side,
                    time_in_force=TimeInForce.DAY
)
                # Place orders
                stock1_order = trading_client.submit_order(order_data=stock1_morder)
                stock2_order = trading_client.submit_order(order_data=stock2_morder)
                # Log the trade data
                action = 'buy' if suggestion == 1 else 'sell'
                df = df.append({'timestamp': timestamp, 'stock1_price':stock1_prices.iloc[-1],
                                'stock2_price': stock2_prices.iloc[-1],
                                'spread_z_score':spread_z_score(stock1_prices, stock2_prices).iloc[-1],
                                'action': action},ignore_index=True)
                df.to_pickle(filename)
                print(f"Orders placed: {stock1_order}, {stock2_order}")
        except Exception as err:
            print(f"***DIAG: {err}")


if __name__ == '__main__':
    run()
