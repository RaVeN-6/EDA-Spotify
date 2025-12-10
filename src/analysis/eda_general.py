import pandas as pd


NUMERIC_COLS_DEFAULT = [
    "Danceability",
    "Energy",
    "Valence",
    "Tempo",
    "Duration_ms",
    "Stream",
]


def summarize_nulls(df: pd.DataFrame) -> pd.Series:
    """Cuenta nulos por columna, de mayor a menor."""
    return df.isna().sum().sort_values(ascending=False)


def numeric_describe(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
    """Devuelve describe().T para columnas numéricas seleccionadas."""
    if cols is None:
        cols = NUMERIC_COLS_DEFAULT
    return df[cols].describe().T


def top_artists_by_streams(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Top n artistas por suma de Streams."""
    return (
        df.groupby("Artist", as_index=False)["Stream"]
        .sum()
        .sort_values("Stream", ascending=False)
        .head(n)
    )


def top_tracks_by_streams(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Top n canciones por Streams."""
    cols = ["Artist", "Track", "Album", "Stream"]
    return df[cols].sort_values("Stream", ascending=False).head(n)
