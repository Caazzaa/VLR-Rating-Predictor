import os
import pandas as pd
import numpy as np

player_stats = pd.read_csv("player_stats.csv", index_col=['Date'], parse_dates=True)
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

"""
Split Player/Team into Player and Team
"""
player_stats["Player"] = player_stats["Player/Team"].str.split(" ", expand=True)[0]
player_stats["Team"] = player_stats["Player/Team"].str.split(" ", expand=True)[1].str.replace(" ", "").str.strip()
player_stats = player_stats.drop(columns=["Player/Team"])

# Reorder columns to make Player and Team the first and second columns
columns_order = ["Player ID", "Player", "Team"] + [col for col in player_stats.columns if col not in ["Player ID", "Player", "Team"]]
player_stats = player_stats[columns_order]

"""
Sort by Date
"""
player_stats = player_stats.sort_values(by=["Date"])

"""
add column to denoate the event experience of the player
"""
player_stats["Experience"] = player_stats.groupby("Player ID").cumcount() + 1

"""
Update CSV file
"""

player_stats.to_csv("player_stats_cleaned.csv", index=False)
print("Player stats cleaned and saved to player_stats.csv")