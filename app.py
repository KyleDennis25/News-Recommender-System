import pandas as pd 
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.recommend import recommend_articles

# Load data
df = pd.read_csv("data/clean_article_data.csv")

# Initialize vectorizer
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')

# Fit and transform the 'text' column
tfidf_matrix = vectorizer.fit_transform(df['text'])

# Compute similarity between all articles
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Map each article to its index
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

# Set title
st.set_page_config(page_title="Article Recommendation System", layout="wide")
st.title("Article Recommendation System")

# Create sidebar for controls
st.sidebar.header("Settings")
top_n = st.sidebar.slider("Number of recommendations:", min_value=1, max_value=10, value=5)

# List articles to select from
article_titles = df['title'].tolist()
title_input = st.selectbox("Select an article:", article_titles)

# Display current article URL
if title_input:
    current_article_url = df.loc[df['title'] == title_input, 'url'].values[0]
    st.markdown(f"**Selected article:** [{title_input}]({current_article_url})")

# Create button to get recommendations
if st.button("Get Recommendations"):
    if title_input:
        try:
            recommendations = recommend_articles(df, title_input, indices, cosine_sim, top_n=top_n)
            if not recommendations.empty:
                st.subheader("Recommended Articles:")
                for _, row in recommendations.iterrows():
                    st.markdown(f"- [{row['title']}]({row['url']})")
            else:
                st.warning("No recommendations found.")
        except ValueError as e:
            st.error(str(e))
    else:
        st.warning("Please select an article.")


