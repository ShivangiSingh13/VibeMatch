"""
Cross-domain recommendation module.
"""
from utils import get_mood_genre_map

def cross_recommend(input_name, input_type, movies_df, songs_df):
    if input_type == 'movie':
        movie_row = movies_df[movies_df['title'] == input_name]
        if movie_row.empty:
            return []
        tags = movie_row.iloc[0]['tags']
        genres = tags.split()
        mood_genres = set()
        for mood, genre_list in get_mood_genre_map().items():
            if any(g in genres for g in genre_list):
                mood_genres.update(genre_list)
        filtered = songs_df[songs_df['genre'].isin(mood_genres)]
        if filtered.empty:
            filtered = songs_df[songs_df['tags'].apply(lambda t: any(g in t for g in genres))]
        return filtered['title'].head(5).tolist()
    elif input_type == 'song':
        song_row = songs_df[songs_df['title'] == input_name]
        if song_row.empty:
            return []
        tags = song_row.iloc[0]['tags']
        genres = tags.split()
        mood_genres = set()
        for mood, genre_list in get_mood_genre_map().items():
            if any(g in genres for g in genre_list):
                mood_genres.update(genre_list)
        filtered = movies_df[movies_df['tags'].apply(lambda t: any(g in t for g in mood_genres))]
        if filtered.empty:
            filtered = movies_df[movies_df['tags'].apply(lambda t: any(g in t for g in genres))]
        return filtered['title'].head(5).tolist()
    else:
        return []
