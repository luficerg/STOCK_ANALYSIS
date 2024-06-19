import pandas as pd

def simulate_trades(stock_data, trading_signals, capital):
    """
    This function simulates trades based on trading signals and initial capital.

    Args:
    stock_data (DataFrame): A pandas DataFrame containing stock price data.
    trading_signals (Series): A pandas Series containing trading signals.
    capital (float): The initial capital for trading.

    Returns:
    DataFrame: A pandas DataFrame containing the portfolio of trades.
    """
    # Initialize the portfolio and variables for tracking position and trading details
    portfolio = []
    position = 0
    buy_price = 0
    quantity = 0

    # Iterate through the stock prices by date
    for date, price in stock_data['Close'].items():
        # Check if there is a trading signal for the current date
        if date in trading_signals.index:
            signal = trading_signals.loc[date]
            
            # Execute buy signal if no position is held
            if signal == 1 and position == 0:
                position = 1
                buy_price = price
                quantity = capital / price
                capital = capital % price
                profit = 0
                portfolio.append({"date": date, "type": "buy", "price": buy_price, "capital": capital,'profit': profit})
            
            # Execute sell signal if a position is held and the sell price is higher than the buy price
            elif signal == -1 and position == 1 and (price > buy_price):
                position = 0
                sell_price = price
                profit = (sell_price - buy_price) * quantity
                capital = capital + quantity * sell_price
                portfolio.append({"date": date, "type": "sell", "price": sell_price, "capital": capital, "profit": profit})

    # Return the portfolio as a DataFrame
    return pd.DataFrame(portfolio)
