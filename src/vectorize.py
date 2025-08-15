import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv("data/clean_article_data.csv")

# Initialize vectorizer
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')

# Fit and transform the 'text' column
tfidf_matrix = vectorizer.fit_transform(df['text'])


# Compute similarity between all articles
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


