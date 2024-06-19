import plotly.graph_objects as go

def calculate_portfolio_metrics(portfolio):
    """
    This function calculates key metrics for a given trading portfolio.

    Args:
    portfolio (DataFrame): A pandas DataFrame containing the portfolio trades.

    Returns:
    tuple: A tuple containing the total number of trades, the win percentage, the total profit, loss_percentage, and the total loss.
    """
    # Calculate the total number of trades (each trade consists of a buy and a sell)
    total_trades = len(portfolio) // 2

    # Calculate the number of winning trades (sell trades with a positive profit)
    wins = portfolio[portfolio['type'] == 'sell']['profit'] > 0
    loss = portfolio[portfolio['type'] == 'sell']['profit'] < 0
    
    # Calculate the win percentage
    win_percentage = wins.mean() * 100
    loss_percentage = loss.mean() * 100
    
    # Calculate the total profit from sell trades
    total_profit = portfolio[portfolio['type'] == 'sell']['profit'].sum()
    total_loss = portfolio[portfolio['type'] == 'sell']['profit'].sum()
    
    # Return the total trades, win percentage, and total profit
    return total_trades, win_percentage, total_profit, loss_percentage, total_loss

def calculate_sharpe_ratio(portfolio, risk_free_rate=0.01):
    """
    This function calculates the Sharpe Ratio for the portfolio.

    Args:
    portfolio (DataFrame): A pandas DataFrame containing the portfolio trades.
    risk_free_rate (float): The risk-free rate of return (default is 0.01).

    Returns:
    float: The Sharpe Ratio of the portfolio.
    """
    # Get the daily returns from the sell trades
    daily_returns = portfolio[portfolio['type'] == 'sell']['profit']
    
    # Calculate the excess returns by subtracting the risk-free rate
    excess_returns = daily_returns - risk_free_rate
    
    # Calculate the Sharpe Ratio
    sharpe_ratio = excess_returns.mean() / excess_returns.std()
    
    # Return the Sharpe Ratio
    return sharpe_ratio

def calculate_max_drawdown(portfolio):
    """
    This function calculates the maximum drawdown for the portfolio.

    Args:
    portfolio (DataFrame): A pandas DataFrame containing the portfolio trades.

    Returns:
    float: The maximum drawdown value.
    """
    # Calculate the cumulative profit over time
    portfolio['cumulative_profit'] = portfolio['profit'].cumsum()
    
    # Calculate the cumulative maximum profit
    cumulative_max = portfolio['cumulative_profit'].cummax()
    
    # Calculate the drawdown
    drawdown = portfolio['cumulative_profit'] - cumulative_max
    
    # Get the maximum drawdown
    max_drawdown = drawdown.min()
    
    # Return the maximum drawdown
    return max_drawdown

def plot_signals(stock_data, portfolio, ticker):
    """
    This function plots stock prices along with buy and sell signals for a given ticker.

    Args:
    stock_data (DataFrame): A pandas DataFrame containing the stock price data.
    portfolio (DataFrame): A pandas DataFrame containing the portfolio trades.
    ticker (str): The stock ticker symbol.

    Returns:
    PLOT: Returns an interactive plot using Plotly.
    """
    # Get the start and end dates from the portfolio
    start_date = portfolio['date'].min()
    end_date = portfolio['date'].max()

    # Filter the stock data to the date range available in the portfolio
    stock_data = stock_data[(stock_data.index >= start_date) & (stock_data.index <= end_date)]
    
    # Separate buy and sell signals from the portfolio
    buy_signals = portfolio[portfolio['type'] == 'buy']
    sell_signals = portfolio[portfolio['type'] == 'sell']
    
    # Create a new plotly figure
    fig = go.Figure()
    
    # Add stock price trace
    fig.add_trace(go.Scatter(
        x=stock_data.index, 
        y=stock_data['Close'],
        mode='lines',
        name='Stock Price',
        line=dict(color='blue')
    ))

    # Add buy signals
    fig.add_trace(go.Scatter(
        x=buy_signals['date'], 
        y=buy_signals['price'],
        mode='markers',
        name='Buy Signal',
        marker=dict(symbol='triangle-up', color='green', size=10)
    ))

    # Add sell signals
    fig.add_trace(go.Scatter(
        x=sell_signals['date'], 
        y=sell_signals['price'],
        mode='markers',
        name='Sell Signal',
        marker=dict(symbol='triangle-down', color='red', size=10)
    ))

    # Update layout for better presentation
    fig.update_layout(
        title=f'Stock Price with Buy and Sell Signals for {ticker}',
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title='Legend',
        hovermode='x'
    )

    # Return the plot
    return fig