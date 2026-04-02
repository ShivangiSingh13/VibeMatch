# VibeMatch AI: Movie & Song Recommendation System

VibeMatch AI is a Streamlit-powered web app that recommends movies and songs based on your mood, preferences, and various recommendation strategies. It supports content-based, collaborative, popularity-based, mood-based, knowledge-based, and cross-domain recommendations, with explanations for each suggestion.

## Features
- **Content-Based Filtering:** Finds similar movies or songs based on content and metadata.
- **Collaborative Filtering:** Suggests items based on user-item interactions (simulated for demo).
- **Popularity-Based:** Shows top-rated or most popular items.
- **Mood-Based:** Recommends items matching your current mood.
- **Knowledge-Based:** Filter movies by genre, year, or rating.
- **Cross-Domain:** Suggests songs for a movie (or vice versa) based on shared features.
- **Explainable AI:** Each recommendation comes with a brief explanation.

## Project Structure
```
app.py                  # Streamlit app entry point
preprocessing.py        # Data cleaning and feature engineering
content_based.py        # Content-based recommendation logic
collaborative.py        # Collaborative filtering logic
popularity.py           # Popularity-based recommendations
mood_based.py           # Mood-based recommendations
knowledge_based.py      # Knowledge-based recommendations
cross_recommend.py      # Cross-domain recommendations
explain.py              # Explanation for recommendations
utils.py                # Shared utilities (mood/genre mapping, etc.)
data/
  movies.csv            # Movie dataset
  songs.csv             # Song dataset
```

## How to Run
1. **Install dependencies:**
   ```bash
   pip install streamlit pandas scikit-learn nltk
   ```
2. **Download NLTK data:**
   ```python
   import nltk
   nltk.download('punkt')
   ```
3. **Launch the app:**
   ```bash
   streamlit run app.py
   ```

## Data Format
- **movies.csv:** Must include columns: `movie_id`, `title`, `genres`, `overview`, `keywords`, `cast`, `crew`
- **songs.csv:** Must include columns: `song_id`, `title`, `artist`, `genre`, `lyrics`

## Customization
- Add more moods or genres in `utils.py` (`mood_genre_map`).
- Extend recommendation logic in respective modules.

## License
This project is for educational/demo purposes.
