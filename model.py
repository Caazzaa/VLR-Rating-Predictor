import os
import pandas as pd
import numpy as np

from sklearn.linear_model import Ridge
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

player_stats = pd.read_csv("player_stats_cleaned.csv", index_col=False)

def next_season(player):
    player = player.sort_values("Experience")
    player["Next_Rating"] = player["Rating"].shift(-1)
    return player

player_stats = player_stats.groupby("Player ID", group_keys=False).filter(lambda x: x.shape[0] > 1)
player_stats = player_stats.groupby("Player ID", group_keys=False).apply(next_season)

print(player_stats.head())