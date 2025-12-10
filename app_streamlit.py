# app_streamlit.py
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

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

buscar_playlist_btn = st.sidebar.button("Analizar playlist")

st.sidebar.markdown("---")

search_query = st.sidebar.text_input(
    "Buscar canción por nombre (global)",
    placeholder="Nombre de la canción o 'artista - título'",
)

buscar_track_btn = st.sidebar.button("Buscar canción")

# ============================================================
# 1) Análisis de playlist por URL
# ============================================================
if playlist_url and buscar_playlist_btn:
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    st.subheader("Análisis de playlist")
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
        st.bar_chart(data=top_tracks.set_index("Track")["popularity"]
                     if "Track" in top_tracks.columns
                     else top_tracks.set_index("track_name")["popularity"])

    # --- Distribución de audio features ---
    feature_cols = {"Danceability", "Energy", "Valence", "Tempo", "duration_ms"}
    available = [col for col in feature_cols if col in df_pl.columns]

    if available:
        st.subheader("Distribución de características de audio")
        for col in available:
            st.line_chart(df_pl[col].sort_values().reset_index(drop=True))
        if len(available) < len(feature_cols):
            st.info(
                "Se pudieron obtener solo algunas audio features; "
                "algunas columnas faltan en los datos devueltos por Spotify."
            )
    else:
        st.info(
            "No se pudieron obtener audio features "
            "(Danceability, Energy, Valence, Tempo, duration_ms)."
        )

# ============================================================
# 2) Búsqueda global de canciones por nombre
# ============================================================
if search_query and buscar_track_btn:
    st.subheader(f"Resultados de búsqueda para: {search_query}")

    with st.spinner("Buscando canciones en Spotify..."):
        try:
            # buscamos pistas por nombre
            results = sp.search(q=search_query, type="track", limit=20)
        except Exception as e:
            st.error(f"Error al buscar canciones: {e}")
            st.stop()

    tracks = results.get("tracks", {}).get("items", [])
    if not tracks:
        st.info("No se encontraron canciones para esa búsqueda.")
    else:
        rows = []
        for t in tracks:
            rows.append(
                {
                    "track_id": t["id"],
                    "Track": t["name"],
                    "Artist": ", ".join(a["name"] for a in t["artists"]),
                    "Album": t["album"]["name"],
                    "popularity": t["popularity"],
                }
            )
        df_search = pd.DataFrame(rows)
        st.dataframe(df_search)

else:
    if not (playlist_url or search_query):
        st.info(
            "Pega una URL de playlist y pulsa 'Analizar playlist', "
            "o escribe el nombre de una canción y pulsa 'Buscar canción'."
        )
