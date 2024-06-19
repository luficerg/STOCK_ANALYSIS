import asyncio
import nest_asyncio
from fetch_data import fetch_news, fetch_stock_data
from calculations import calculate_max_drawdown, calculate_portfolio_metrics, calculate_sharpe_ratio, plot_signals
from sentiment import aggregate_sentiment_scores, generate_trading_signals, calculate_sentiment_scores
from simulate_trade import simulate_trades
import streamlit as st

async def final(ticker, rate, initial, df):
    """
    This function orchestrates the entire trading strategy pipeline from fetching data to plotting results.

    Args:
    ticker (str): The stock ticker symbol.
    rate (float): The risk-free rate for Sharpe ratio calculation.
    initial (float): The initial capital for trading.
    df (DataFrame): A pandas DataFrame containing news data.

    Returns:
    None: Displays trade metrics and plots trading signals.
    """
    # Fetch stock data
    print("Fetching stock data...")
    stock_data = fetch_stock_data(ticker)

    # Calculate sentiment scores
    print("Calculating sentiment scores...")
    news_data_with_scores = calculate_sentiment_scores(df)

    
    # Aggregate sentiment scores by 
    print("Aggregate sentiment scores...")
    sentiment_summary = aggregate_sentiment_scores(news_data_with_scores)
    
    # Generate trading signals
    print("Generate trading signals...")
    trading_signals = generate_trading_signals(sentiment_summary)
    
    # Simulate trades
    print("\nSimulating trades...")
    portfolio = simulate_trades(stock_data, trading_signals, initial)
    
    # Calculate portfolio metrics
    total_trades, win_percentage, total_profit, loss_percentage , total_loss = calculate_portfolio_metrics(portfolio)
    
    # Display portfolio and key metrics
    st.write(portfolio)
    st.write(f"Initial capital: ${initial}")
    st.write(f"Total Trades: {total_trades}")
    st.write(f"Win Percentage: {win_percentage:.2f}%")
    st.write(f"Total Profit: ${total_profit:.2f}")
    st.write(f"Sharpe Ratio: {calculate_sharpe_ratio(portfolio, rate):.2f} with risk-free rate of {rate}")
    st.write(f"Max Drawdown: {calculate_max_drawdown(portfolio)}")
    
    # Plot buy and sell signals
    print("Plotting charts..")
    fig = plot_signals(stock_data, portfolio, ticker)
    st.plotly_chart(fig)


async def main(ticker):
    nest_asyncio.apply()

    print("Started to fetch news")
    news = await fetch_news(ticker)
    await final(ticker, 0.01, 100, news)


# Streamlit app code
st.title("Stock Sentiment Analysis")

# Input for stock symbol
ticker = st.text_input("Enter stock symbol:", "NVDA")


# Run analysis when button is clicked
if st.button("Run Analysis"):
    asyncio.run(main(ticker))
