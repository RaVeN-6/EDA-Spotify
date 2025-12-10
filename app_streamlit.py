import sys
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[0]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data.spotify_api import get_spotify_client, fetch_playlist_tracks_with_features


@st.cache_resource
def get_client():
    return get_spotify_client()


st.set_page_config(page_title="Spotify Playlist Analyzer", layout="wide")
st.title("Spotify Playlist Analyzer (rock project demo)")

sp = get_client()

st.sidebar.header("Entrada")
playlist_url = st.sidebar.text_input(
    "Pega la URL de una playlist de Spotify",
    placeholder="https://open.spotify.com/playlist/...",
)

search_query = st.sidebar.text_input(
    "Buscar canción dentro de la playlist (opcional)",
    placeholder="Parte del título",
)

if playlist_url:
    playlist_id = playlist_url.split("/")[-1].split("?")[0]

    with st.spinner("Descargando playlist desde Spotify..."):
        df_pl = fetch_playlist_tracks_with_features(sp, playlist_id)

    if df_pl.empty:
        st.error("No se encontraron canciones en esta playlist.")
    else:
        st.subheader("Resumen de la playlist")
        st.write(f"Número de canciones: {len(df_pl)}")
        st.dataframe(df_pl.head(20))

        # Ranking por popularidad
        df_ranked = df_pl.sort_values("popularity", ascending=False).reset_index(drop=True)

        st.subheader("Top canciones por popularidad en la playlist")
        top_n = st.slider("Número de canciones a mostrar", 5, 30, 15)

        top_tracks = df_ranked.head(top_n)
        st.bar_chart(
            data=top_tracks.set_index("track_name")["popularity"]
        )

        # Búsqueda de una canción concreta
        if search_query:
            mask = df_ranked["track_name"].str.contains(search_query, case=False, na=False)
            results = df_ranked[mask]
            st.subheader(f"Resultados para: {search_query}")
            if results.empty:
                st.info("No se encontraron coincidencias en esta playlist.")
            else:
                st.dataframe(results)

        # Si hay audio features, se pueden mostrar histogramas
        feature_cols = {"Danceability", "Energy", "Valence", "Tempo", "duration_ms"}
        if feature_cols.issubset(set(df_pl.columns)):
            st.subheader("Distribución de características de audio")
            features = ["Danceability", "Energy", "Valence", "Tempo"]
            for col in features:
                st.line_chart(df_pl[col].sort_values().reset_index(drop=True))
