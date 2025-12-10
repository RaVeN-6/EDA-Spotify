from typing import List

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def boxplots_audio_rock_vs_nonrock(
    df: pd.DataFrame,
    rock_artists: List[str],
    audio_cols: List[str] | None = None,
) -> None:
    """
    Dibuja boxplots comparando audio features entre rock y no-rock.
    """
    if audio_cols is None:
        audio_cols = [
            "Danceability",
            "Energy",
            "Valence",
            "Tempo",
            "Duration_ms",
        ]

    plt.figure(figsize=(14, 8))
    for i, col in enumerate(audio_cols, 1):
        plt.subplot(2, 3, i)
        sns.boxplot(
            data=df,
            x=df["Artist"].isin(rock_artists),
            y=col,
        )
        plt.xticks([0, 1], ["No rock", "Rock"])
        plt.title(col)
    plt.tight_layout()
    plt.show()
