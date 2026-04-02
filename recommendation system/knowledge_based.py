"""
Knowledge-based recommendation module.
"""
def recommend_by_filters(df, genre=None, year=None, rating=None):
    filtered = df
    if genre:
        filtered = filtered[filtered['tags'].str.contains(genre.lower())]
    if year and 'year' in filtered.columns:
        filtered = filtered[filtered['year'] == year]
    if rating and 'rating' in filtered.columns:
        filtered = filtered[filtered['rating'] >= rating]
    return filtered['title'].head(5).tolist()
