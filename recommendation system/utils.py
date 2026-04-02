"""
Shared utility functions
"""
import re


"""
Utility functions for mood/genre mapping and other helpers.
"""
mood_genre_map = {
    'happy': ['Comedy', 'Family', 'Adventure', 'Animation', 'Music', 'Pop'],
    'sad': ['Drama', 'Romance', 'Tragedy', 'Acoustic'],
    'romantic': ['Romance', 'Drama', 'Music', 'Soft Music'],
    'action': ['Action', 'Thriller', 'Adventure', 'High Energy'],
    'excited': ['Action', 'Adventure', 'Thriller'],
    'chill': ['Music', 'Family', 'Animation'],
    'party': ['Music', 'Comedy'],
    'angry': ['Thriller', 'Crime', 'Action'],
    'scary': ['Horror', 'Thriller'],
    'inspirational': ['Biography', 'Sport', 'History']
}

def map_mood_to_genres(mood):
    """Map a mood to a list of genres."""
    mood = mood.lower()
    return mood_genre_map.get(mood, [])

def get_mood_genre_map():
    """Return the full mood to genre mapping."""
    return mood_genre_map
