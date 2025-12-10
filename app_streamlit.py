# app_streamlit.py
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# --- Ajuste del PATH para importar desde /src ---
BASE_DIR = Path(__file__).resolve().parents[0]
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from data.spotify_api import get_spotify_client, fetch_playlist_tracks_with_features


# ============================================================
# 0) CONFIGURACIÓN INICIAL
# ============================================================
st.set_page_config(page_title="Spotify Analyzer", layout="wide")
st.title("🎧 Analizador de Spotify")

@st.cache_resource
def get_client():
    return get_spotify_client()


# --- Cliente Spotify ---
try:
    sp = get_client()
except Exception as e:
    st.error(f"Error creando cliente: {e}")
    st.stop()


# ============================================================
# SELECTOR PRINCIPAL
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
        "Pega la URL de una playlist",
        placeholder="https://open.spotify.com/playlist/..."
    )

    analizar_btn = st.sidebar.button("Analizar playlist")

    if playlist_url and analizar_btn:

        playlist_id = playlist_url.split("/")[-1].split("?")[0]

        with st.spinner("Descargando playlist..."):
            try:
                df_pl = fetch_playlist_tracks_with_features(sp, playlist_id)
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

        if df_pl.empty:
            st.error("No se encontraron canciones.")
            st.stop()

        st.subheader("📊 Resumen de la Playlist")
        st.write(f"Número de canciones: **{len(df_pl)}**")

        st.dataframe(df_pl.head(20))


# ============================================================
# 2) BUSCADOR (ARTISTA / CANCIÓN / AMBOS)
# ============================================================
else:

    st.subheader("🔍 Buscador General")

    artist_query = st.text_input("Nombre del artista (opcional)")
    song_query = st.text_input("Nombre de la canción (opcional)")

    buscar_btn = st.button("Buscar")


    if buscar_btn:

        artist_q = artist_query.strip().lower()
        song_q = song_query.strip().lower()

        # -------------------------------------------
        # CASO A: Solo ARTISTA
        # -------------------------------------------
        if artist_q and not song_q:
            with st.spinner("Buscando artista..."):
                results = sp.search(q=f'artist:"{artist_query}"', type="artist", limit=5)

            artists = results.get("artists", {}).get("items", [])
            if not artists:
                st.info("No se encontró el artista.")
                st.stop()

            artist = artists[0]
            artist_id = artist["id"]
            artist_name = artist["name"]

            st.markdown(f"### 🎤 Canciones de **{artist_name}**")

            top = sp.artist_top_tracks(artist_id, country="US")
            tracks = top.get("tracks", [])

            filas = [{
                "Track": t["name"],
                "Album": t["album"]["name"],
                "Popularity": t["popularity"],
                "ID": t["id"]
            } for t in tracks]

            st.dataframe(pd.DataFrame(filas))
            st.stop()


        # -------------------------------------------
        # CASO B: Solo CANCIÓN
        # -------------------------------------------
        if song_q and not artist_q:

            with st.spinner("Buscando canciones..."):
                results = sp.search(q=f'track:"{song_query}"', type="track", limit=20)

            tracks = results.get("tracks", {}).get("items", [])
            if not tracks:
                st.info("No se encontraron canciones.")
                st.stop()

            filas = []
            for t in tracks:
                filas.append({
                    "Track": t["name"],
                    "Artist": ", ".join(a["name"] for a in t["artists"]),
                    "Album": t["album"]["name"],
                    "Popularity": t["popularity"],
                    "ID": t["id"]
                })

            df = pd.DataFrame(filas)

            # Coincidencia parcial
            df = df[df["Track"].str.lower().str.contains(song_q)]

            st.dataframe(df)
            st.stop()


        # -------------------------------------------
        # CASO C: ARTISTA + CANCIÓN (coincidencia parcial)
        # -------------------------------------------
        if artist_q and song_q:

            query = f'track:"{song_query}" artist:"{artist_query}"'

            with st.spinner("Buscando coincidencias..."):
                results = sp.search(q=query, type="track", limit=20)

            tracks = results.get("tracks", {}).get("items", [])

            if not tracks:
                st.info("No hay coincidencias exactas, se aplicará filtro flexible...")
                # Búsqueda flexible
                results = sp.search(q=f'track:"{song_query}"', type="track", limit=20)
                tracks = results.get("tracks", {}).get("items", [])

            filas = []
            for t in tracks:
                filas.append({
                    "Track": t["name"],
                    "Artist": ", ".join(a["name"] for a in t["artists"]),
                    "Album": t["album"]["name"],
                    "Popularity": t["popularity"],
                    "ID": t["id"]
                })

            df = pd.DataFrame(filas)

            # Filtro flexible
            df = df[
                df["Track"].str.lower().str.contains(song_q) &
                df["Artist"].str.lower().str.contains(artist_q)
            ]

            if df.empty:
                st.warning("No se encontraron coincidencias parciales.")
            else:
                st.dataframe(df)
