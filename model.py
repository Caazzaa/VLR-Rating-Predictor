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

removed_columns = ["Player ID", "Player", "Team", "Experience", "Next_Rating", "Event Title", "Event Number"]
selected_columns = player_stats.columns[~player_stats.columns.isin(removed_columns)]

print(player_stats[selected_columns].head())

scaler = MinMaxScaler()
player_stats.loc[:, selected_columns] = scaler.fit_transform(player_stats[selected_columns])

print(player_stats.head())
print(player_stats.describe())
print(player_stats.isnull().sum())

sfs.fit(player_stats[selected_columns], player_stats["Next_Rating"])
predictors = list(selected_columns[sfs.get_support()])

print(sorted(player_stats["Event Number"].unique()))

def backtest(data, model, predictors, start=100, step=1):
    all_preds = []
    events = sorted(data["Event Number"].unique())
    for i in range(start, len(events), step):
        current_event = events[i]
        train = data[data["Event Number"] < current_event]
        test = data[data["Event Number"] == current_event]

        model.fit(train[predictors], train["Next_Rating"])

        preds = model.predict(test[predictors])
        preds = pd.Series(preds, index=test.index, name="Predicted Rating")
        combined = pd.concat([test["Next_Rating"], preds], axis=1)
        combined.columns = ["Actual Rating", "Predicted Rating"]
        all_preds.append(combined)
    
    return pd.concat(all_preds)

predictions = backtest(player_stats, rr, predictors, start=5, step=1)
print(predictions)
print((mean_squared_error(predictions["Actual Rating"], predictions["Predicted Rating"]))**0.5)
print(player_stats["Next_Rating"].describe())
