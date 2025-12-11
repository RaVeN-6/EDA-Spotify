# app_streamlit.py
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Ajustar ruta /src
BASE_DIR = Path(__file__).resolve().parents[0]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data.spotify_api import get_spotify_client, fetch_playlist_tracks_with_features


# ============================================================
# Configuración inicial
# ============================================================
st.set_page_config(page_title="Spotify Analyzer", layout="wide")
st.title("🎧 Analizador de Spotify")

@st.cache_resource
def get_client():
    return get_spotify_client()

try:
    sp = get_client()
except Exception as e:
    st.error(f"Error creando cliente Spotify: {e}")
    st.stop()


# ============================================================
# Menú lateral
# ============================================================
st.sidebar.header("¿Qué deseas hacer?")
modo = st.sidebar.radio(
    "Selecciona una opción:",
    ["Analizar Playlist", "Buscar (Artista / Canción)"]
)
st.sidebar.markdown("---")


# ============================================================
# 1) ANALIZAR PLAYLIST
# ============================================================
if modo == "Analizar Playlist":

    st.subheader("📌 Análisis de Playlist por URL")

    playlist_url = st.sidebar.text_input(
        "Pega la URL de la playlist",
        placeholder="https://open.spotify.com/playlist/..."
    )

    analizar_btn = st.sidebar.button("Analizar playlist")

    if playlist_url and analizar_btn:

        playlist_id = playlist_url.split("/")[-1].split("?")[0]

        with st.spinner("Descargando playlist y audio features..."):
            df = fetch_playlist_tracks_with_features(sp, playlist_id)

        if df.empty:
            st.error("No se encontraron canciones en la playlist.")
            st.stop()

        st.success("Playlist cargada correctamente ✔")

        # ---------------------------------------------------
        # TABLA PRINCIPAL
        # ---------------------------------------------------
        st.subheader("📋 Tabla General de Canciones")
        st.dataframe(df)

        # Convertir fechas a año
        df["Year"] = pd.to_datetime(df["Release_Date"], errors="coerce").dt.year

        # ---------------------------------------------------
        # TOP ARTISTAS
        st.subheader("🎤 Artistas más frecuentes")
        artists_count = df["Artist"].value_counts().head(10)
        st.bar_chart(artists_count)

        # ---------------------------------------------------
        # TOP ÁLBUMES
        st.subheader("💿 Álbumes más frecuentes")
        album_count = df["Album"].value_counts().head(10)
        st.bar_chart(album_count)

        # ---------------------------------------------------
        # DISTRIBUCIÓN DE POPULARIDAD
        st.subheader("🔥 Distribución de Popularidad")
        st.line_chart(df["Popularity"].sort_values().reset_index(drop=True))

        # ---------------------------------------------------
        # FECHAS DE LANZAMIENTO
        st.subheader("📅 Años de Lanzamiento")
        year_counts = df["Year"].value_counts().sort_index()
        st.bar_chart(year_counts)

        # ---------------------------------------------------
        # AUDIO FEATURES
        feature_cols = ["Energy", "Danceability", "Valence", "Tempo",
                        "Acousticness", "Instrumentalness", "Liveness", "Speechiness"]

        for col in feature_cols:
            if col in df:
                st.subheader(f"🎼 Distribución de {col}")
                st.line_chart(df[col].sort_values().reset_index(drop=True))


# ============================================================
# 2) BUSCADOR ARTISTA / CANCIÓN / AMBOS
# ============================================================
else:

    st.subheader("🔍 Buscador General")

    artist_query = st.text_input("Nombre del artista (opcional)")
    song_query = st.text_input("Nombre de la canción (opcional)")

    buscar_btn = st.button("Buscar")

    if buscar_btn:

        aq = artist_query.strip().lower()
        sq = song_query.strip().lower()

        # -------------------------------------------
        # SOLO ARTISTA
        # -------------------------------------------
        if aq and not sq:
            with st.spinner("Buscando artista..."):
                results = sp.search(q=f'artist:"{artist_query}"', type="artist", limit=5)

            artists = results["artists"]["items"]
            if not artists:
                st.info("No se encontró el artista.")
                st.stop()

            artist = artists[0]
            artist_name = artist["name"]
            artist_id = artist["id"]

            st.markdown(f"### 🎤 Canciones de **{artist_name}**")

            top = sp.artist_top_tracks(artist_id, country="US")
            tracks = top.get("tracks", [])

            rows = [{
                "Track": t["name"],
                "Album": t["album"]["name"],
                "Popularity": t["popularity"],
                "ID": t["id"]
            } for t in tracks]

            st.dataframe(pd.DataFrame(rows))
            st.stop()

        # -------------------------------------------
        # SOLO CANCIÓN
        # -------------------------------------------
        if sq and not aq:
            with st.spinner("Buscando canciones..."):
                results = sp.search(q=f'track:"{song_query}"', type="track", limit=20)

            tracks = results["tracks"]["items"]
            if not tracks:
                st.info("No se encontraron canciones.")
                st.stop()

            rows = []
            for t in tracks:
                rows.append({
                    "Track": t["name"],
                    "Artist": ", ".join(a["name"] for a in t["artists"]),
                    "Album": t["album"]["name"],
                    "Popularity": t["popularity"],
                    "ID": t["id"]
                })

            df = pd.DataFrame(rows)
            df = df[df["Track"].str.lower().str.contains(sq)]
            st.dataframe(df)
            st.stop()

        # -------------------------------------------
        # ARTISTA + CANCIÓN (COINCIDENCIA PARCIAL)
        # -------------------------------------------
        if aq and sq:

            query = f'track:"{song_query}" artist:"{artist_query}"'

            with st.spinner("Buscando coincidencias..."):
                results = sp.search(q=query, type="track", limit=20)

            tracks = results["tracks"]["items"]

            if not tracks:
                results = sp.search(q=f'track:"{song_query}"', type="track", limit=20)
                tracks = results["tracks"]["items"]

            rows = []
            for t in tracks:
                rows.append({
                    "Track": t["name"],
                    "Artist": ", ".join(a["name"] for a in t["artists"]),
                    "Album": t["album"]["name"],
                    "Popularity": t["popularity"],
                    "ID": t["id"]
                })

            df = pd.DataFrame(rows)

            df = df[
                df["Track"].str.lower().str.contains(sq) &
                df["Artist"].str.lower().str.contains(aq)
            ]

            if df.empty:
                st.warning("No se encontraron coincidencias.")
            else:
                st.dataframe(df)
