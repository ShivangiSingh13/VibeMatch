"""
Popularity-based recommendation module.
"""
def recommend_popular(df, type_):
    """Return top 5 most popular items (by rating or frequency)."""
    if 'rating' in df.columns:
        return df.sort_values('rating', ascending=False)['title'].head(5).tolist()
    else:
        return df['title'].value_counts().head(5).index.tolist()
