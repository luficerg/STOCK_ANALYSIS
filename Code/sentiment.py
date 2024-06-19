import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


def calculate_sentiment_scores(headlines_df):
    """
    This function calculates sentiment scores for each headline in the DataFrame using a sentiment analyzer.

    Args:
    headlines_df (DataFrame): A pandas DataFrame containing headlines.

    Returns:
    DataFrame: The input DataFrame with an additional 'sentiment' column containing the sentiment scores.
    """
    # Apply the sentiment analyzer to each headline and store the compound sentiment score in a new 'sentiment' column
    headlines_df['sentiment'] = headlines_df['headline'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
    
    # Convert the 'date' column to datetime type
    headlines_df['date'] = pd.to_datetime(headlines_df['date'])
    
    # Return the DataFrame with the sentiment scores
    return headlines_df

def aggregate_sentiment_scores(headlines_df):
    """
    This function aggregates sentiment scores by date, calculating the mean sentiment score for each date.

    Args:
    headlines_df (DataFrame): A pandas DataFrame containing headlines and their sentiment scores.

    Returns:
    Series: A pandas Series with dates as the index and the mean sentiment score for each date as the values.
    """
    # Group the DataFrame by 'date' and calculate the mean sentiment score for each group
    sentiment_summary = headlines_df.groupby('date')['sentiment'].mean()
    
    # Return the aggregated sentiment scores
    return sentiment_summary

def generate_trading_signals(sentiment_summary):
    """
    This function generates trading signals based on the sentiment scores.

    Args:
    sentiment_summary (Series): A pandas Series containing aggregated sentiment scores by date.

    Returns:
    Series: A pandas Series with trading signals (1 for positive sentiment, -1 for negative sentiment, and 0 for neutral sentiment).
    """
    # Apply a function to generate trading signals: 1 for sentiment > 0.2, -1 for sentiment < -0.2, and 0 for sentiment between -0.2 and 0.2
    signals = sentiment_summary.apply(lambda x: 1 if x > 0.2 else (-1 if x < -0.2 else 0))
    
    # Return the generated trading signals
    return signals
