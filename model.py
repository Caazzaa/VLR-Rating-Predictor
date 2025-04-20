import os
import pandas as pd
import numpy as np

from sklearn.linear_model import Ridge
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

player_stats = pd.read_csv("player_stats_cleaned.csv", index_col=False)

player_stats_full = player_stats.copy()
player_stats = player_stats.dropna(subset=["Next_Rating"])

rr = Ridge(alpha=1)

split = TimeSeriesSplit(n_splits=3)

sfs = SequentialFeatureSelector(rr, n_features_to_select=15, direction="forward", cv=split, n_jobs=4)

removed_columns = ["Player ID", "Player", "Team", "Experience", "Next_Rating", "Event Title", "Event ID"]
selected_columns = player_stats.columns[~player_stats.columns.isin(removed_columns)]

print(player_stats[selected_columns].head())

scaler = MinMaxScaler()
player_stats.loc[:, selected_columns] = scaler.fit_transform(player_stats[selected_columns])

print(player_stats.head())
print(player_stats.describe())
print(player_stats.isnull().sum())

sfs.fit(player_stats[selected_columns], player_stats["Next_Rating"])
predictors = list(selected_columns[sfs.get_support()])

print(selected_columns)
print(predictors)