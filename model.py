import os
import pandas as pd
import numpy as np

from sklearn.linear_model import Ridge
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

player_stats = pd.read_csv("player_stats_cleaned.csv")

rr = Ridge(alpha=1)

split = TimeSeriesSplit(n_splits=3)

sfs = SequentialFeatureSelector(rr, n_features_to_select=12, direction="forward", cv=split, n_jobs=4)

removed_columns = ["Player ID", "Player", "Team", "Experience", "Next_Rating", "Event Title", "Event ID"]
selected_columns = player_stats.columns[~player_stats.columns.isin(removed_columns)]

scaler = MinMaxScaler()
player_stats.loc[:, selected_columns] = scaler.fit_transform(player_stats[selected_columns])

print(player_stats.head())

# def next_season(player):
#     player = player.sort_values("Experience")
#     player["Next_Rating"] = player["Rating"].shift(-1)
#     return player

# player_stats = player_stats.groupby("Player ID", group_keys=False).filter(lambda x: x.shape[0] > 1)
# player_stats = player_stats.groupby("Player ID", group_keys=False).apply(next_season)

# print(player_stats.head())