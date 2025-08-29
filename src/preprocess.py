import re
import pandas as pd
import string


def clean_text(text):
    """
    Cleans a text string (lowercases text, removes trivial characters, and tokenizes text).
    Returns cleaned string.
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
    Preprocesses article DataFrame (combines title and text columns, and cleans text).
    Returns cleaned DataFrame with relevant columns.
    """
    df = df.dropna().copy()
    # Combine title and description into text column
    df["text"] = df["title"] + " " + df["description"]
    # Clean text
    df["text"] = df["text"].apply(clean_text)
    return df[["title", "topic", "text", "source", "publishedAt", "url"]]


if __name__ == "__main__":
    # Preprocesses raw data and saves to data directory
    df_raw = pd.read_csv("data/article_data.csv")
    df_clean = preprocess(df_raw)
    df_clean.to_csv("data/clean_article_data.csv", index=False)