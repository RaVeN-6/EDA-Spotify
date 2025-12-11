import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# --------------------------------------------------
# CLIENTE DE SPOTIFY
# --------------------------------------------------
def get_spotify_client() -> spotipy.Spotify:
    """
    Autenticación de Spotify con OAuth.
    """
    auth_manager = SpotifyOAuth(
        client_id=os.environ.get("SPOTIFY_CLIENT_ID"),
        client_secret=os.environ.get("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback"),
        scope=(
            "playlist-read-private playlist-read-collaborative user-library-read"
        ),
        cache_path=".cache-spotify",
        open_browser=False,
    )
    return spotipy.Spotify(auth_manager=auth_manager)


# --------------------------------------------------
# FUNCIÓN PRINCIPAL DE ANÁLISIS
# --------------------------------------------------
def fetch_playlist_tracks_with_features(sp: spotipy.Spotify, playlist_id: str) -> pd.DataFrame:
    """
    Obtiene TODA la información del playlist:
    - Metadata del track
    - Fecha de lanzamiento
    - Album + detalles
    - Audio features completos
    - Datos útiles para análisis
    """

    # -----------------------------------------
    # Obtener items del playlist (con paginación)
    # -----------------------------------------
    tracks = []
    results = sp.playlist_items(playlist_id, additional_types=("track",))

    while results:
        items = results.get("items", [])
        for item in items:
            track = item.get("track")
            if track:
                tracks.append(track)

        if results.get("next"):
            results = sp.next(results)
        else:
            break

    if not tracks:
        return pd.DataFrame()

    # -----------------------------------------
    # EXTRAER METADATOS
    # -----------------------------------------
    meta_rows = []

    for t in tracks:
        album = t.get("album", {})
        release_date = album.get("release_date")

        meta_rows.append({
            "track_id": t.get("id"),
            "Track": t.get("name"),
            "Artist": ", ".join(a.get("name") for a in t.get("artists", [])),
            "Album": album.get("name"),
            "Album_ID": album.get("id"),
            "Album_Total_Tracks": album.get("total_tracks"),
            "Release_Date": release_date,
            "Popularity": t.get("popularity"),
            "Duration_ms": t.get("duration_ms"),
            "Track_Number": t.get("track_number"),
            "Disc_Number": t.get("disc_number"),
            "Preview_URL": t.get("preview_url"),
        })

    df_meta = pd.DataFrame(meta_rows)

    # -----------------------------------------
    # AUDIO FEATURES
    # -----------------------------------------
    ids = [tid for tid in df_meta["track_id"].dropna().tolist() if isinstance(tid, str)]
    features_list = []

    for i in range(0, len(ids), 100):
        batch = ids[i:i + 100]

        try:
            audio_features = sp.audio_features(batch)
        except spotipy.SpotifyException:
            continue

        if audio_features:
            cleaned = [f for f in audio_features if f]
            features_list.extend(cleaned)

    if not features_list:
        return df_meta

    df_feat = pd.DataFrame(features_list)

    # -----------------------------------------
    # MERGE METADATA + FEATURES
    # -----------------------------------------
    df = df_meta.merge(df_feat, left_on="track_id", right_on="id", how="left")

    # -----------------------------------------
    # COLUMNAS FINALES ÚTILES (las acordadas)
    # -----------------------------------------
    final_cols = [
        "track_id", "Track", "Artist", "Album", "Album_ID", "Album_Total_Tracks",
        "Release_Date", "Popularity", "Duration_ms", "Track_Number", "Disc_Number",
        "Preview_URL", "danceability", "energy", "valence", "tempo", "acousticness",
        "instrumentalness", "liveness", "speechiness"
    ]

    df = df[[c for c in final_cols if c in df.columns]]

    return df
