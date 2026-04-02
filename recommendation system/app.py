import streamlit as st
import pandas as pd
from preprocessing import preprocess_movies, preprocess_songs
from content_based import create_similarity_matrix, recommend_content
from collaborative import recommend_collaborative
from popularity import recommend_popular
from mood_based import recommend_by_mood
from knowledge_based import recommend_by_filters
from cross_recommend import cross_recommend
from explain import explain_recommendation
from utils import get_mood_genre_map

# --- UI Configuration ---
st.set_page_config(page_title="VibeMatch AI", layout="wide")

st.markdown("""
    <style>
    body, .stApp { background-color: #18191A; color: #E4E6EB; }
    .stButton>button { background: #242526; color: #E4E6EB; border-radius: 8px; border: none; width: 100%; }
    .stButton>button:hover { background: #3A3B3C; color: #FFD700; border: 1px solid #FFD700; }
    .card { background: #242526; border-radius: 12px; padding: 1em; margin: 0.5em 0; border: 1px solid #3A3B3C; }
    .section-title { font-size: 1.5em; font-weight: bold; margin: 1em 0; color: #FFD700; }
    </style>
""", unsafe_allow_html=True)

# --- Robust Data Loading ---
def initialize_system():
    m_raw = pd.read_csv('data/movies.csv')
    s_raw = pd.read_csv('data/songs.csv')
    # Preprocess
    m_df = preprocess_movies(m_raw)
    s_df = preprocess_songs(s_raw)

    # --- Similarity Matrices ---
    movie_similarity, _ = create_similarity_matrix(m_df)
    song_similarity, _ = create_similarity_matrix(s_df)

    mood_to_genres = get_mood_genre_map()

    return m_df, s_df, movie_similarity, song_similarity, mood_to_genres



# --- UI Helper Functions (must be top-level for Streamlit cache) ---
def fetch_movie_poster(title):
    return "https://via.placeholder.com/70x100?text=No+Poster"

def fetch_song_cover(title):
    return "https://via.placeholder.com/70x100?text=No+Cover"

def display_card(title, img, explanation):
    st.image(img, width=70)
    st.markdown(f"**{title}**")
    st.caption(explanation)

def render_recommendations(title, icon, items, fetch_fn, explain_fn, input_val, df):
    st.markdown(f'<div class="section-title">{icon} {title}</div>', unsafe_allow_html=True)
    if not items:
        st.write("No matches found. Try a different vibe!")
        return
    cols = st.columns(2)
    for i, item in enumerate(items):
        with cols[i % 2]:
            img = fetch_fn(item)
            exp = explain_fn(input_val, item, df)
            display_card(item, img, exp)

# --- Initialize system and unpack variables ---
movies_df, songs_df, movie_similarity, song_similarity, mood_to_genres = initialize_system()

# --- Sidebar & Main Logic ---
mode = st.sidebar.selectbox("Choose Recommendation Type:", [
    "Content-Based", "Collaborative", "Mood-Based", "Popular", "Knowledge-Based", "Compare"])

if mode == "Content-Based":
    rec_type = st.sidebar.selectbox("Recommend for:", ["Movie", "Song"])
    if rec_type == "Movie":
        user_input = st.sidebar.selectbox("Search Movie:", movies_df['title'].unique())
    else:
        user_input = st.sidebar.selectbox("Search Song:", songs_df['title'].unique())
elif mode == "Collaborative":
    user_id = st.sidebar.text_input("Enter User ID:")
    rec_type = st.sidebar.selectbox("Recommend for:", ["Movie", "Song"])
elif mode == "Mood-Based":
    mood = st.sidebar.selectbox("Select Mood:", list(mood_to_genres.keys()))
elif mode == "Popular":
    rec_type = st.sidebar.selectbox("Recommend for:", ["Movie", "Song"])
elif mode == "Knowledge-Based":
    genre = st.sidebar.text_input("Genre (optional):")
    year = st.sidebar.text_input("Year (optional):")
    rating = st.sidebar.text_input("Min Rating (optional):")
elif mode == "Compare":
    rec_type = st.sidebar.selectbox("Compare for:", ["Movie", "Song"])
    if rec_type == "Movie":
        user_input = st.sidebar.selectbox("Search Movie:", movies_df['title'].unique())
    else:
        user_input = st.sidebar.selectbox("Search Song:", songs_df['title'].unique())

# --- Execution ---
if mode == "Content-Based" and 'user_input' in locals():
    with st.spinner('Finding content-based recommendations...'):
        if rec_type == "Movie":
            recs = recommend_content(user_input, movies_df, movie_similarity, 'movie')
            cross = cross_recommend(user_input, 'movie', movies_df, songs_df)
            render_recommendations("Similar Movies", "🎬", recs, fetch_movie_poster, explain_recommendation, user_input, movies_df)
            render_recommendations("Matching Songs", "🎵", cross, fetch_song_cover, explain_recommendation, user_input, songs_df)
        else:
            recs = recommend_content(user_input, songs_df, song_similarity, 'song')
            cross = cross_recommend(user_input, 'song', movies_df, songs_df)
            render_recommendations("Similar Songs", "🎵", recs, fetch_song_cover, explain_recommendation, user_input, songs_df)
            render_recommendations("Matching Movies", "🎬", cross, fetch_movie_poster, explain_recommendation, user_input, movies_df)

elif mode == "Collaborative" and 'user_id' in locals():
    with st.spinner('Finding collaborative recommendations...'):
        import numpy as np
        import pandas as pd
        if rec_type == "Movie":
            user_item_matrix = pd.DataFrame(np.random.randint(0, 2, (10, len(movies_df))),
                                            index=[f'user{i}' for i in range(10)],
                                            columns=movies_df['title'])
            recs = recommend_collaborative(user_id, user_item_matrix, movies_df['title'].tolist(), 'movie')
            render_recommendations("Collaborative Movies", "👥", recs, fetch_movie_poster, explain_recommendation, user_id, movies_df)
        else:
            user_item_matrix = pd.DataFrame(np.random.randint(0, 2, (10, len(songs_df))),
                                            index=[f'user{i}' for i in range(10)],
                                            columns=songs_df['title'])
            recs = recommend_collaborative(user_id, user_item_matrix, songs_df['title'].tolist(), 'song')
            render_recommendations("Collaborative Songs", "👥", recs, fetch_song_cover, explain_recommendation, user_id, songs_df)

elif mode == "Mood-Based" and 'mood' in locals():
    with st.spinner('Finding mood-based recommendations...'):
        m_recs = recommend_by_mood(mood, movies_df)
        s_recs = recommend_by_mood(mood, songs_df)
        render_recommendations(f"{mood.title()} Movies", "🎬", m_recs, fetch_movie_poster, lambda x,y,z: "Matches your mood", mood, movies_df)
        render_recommendations(f"{mood.title()} Songs", "🎵", s_recs, fetch_song_cover, lambda x,y,z: "Matches your mood", mood, songs_df)

elif mode == "Popular":
    with st.spinner('Finding popular recommendations...'):
        if rec_type == "Movie":
            recs = recommend_popular(movies_df, 'movie')
            render_recommendations("Popular Movies", "🔥", recs, fetch_movie_poster, explain_recommendation, '', movies_df)
        else:
            recs = recommend_popular(songs_df, 'song')
            render_recommendations("Popular Songs", "🔥", recs, fetch_song_cover, explain_recommendation, '', songs_df)

elif mode == "Knowledge-Based":
    with st.spinner('Finding knowledge-based recommendations...'):
        recs = recommend_by_filters(movies_df, genre=genre, year=year if year else None, rating=float(rating) if rating else None)
        render_recommendations("Filtered Movies", "🔎", recs, fetch_movie_poster, explain_recommendation, '', movies_df)

elif mode == "Compare" and 'user_input' in locals():
    with st.spinner('Comparing recommendation techniques...'):
        if rec_type == "Movie":
            content_recs = recommend_content(user_input, movies_df, movie_similarity, 'movie')
            pop_recs = recommend_popular(movies_df, 'movie')
            m_recs = recommend_by_mood('happy', movies_df)
            import numpy as np
            import pandas as pd
            user_item_matrix = pd.DataFrame(np.random.randint(0, 2, (10, len(movies_df))),
                                            index=[f'user{i}' for i in range(10)],
                                            columns=movies_df['title'])
            collab_recs = recommend_collaborative('user0', user_item_matrix, movies_df['title'].tolist(), 'movie')
            st.markdown("### Content-Based vs Collaborative vs Popularity vs Mood-Based")
            cols = st.columns(4)
            for i, (title, recs) in enumerate(zip([
                "Content-Based", "Collaborative", "Popularity", "Mood-Based"],
                [content_recs, collab_recs, pop_recs, m_recs])):
                with cols[i]:
                    st.markdown(f"**{title}**")
                    for item in recs:
                        st.markdown(f"- {item}")
        else:
            content_recs = recommend_content(user_input, songs_df, song_similarity, 'song')
            pop_recs = recommend_popular(songs_df, 'song')
            m_recs = recommend_by_mood('happy', songs_df)
            import numpy as np
            import pandas as pd
            user_item_matrix = pd.DataFrame(np.random.randint(0, 2, (10, len(songs_df))),
                                            index=[f'user{i}' for i in range(10)],
                                            columns=songs_df['title'])
            collab_recs = recommend_collaborative('user0', user_item_matrix, songs_df['title'].tolist(), 'song')
            st.markdown("### Content-Based vs Collaborative vs Popularity vs Mood-Based")
            cols = st.columns(4)
            for i, (title, recs) in enumerate(zip([
                "Content-Based", "Collaborative", "Popularity", "Mood-Based"],
                [content_recs, collab_recs, pop_recs, m_recs])):
                with cols[i]:
                    st.markdown(f"**{title}**")
                    for item in recs:
                        st.markdown(f"- {item}")