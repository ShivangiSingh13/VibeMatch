import pandas as pd
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# --- NLTK Resource Setup ---
def setup_nltk():
    """Ensure required NLTK resources are available for tokenization."""
    resources = ['punkt', 'punkt_tab']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            nltk.download(resource)

setup_nltk()
stemmer = PorterStemmer()

# --- TMDB API Config ---
TMDB_API_KEY = "demo"  # Replace with your actual TMDB API key for real images
TMDB_BASE_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# --- Image & Explanation Helpers ---
def fetch_movie_poster(title):
    """Fetch movie poster from TMDB API. Returns poster URL or a placeholder."""
    try:
        params = {"api_key": TMDB_API_KEY, "query": title}
        response = requests.get(TMDB_BASE_URL, params=params, timeout=5)
        data = response.json()
        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return f"{TMDB_IMAGE_BASE}{poster_path}"
    except Exception:
        pass
    return "https://via.placeholder.com/70x100?text=No+Poster"

def explain_movie_recommendation(movie, user_input, movies_df):
    try:
        if user_input in movies_df['title'].values:
            user_row = movies_df[movies_df['title'] == user_input].iloc[0]
            movie_row = movies_df[movies_df['title'] == movie].iloc[0]
            
            user_tags = set(user_row['tags'].split())
            movie_tags = set(movie_row['tags'].split())
            shared = list(user_tags & movie_tags)
            
            if shared:
                # Filter out very short stems to give more meaningful reasons
                meaningful = [s for s in shared if len(s) > 3][:3]
                return f"Matches your interest in: {', '.join(meaningful)}"
        return "Similar genre or narrative style"
    except Exception:
        return "Recommended based on content similarity"
    # ...migrated to explain.py...
    from explain import explain_recommendation
    return explain_recommendation(user_input, movie, movies_df)

# --- Core Recommendation Logic ---
def preprocess_movies(movies_df):
    """Clean data and combine features into a single 'tags' column."""
    # Drop duplicates and handle missing values in critical columns
    movies_df = movies_df.drop_duplicates(subset='title')
    movies_df = movies_df.dropna(subset=['genres', 'overview', 'keywords', 'cast', 'crew'])
    
    def safe_eval(val):
        try:
            return ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return []

    def create_tags(row):
        # 1. Start with Overview
        tags = str(row['overview']) + ' '
        
        # 2. Add Genres
        genres = safe_eval(row['genres'])
        tags += ' '.join([str(g['name'] if isinstance(g, dict) else g) for g in genres]) + ' '
        
        # 3. Add Keywords
        keywords = safe_eval(row['keywords'])
        tags += ' '.join([str(k['name'] if isinstance(k, dict) else k) for k in keywords]) + ' '
        
        # 4. Add Top 3 Cast members
        cast = safe_eval(row['cast'])
        tags += ' '.join([str(c['name'] if isinstance(c, dict) else c) for c in cast[:3]]) + ' '
        
        # 5. Add Director
        crew = safe_eval(row['crew'])
        for member in crew:
            if isinstance(member, dict) and member.get('job') == 'Director':
                tags += member.get('name', '').replace(" ", "") # Join name to treat as one tag
                break
        return tags

    movies_df['tags'] = movies_df.apply(create_tags, axis=1)

    def clean_text(text):
        """Lowercase, tokenize, and stem words."""
        words = nltk.word_tokenize(text.lower())
        return ' '.join([stemmer.stem(word) for word in words if word.isalnum()])

    movies_df['tags'] = movies_df['tags'].apply(clean_text)
    return movies_df[['movie_id', 'title', 'tags']]
    # ...migrated to preprocessing.py...

def create_similarity_matrix(movies_df):
    """Convert tags to vectors and calculate cosine similarity."""
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies_df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return similarity, cv

def recommend_movies(movie_name, movies_df, similarity):
    """Find the top 5 most similar movies based on the similarity matrix."""
    if movie_name not in movies_df['title'].values:
        return []
    
    # Reset index to ensure the matrix index matches the dataframe index
    movies_df = movies_df.reset_index(drop=True)
    idx = movies_df[movies_df['title'] == movie_name].index[0]
    
    distances = list(enumerate(similarity[idx]))
    # Sort by similarity score (x[1]) in descending order, skip the first one (itself)
    movie_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    
    return [movies_df.iloc[i[0]]['title'] for i in movie_list]
    # ...migrated to content_based.py as recommend_content...