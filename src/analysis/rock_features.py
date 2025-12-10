from typing import List, Tuple

import pandas as pd


DEFAULT_ROCK_ARTISTS = [
    "Red Hot Chili Peppers",
    "Metallica",
    "Linkin Park",
    "Radiohead",
    "AC/DC",
    "Gorillaz",
]


def split_rock_nonrock(
    df: pd.DataFrame,
    rock_artists: List[str] | None = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Separa el DataFrame en dos: canciones de artistas de rock y resto.
    """
    if rock_artists is None:
        rock_artists = DEFAULT_ROCK_ARTISTS

    mask_rock = df["Artist"].isin(rock_artists)
    df_rock = df[mask_rock].copy()
    df_no_rock = df[~mask_rock].copy()
    return df_rock, df_no_rock


def audio_stats_by_group(
    df_rock: pd.DataFrame,
    df_no_rock: pd.DataFrame,
    audio_cols: List[str] | None = None,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Devuelve estadísticas descriptivas (describe().T) para rock y no-rock.
    """
    if audio_cols is None:
        audio_cols = [
            "Danceability",
            "Energy",
            "Valence",
            "Tempo",
            "Duration_ms",
        ]

    rock_stats = df_rock[audio_cols].describe().T
    no_rock_stats = df_no_rock[audio_cols].describe().T
    return rock_stats, no_rock_stats
