def recommend_articles(df, title, indices, cosine_sim, top_n=5):
    """
    Retrieves top_n most similar articles based on cosine similarity.
    Returns a DataFrame of recommended articles.
    """
    if title not in indices:
        raise ValueError(f"Article '{title}' not found in dataset.")
    
    idx = indices[title]
    # Pair similarity scores with given article
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort by similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # Get top_n most similar articles to the given article, excluding itself
    sim_scores = sim_scores[1:top_n+1]
    # Get article indices
    article_indices = [i[0] for i in sim_scores]
    return df[['title', 'url', 'topic', 'publishedAt']].iloc[article_indices]