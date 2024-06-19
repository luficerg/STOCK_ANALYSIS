from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import nest_asyncio
import asyncio
import aiohttp

def fetch_stock_data(ticker):
    """
    This function fetches historical stock price data for a given ticker symbol.

    Args:
    ticker (str): The stock ticker symbol.

    Returns:
    DataFrame: A pandas DataFrame containing the closing prices of the stock.
    """
    print("Fetching stock prices...")

    # Download the stock data for the given ticker for the maximum available period
    stock_data = yf.download(ticker, period="max")

    # Keep only the 'Close' column which contains the closing prices
    stock_data = stock_data[['Close']]

    # Return the DataFrame containing the closing prices
    return stock_data

# Apply nest_asyncio
nest_asyncio.apply()
    
async def fetch_page(session, url, retries=3, delay=2):
    """
    Asynchronously fetch a single page with retry logic.
    
    Args:
    session (aiohttp.ClientSession): The HTTP session to use for the request.
    url (str): The URL of the page to fetch.
    retries (int): Number of retries for the request.
    delay (int): Delay between retries in seconds.

    Returns:
    str: The HTML content of the page.
    """
    for attempt in range(retries):
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response.raise_for_status()
                return await response.text()
        except (aiohttp.ClientError, aiohttp.ClientResponseError, aiohttp.ServerTimeoutError, asyncio.TimeoutError) as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                await asyncio.sleep(delay)
            else:
                raise

async def fetch_news(ticker):
    """
    Asynchronously fetch news headlines for a given ticker symbol from the Business Insider website.

    Args:
    ticker (str): The stock ticker symbol.

    Returns:
    DataFrame: A pandas DataFrame containing the datetime, ticker, source, and headline of the news articles.
    """
    # Define the columns for the DataFrame
    columns = ['datetime', 'ticker', 'source', 'headline']
    df = pd.DataFrame(columns=columns)
    ticker = str(ticker).lower()
    urls = [f'https://markets.businessinsider.com/news/{ticker}-stock?p={page}' for page in range(1, 200)]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url) for url in urls]
        pages = await asyncio.gather(*tasks)

    counter = 0

    for html in pages:
        soup = BeautifulSoup(html, 'lxml')
        articles = soup.find_all('div', class_='latest-news__story')
        for article in articles:
            datetime = article.find('time', class_='latest-news__date').get('datetime')
            title = article.find('a', class_='news-link').text
            source = article.find('span', class_='latest-news__source').text
            df = pd.concat([pd.DataFrame([[datetime, ticker, source, title]], columns=df.columns), df], ignore_index=True)
            counter += 1

    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = df['datetime'].dt.date
    df['time'] = df['datetime'].dt.time
    df.drop(columns=['datetime'], inplace=True)

    print(f'{counter} headlines scraped from 200 pages')
    return df