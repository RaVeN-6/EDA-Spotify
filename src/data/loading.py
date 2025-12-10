import pandas as pd
from config.paths import SPOTIFY_RAW_CSV


def load_spotify_raw() -> pd.DataFrame:
    """
    Carga el CSV principal de Spotify desde data/raw.
    """
    df = pd.read_csv(SPOTIFY_RAW_CSV)
    return df
