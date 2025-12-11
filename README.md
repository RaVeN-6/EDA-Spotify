# 🎸 Analizador de Música en Spotify (RaVeN-6)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)
![Libraries](https://img.shields.io/badge/pandas-numpy-orange?style=for-the-badge)
![Viz](https://img.shields.io/badge/matplotlib-seaborn-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

> Un proyecto de Exploración de Datos (EDA) para descubrir qué hace popular a una canción y cómo el Rock se diferencia del resto, utilizando datos de Spotify y YouTube.

## 📋 Descripción

Este proyecto realiza un análisis exhaustivo sobre el dataset **"Spotify and Youtube"** de Kaggle. El objetivo principal es desglosar las características de audio (como *energy*, *danceability*, *valence*) y entender su relación con la popularidad (*streams*).

Además, incluye un módulo especial para interactuar con la **API de Spotify**, permitiendo analizar tus propias playlists en tiempo real.

## 🎯 Objetivos del Proyecto

1.  **Perfilado de Audio:** Analizar la distribución de métricas clave (tempo, duración, energía) en canciones exitosas.
2.  **Rock vs. El Mundo:** Comparar un subconjunto de artistas de Rock legendarios (Metallica, RHCP, AC/DC, etc.) contra el resto del panorama musical.
3.  **Factores de Éxito:** Visualizar correlaciones entre las características de la canción y su éxito en reproducciones (`Stream`).
4.  **Herramienta Personalizada:** Proveer un script para analizar cualquier playlist pública de Spotify mediante su API.

## 📂 Estructura del Repositorio

El proyecto sigue una estructura modular para separar los datos crudos, el procesamiento y la visualización.

```text
spotify_rock/
├── data/
│   ├── raw/
│   │   └── spotify.csv       # Dataset original (descargar de Kaggle)
├── notebooks/
│   ├── 01_eda_general.ipynb  # Análisis principal y visualizaciones estáticas
│   └── 02_playlist.ipynb     # Análisis en vivo con API de Spotify
├── src/
│   ├── config/               # Configuraciones y rutas
│   ├── data/                 # Scripts de carga y limpieza
│   ├── analysis/             # Lógica de negocio y estadística
│   └── viz/                  # Funciones de ploteo
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Documentación

Instalación y Requisitos
Prerrequisitos
Python 3.x

Cuenta de Spotify Developer (opcional, solo para el análisis de playlists)

Paso a paso
Clonar el repositorio:
git clone [https://github.com/RaVeN-6/EDA-Spotify.git](https://github.com/RaVeN-6/EDA-Spotify.git)
cd EDA-Spotify

# Windows
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

Configurar Datos:

Descarga el dataset desde Kaggle: Spotify and Youtube.

Coloca el archivo Spotify_Youtube.csv en la carpeta data/raw/ y renómbralo a spotify.csv.

📊 Cómo ejecutar el análisis
A. Análisis Exploratorio (Dataset Kaggle)
Para ver los resultados del estudio sobre Rock y tendencias generales:

Abre Jupyter Notebook: jupyter notebook

Navega a notebooks/01_eda_general.ipynb.

Ejecuta todas las celdas secuencialmente.

B. Modo Playlist Personalizada (API Spotify)
Para analizar tu propia música:

Crea una app en el Dashboard de Spotify for Developers.

Obtén tu Client ID y Client Secret.

Configura tus variables de entorno (o crea un archivo .env):

export SPOTIFY_CLIENT_ID='tu_id_aqui'
export SPOTIFY_CLIENT_SECRET='tu_secreto_aqui'
export SPOTIFY_REDIRECT_URI='http://localhost:8888/callback'

jecuta el notebook notebooks/02_playlist_analysis.ipynb e introduce el enlace de tu playlist.

💡 Resumen de Hallazgos
A continuación, algunos de los descubrimientos más interesantes tras el análisis:

⚡ El estándar del éxito: Las canciones populares tienden a concentrarse en niveles medio-altos de energy y danceability, con un tempo estándar de 100–130 BPM.

🔗 Correlaciones: Existe una correlación positiva moderada entre energy/danceability y el número de Streams. La duración de la canción, sin embargo, tiene poca influencia en el éxito actual.

🎸 La Huella del Rock: El subconjunto analizado (Metallica, Linkin Park, Gorillaz, etc.) muestra niveles de energía superiores al promedio y duraciones más largas.

💔 Intensidad vs. Felicidad: En el Rock, las canciones con más streams suelen tener mucha Energy pero Valence (positividad) media o baja. Son temas intensos, no necesariamente "felices".

🔮 Roadmap (Próximos Pasos)
[ ] Ampliar el dataset de Rock con más subgéneros (Indie, Metal, Classic).

[ ] Implementar métricas derivadas (ej: Ratio Likes/Views de YouTube).

[ ] Crear un modelo de regresión simple para predecir Streams basado en audio features.

[ ] Exportar los resultados de la playlist a un reporte PDF/HTML.

Desarrollado con ❤️ por RaVeN-6