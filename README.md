# Análisis de música de Spotify (rock vs no-rock)

Proyecto de análisis exploratorio de datos (EDA) en Python sobre el dataset **Spotify and Youtube** de Kaggle, centrado en comparar canciones de rock frente a otros géneros a partir de sus características de audio y su popularidad (streams).  

## Objetivo

- Explorar las características de audio de canciones populares en Spotify (danceability, energy, valence, tempo, duración, etc.).
- Comparar un subconjunto de artistas de rock con el resto del dataset (no rock).
- Visualizar cómo se relacionan estas características con la popularidad medida en `Stream` (escala logarítmica).

## Dataset

- Fuente: [Spotify and Youtube (Kaggle)](https://www.kaggle.com/datasets/salvatorerastelli/spotify-and-youtube)  
- Tamaño: ~20 700 canciones con 28 columnas (audio features de Spotify + métricas de YouTube y Streams).  
- El CSV se guarda en `data/raw/spotify.csv`.  

## Tecnologías

- Python 3.x
- pandas, numpy
- matplotlib, seaborn
- Jupyter Notebook

Para reproducir el entorno se recomienda instalar las dependencias desde `requirements.txt`.

## Estructura del repositorio

spotify_rock/
data/
raw/
spotify.csv
notebooks/
01_eda_general.ipynb
src/
config/
paths.py
data/
loading.py
analysis/
eda_general.py
rock_features.py
viz/
plots_rock.py
tests/
...
README.md
requirements.txt

## Cómo ejecutar el análisis

1. Clonar el repositorio y entrar en la carpeta del proyecto.
2. Crear y activar un entorno virtual.
3. Instalar dependencias:


4. Descargar el dataset de Kaggle y guardarlo como `data/raw/spotify.csv`.
5. Abrir `notebooks/01_eda_general.ipynb` y ejecutar las celdas en orden.

## Resumen de hallazgos

- La mayoría de las canciones del dataset se concentran en niveles medios-altos de **energy** y **danceability**, con tempos en torno a 100–130 bpm y duraciones cerca de 3–4 minutos, algo consistente con otros análisis de canciones populares en Spotify.[memory:16][web:79]  
- El mapa de calor de correlaciones muestra que **energy**, **danceability** y **valence** tienen correlación positiva moderada con los `Stream`, mientras que la duración tiene una relación más débil.[memory:16][web:54]  
- En el subconjunto de rock (Metallica, Red Hot Chili Peppers, Linkin Park, Radiohead, AC/DC, Gorillaz), las canciones presentan **energy** más alta y duraciones ligeramente mayores que el resto del dataset.[memory:11][web:32]  
- En los scatterplots de **Energy/Valence vs Streams** (escala log), las canciones de rock más reproducidas aparecen principalmente con energy alta y valence en rangos medios, indicando temas intensos pero no necesariamente los más “felices” según la métrica de valence.[memory:11][web:52]  

## Futura Version

- Incluir más artistas y subgéneros de rock para robustecer el subconjunto.
- Añadir métricas derivadas (por ejemplo, ratios de YouTube como Likes/Views).
- Explorar modelos simples (sin llegar a ML complejo) que expliquen mejor la variación en Streams.
