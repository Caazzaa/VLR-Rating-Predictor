import os
import pandas as pd
import numpy as np

from sklearn.linear_model import Ridge
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

player_stats = pd.read_csv("player_stats_cleaned.csv", index_col=False)

rr = Ridge(alpha=1)

split = TimeSeriesSplit(n_splits=3)

sfs = SequentialFeatureSelector(rr, n_features_to_select=16, direction="forward", cv=split, n_jobs=4)

removed_columns = ["Player ID", "Player", "Team", "Next_Rating", "Event Title", "Event Number"]
selected_columns = player_stats.columns[~player_stats.columns.isin(removed_columns)]

scaler = MinMaxScaler()
player_stats.loc[:, selected_columns] = scaler.fit_transform(player_stats[selected_columns])

valid_data = player_stats.dropna(subset=["Next_Rating"])
sfs.fit(valid_data[selected_columns], valid_data["Next_Rating"])
predictors = list(selected_columns[sfs.get_support()])

def backtest(data, model, predictors, start=120, step=1):
    all_preds = []
    events = sorted(data["Event Number"].unique())
    for i in range(start, len(events), step):
        current_event = events[i]
        train = data[data["Event Number"] < current_event]
        test = data[data["Event Number"] == current_event]

        train = train.dropna(subset=["Next_Rating"])

        model.fit(train[predictors], train["Next_Rating"])

        preds = model.predict(test[predictors])
        preds = pd.Series(preds, index=test.index, name="Predicted Rating")

        combined = pd.concat([test["Next_Rating"], preds], axis=1)
        combined.columns = ["Actual Rating", "Predicted Rating"]
        combined["Player"] = test["Player"].values
        combined["Event Title"] = test["Event Title"].values

        all_preds.append(combined)
    
    return pd.concat(all_preds)

def player_history(df):
    df = df.sort_values("Event Number")

    df["rating_diff"] = df["Rating"] / df["Rating"].shift(1)
    df["rating_diff"] = df["rating_diff"].fillna(1)
    df.loc[df["rating_diff"] == np.inf, "rating_diff"] = 1.0

    df["rating_corr"] = list(df[["Experience", "Rating"]].expanding().corr().loc[(slice(None), "Experience"), "Rating"])
    df["rating_corr"] = df["rating_corr"].fillna(1)

    return df

def group_avgs(df):
    return df["Rating"] / df["Rating"].mean()


player_stats = player_stats.groupby("Player ID", group_keys=False).apply(player_history)
player_stats["rating_season"] = player_stats.groupby("Event Number", group_keys=False).apply(group_avgs)

new_predictors = predictors + ["rating_diff", "rating_corr", "rating_season"]

print(player_stats["Next_Rating"].describe())

new_predictions = backtest(player_stats, rr, new_predictors, start=5, step=1)
print(new_predictions.isnull().sum())
print(new_predictions[new_predictions["Event Title"] == "Champions Tour 2025: EMEA Stage 1"])
check_error = new_predictions.dropna(subset=["Actual Rating"])
print((mean_squared_error(check_error["Actual Rating"], check_error["Predicted Rating"]))**0.5)

"""
TODOs:
- Predict Future Ratings: DONE
- Explore other models beside ridge regression
- Engineer knew features to give better context
- Allow user input to grab the future predictions or predictions for specific player or event
"""


