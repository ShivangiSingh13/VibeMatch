import kagglehub
import shutil
import os

# Download Spotify Playlists dataset
spotify_path = kagglehub.dataset_download("andrewmvd/spotify-playlists")
# Download TMDB Movie Metadata dataset
tmdb_path = kagglehub.dataset_download("tmdb/tmdb-movie-metadata")

# Find the main CSVs
tmdb_csv = os.path.join(tmdb_path, "tmdb_5000_movies.csv")
spotify_csv = os.path.join(spotify_path, "tracks.csv")

# Copy to your data/ folder
os.makedirs("data", exist_ok=True)
shutil.copy(tmdb_csv, "data/movies.csv")
shutil.copy(spotify_csv, "data/songs.csv")

print("Copied TMDB and Spotify datasets to data/ folder.")
