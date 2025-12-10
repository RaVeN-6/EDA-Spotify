# tests/test_auth.py
from dotenv import load_dotenv
load_dotenv()

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]  # sube de tests/ a la raíz
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data.spotify_api import get_spotify_client
import spotipy

sp: spotipy.Spotify = get_spotify_client()

print("Usuario:", sp.me()["display_name"])

playlist_id = "02FpEk5yRs7XcnXna2RIuJ"
results = sp.playlist_items(playlist_id, additional_types=("track",))
print("Items en primera página:", len(results["items"]))
print("Next:", results["next"])
