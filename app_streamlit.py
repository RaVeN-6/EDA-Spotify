import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()  # carga SPOTIFY_CLIENT_ID, etc. desde .env

BASE_DIR = Path(__file__).resolve().parents[0]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data.spotify_api import get_spotify_client, fetch_playlist_tracks_with_features


@st.cache_resource
def get_client():
    return get_spotify_client()


st.set_page_config(page_title="Spotify Playlist Analyzer", layout="wide")
st.title("Analizador de Playlist En Spotify")

# --- Cliente de Spotify ---
st.sidebar.header("Autenticación / estado")
try:
    sp = get_client()
    st.sidebar.success("Cliente de Spotify inicializado.")
except Exception as e:
    st.sidebar.error(f"Error creando cliente de Spotify: {e}")
    st.stop()

# --- Inputs ---
st.sidebar.header("Entrada")
playlist_url = st.sidebar.text_input(
    "Pega la URL de una playlist de Spotify",
    placeholder="https://open.spotify.com/playlist/...",
)

search_query = st.sidebar.text_input(
    "Buscar canción dentro de la playlist (opcional)",
    placeholder="Parte del título",
)

buscar_btn = st.sidebar.button("Analizar playlist")  # botón para disparar la búsqueda

# --- Lógica principal ---
if playlist_url and buscar_btn:
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    st.write(f"Playlist ID detectado: `{playlist_id}`")

    with st.spinner("Descargando playlist desde Spotify..."):
        try:
            df_pl = fetch_playlist_tracks_with_features(sp, playlist_id)
        except Exception as e:
            st.error(f"Error al descargar playlist: {e}")
            st.stop()

    if df_pl is None:
        st.error("La función devolvió None. Revisa fetch_playlist_tracks_with_features.")
        st.stop()

    if df_pl.empty:
        st.error("No se encontraron canciones en esta playlist.")
        st.stop()

    # --- Resumen de la playlist ---
    st.subheader("Resumen de la playlist")
    st.write(f"Número de canciones: {len(df_pl)}")
    st.dataframe(df_pl.head(20))

    # --- Ranking por popularidad ---
    if "popularity" not in df_pl.columns:
        st.warning("La columna 'popularity' no está disponible en el DataFrame.")
    else:
        df_ranked = df_pl.sort_values("popularity", ascending=False).reset_index(drop=True)

        st.subheader("Top canciones por popularidad en la playlist")
        top_n = st.slider("Número de canciones a mostrar", 5, 30, 15)

        top_tracks = df_ranked.head(top_n)
        st.bar_chart(
            data=top_tracks.set_index("track_name")["popularity"]
        )

        # --- Búsqueda dentro de la playlist ---
        if search_query:
            mask = df_ranked["track_name"].str.contains(search_query, case=False, na=False)
            results = df_ranked[mask]
            st.subheader(f"Resultados para: {search_query}")
            if results.empty:
                st.info("No se encontraron coincidencias en esta playlist.")
            else:
                st.dataframe(results)

    # --- Distribución de audio features ---
    # Mostramos las features disponibles, aunque falte alguna
    feature_map = {
        "Danceability": "Danceability",
        "Energy": "Energy",
        "Valence": "Valence",
        "Tempo": "Tempo",
        "duration_ms": "duration_ms",
    }
    available = [col for col in feature_map.values() if col in df_pl.columns]

    if available:
        st.subheader("Distribución de características de audio")
        for col in available:
            st.line_chart(df_pl[col].sort_values().reset_index(drop=True))
        if len(available) < len(feature_map):
            st.info(
                "Se pudieron obtener solo algunas audio features; "
                "algunas columnas faltan en los datos devueltos por Spotify."
            )
    else:
        st.info(
            "No se pudieron obtener audio features "
            "(Danceability, Energy, Valence, Tempo, duration_ms)."
        )

elif playlist_url and not buscar_btn:
    st.info("Pulsa el botón 'Analizar playlist' para descargar y analizar la playlist.")
else:
    st.info("Pega una URL de playlist en la barra lateral y pulsa 'Analizar playlist' para comenzar.")
