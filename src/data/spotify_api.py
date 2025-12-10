import os

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_spotify_client() -> spotipy.Spotify:
    auth_manager = SpotifyOAuth(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback"),
        scope="playlist-read-private playlist-read-collaborative user-library-read",
        cache_path=".cache-spotify",
        open_browser=False,
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def fetch_playlist_tracks_with_features(sp: spotipy.Spotify, playlist_id: str) -> pd.DataFrame:
    """
    Descarga todas las canciones de una playlist y sus audio features.
    Devuelve un DataFrame listo para EDA.
    """
    # 1) Obtener todas las pistas de la playlist (paginando)
    tracks = []
    results = sp.playlist_items(playlist_id, additional_types=("track",))
    while results:
        for item in results["items"]:
            track = item["track"]
            if track is None:
                continue
            tracks.append(track)
        if results["next"]:
            results = sp.next(results)
        else:
            break

    if not tracks:
        return pd.DataFrame()

    # 2) Extraer IDs y metadatos básicos
    rows = []
    for t in tracks:
        rows.append(
            {
                "track_id": t["id"],
                "track_name": t["name"],
                "artist_name": ", ".join([a["name"] for a in t["artists"]]),
                "album_name": t["album"]["name"],
                "popularity": t["popularity"],
            }
        )

    df_meta = pd.DataFrame(rows)

        # 3) Audio features por lote (API permite hasta 100 IDs a la vez)
    features_list = []
    ids = df_meta["track_id"].dropna().tolist()

    # Filtrar posibles IDs vacíos o raros
    ids = [tid for tid in ids if isinstance(tid, str) and tid.strip()]

    for i in range(0, len(ids), 100):
        batch = ids[i : i + 100]
        try:
            audio_features = sp.audio_features(batch)
        except spotipy.SpotifyException as e:
            print("Error en batch, se omite:", e)
            continue

        # audio_features puede contener None para algunos IDs
        audio_features = [af for af in audio_features if af is not None]
        features_list.extend(audio_features)

    if not features_list:
        return df_meta  # al menos devuelves metadatos básicos


    # 4) Unir metadatos + audio features
    df = df_meta.merge(df_feat, left_on="track_id", right_on="id", how="left")

    # 5) Seleccionar columnas clave y renombrar parecido a tu dataset
    df = df[
        [
            "track_id",
            "track_name",
            "artist_name",
            "album_name",
            "popularity",
            "danceability",
            "energy",
            "valence",
            "tempo",
            "duration_ms",
        ]
    ].rename(
        columns={
            "track_name": "Track",
            "artist_name": "Artist",
            "album_name": "Album",
            "danceability": "Danceability",
            "energy": "Energy",
            "valence": "Valence",
            "tempo": "Tempo",
        }
    )

    return df
