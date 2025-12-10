from pathlib import Path

# Ruta base del proyecto (carpeta spotify_rock_eda)
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# CSV principal de Spotify
SPOTIFY_RAW_CSV = RAW_DATA_DIR / "spotify.csv"
