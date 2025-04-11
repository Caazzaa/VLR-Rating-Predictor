import os
import pandas as pd
import numpy as np

player_stats = pd.read_csv("player_stats.csv", index_col=['Date'], parse_dates=True)
print(player_stats.head())
"""
Convert Percentage Columns to Decimal
"""
player_stats["Clutch%"] = player_stats["Clutch%"].str.replace("%", "").astype(float) / 100.0
player_stats["HS%"] = player_stats["HS%"].str.replace("%", "").astype(float) / 100.0
player_stats["KAST"] = player_stats["KAST"].str.replace("%", "").astype(float) / 100.0
player_stats["Clutches (won/played)"] = player_stats["Clutches (won/played)"].str.split("/").str[1].astype(float)
player_stats = player_stats.rename(columns={"Clutches (won/played)": "Clutches Played"})

"""
Convert NaN to 0 or remove columns
"""
player_stats = player_stats.drop(columns=["Agents"])

player_stats = player_stats.reset_index()
nullClutch = np.where(player_stats["Clutch%"].isnull()) 
player_stats.loc[nullClutch[0], "Clutch%"] = 0.0
player_stats.loc[nullClutch[0], "Clutches Played"] = 0
player_stats = player_stats.set_index("Date")

nullHS = np.where(player_stats["HS%"].isnull())
player_stats = player_stats.reset_index()
player_stats.loc[nullHS[0], "HS%"] = 0.0
player_stats = player_stats.set_index("Date")

player_stats.copy()
player_stats = player_stats.dropna(subset=["Rating"])
null_count = player_stats.isnull().sum()
print(null_count)
print(player_stats.describe())
print(player_stats.head())
player_stats = player_stats.sort_index()
print(player_stats)
