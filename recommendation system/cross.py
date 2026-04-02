"""
Cross Recommendation Logic for VibeMatch AI
"""
import pandas as pd
from utils import map_mood_to_genres, get_mood_genre_map

def cross_recommend(input_name, input_type, movies_df, songs_df):
    """
    input_type: 'movie' or 'song'
    Returns: list of recommended items from the other domain
    """
    if input_type == 'movie':
        # Find movie row
        movie_row = movies_df[movies_df['title'] == input_name]
        if movie_row.empty:
            return []
        # Extract genres/tags
        tags = movie_row.iloc[0]['tags']
        # Try to infer mood from genres
        genres = tags.split()
        mood_genres = set()
        for mood, genre_list in get_mood_genre_map().items():
            if any(g in genres for g in genre_list):
                mood_genres.update(genre_list)
        # Recommend songs with matching genres
        filtered = songs_df[songs_df['genre'].isin(mood_genres)]
        if filtered.empty:
            # fallback: match by tags
            filtered = songs_df[songs_df['tags'].apply(lambda t: any(g in t for g in genres))]
        return filtered['title'].head(5).tolist()
    elif input_type == 'song':
        # Find song row
        song_row = songs_df[songs_df['title'] == input_name]
        if song_row.empty:
            return []
        # Extract genre/tags
        tags = song_row.iloc[0]['tags']
        genres = tags.split()
        mood_genres = set()
        for mood, genre_list in get_mood_genre_map().items():
            if any(g in genres for g in genre_list):
                mood_genres.update(genre_list)
        # Recommend movies with matching genres
        filtered = movies_df[movies_df['tags'].apply(lambda t: any(g in t for g in mood_genres))]
        if filtered.empty:
            filtered = movies_df[movies_df['tags'].apply(lambda t: any(g in t for g in genres))]
        return filtered['title'].head(5).tolist()
    else:
        return []
