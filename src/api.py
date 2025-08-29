import os
import requests
import pandas as pd
from dotenv import load_dotenv


def get_articles(topics, page_size, pages, language="en"):
    """
    Pulls articles from NewsAPI based on a list of topics.
    Returns a combined list of article dictionaries.
    """
    all_articles = []
    for topic in topics:
        for page in range(1, pages + 1):
            params = {
                "q": topic,
                "pageSize": page_size,
                "page": page,
                "language": language,
                "apiKey": API_KEY,
            }
            url = f"{BASE_URL}/everything"
            # Sends request to NewsAPI for article data
            response = requests.get(url, params=params)
            # Raises error if API request failed
            response.raise_for_status()
            # Converts results into dictionary
            data = response.json()
            # Creates list of articles (dictionaries)
            articles = data.get("articles", [])
            for article in articles:
                article["topic"] = topic
            all_articles.extend(articles)
    return all_articles


def articles_to_df(articles):
    """
    Converts list of NewsAPI articles into a pandas DataFrame.
    Returns DataFrame with relevant columns.
    """
    df = pd.DataFrame(articles)
    if df.empty:
        return df
    columns = ["title", "topic", "description", "source", "publishedAt", "url"]
    df = df[columns].copy()
    # replaces source dictionary with just the name if source is a nested dictionary
    df["source"] = df["source"].apply(lambda x: x["name"] if isinstance(x, dict) else x)
    return df


if __name__ == "__main__":
    # Load API key from .env file
    load_dotenv()
    API_KEY = os.getenv("NEWS_API_KEY")
    BASE_URL = "https://newsapi.org/v2"
    
    # Gets 100 articles for each topic
    topics = ["technology", "science", "business", "politics", "health", "sports", "entertainment", "world", "finance", "economy", "education"]
    articles = get_articles(topics, page_size=50, pages=2)
    df = articles_to_df(articles)
    # Save as a csv in the data directory
    df.to_csv("data/article_data.csv", index=False)