import streamlit as st
from src.vectorize import df
from src.recommend import recommend_articles

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
            recommendations = recommend_articles(title_input, top_n=top_n)
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


