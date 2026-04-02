"""
Mood-based recommendation module.
"""
from utils import map_mood_to_genres

def recommend_by_mood(mood, df):
    genres = map_mood_to_genres(mood)
    if not genres:
        return []
    filtered = df[df['tags'].apply(lambda t: any(g.lower() in t for g in genres))]
    return filtered['title'].head(5).tolist()
