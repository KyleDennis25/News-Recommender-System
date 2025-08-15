import os
import re
import pandas as pd
import string



def clean_text(text):
    """
    Cleans a string- lowercases string and removes trivial characters and stopwords .
    """
    text = text.lower()
    # Removes standard punctuation and quotes
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Removes curly quotes and other characters
    text = re.sub(r"[“”‘’—–…•]", "", text)
    # Tokenizes text
    tokens = text.split()
    return " ".join(tokens)

def preprocess(df):
    """
    Converts list of NewsAPI articles into a pandas DataFrame.
    """
    # Drops nulls
    df = df.dropna()
    # Combine title and description into text column
    df["text"] = df["title"] + " " + df["description"]
    # Clean text
    df["text"] = df["text"].apply(clean_text)
    # Keep relevant columns
    return df[["title", "topic", "text", "source", "publishedAt", "url"]]

if __name__ == "__main__":
    # preprecesses raw data and saves to data directory
    df_raw = pd.read_csv("data/article_data.csv")
    df_clean = preprocess(df_raw)
    df_clean.to_csv("data/clean_article_data.csv", index=False)
    


