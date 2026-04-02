"""
Preprocessing module for movies and songs datasets.
Handles cleaning, tag creation, and text normalization.
"""
import ast
import nltk
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def safe_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return []

def clean_text(text):
    """Lowercase, tokenize, and stem words."""
    words = nltk.word_tokenize(str(text).lower())
    return ' '.join([stemmer.stem(word) for word in words if word.isalnum()])

def preprocess_movies(movies_df):
    """Clean data and combine features into a single 'tags' column."""
    movies_df = movies_df.drop_duplicates(subset='title')
    movies_df = movies_df.dropna(subset=['genres', 'overview', 'keywords', 'cast', 'crew'])
    def create_tags(row):
        tags = str(row['overview']) + ' '
        genres = safe_eval(row['genres'])
        tags += ' '.join([str(g['name'] if isinstance(g, dict) else g) for g in genres]) + ' '
        keywords = safe_eval(row['keywords'])
        tags += ' '.join([str(k['name'] if isinstance(k, dict) else k) for k in keywords]) + ' '
        cast = safe_eval(row['cast'])
        tags += ' '.join([str(c['name'] if isinstance(c, dict) else c) for c in cast[:3]]) + ' '
        crew = safe_eval(row['crew'])
        for member in crew:
            if isinstance(member, dict) and member.get('job') == 'Director':
                tags += member.get('name', '').replace(" ", "")
                break
        return tags
    movies_df['tags'] = movies_df.apply(create_tags, axis=1)
    movies_df['tags'] = movies_df['tags'].apply(clean_text)
    return movies_df[['movie_id', 'title', 'tags']]

def preprocess_songs(songs_df):
    songs_df = songs_df.drop_duplicates(subset='title')
    songs_df = songs_df.dropna(subset=['title', 'artist', 'genre'])
    def create_tags(row):
        tags = f"{row['title']} {row['artist']} {row['genre']} {row.get('lyrics', '')}"
        return tags
    songs_df['tags'] = songs_df.apply(create_tags, axis=1)
    songs_df['tags'] = songs_df['tags'].apply(clean_text)
    return songs_df[['song_id', 'title', 'artist', 'genre', 'tags']]
