scaler = MinMaxScaler()
# player_stats.loc[:, selected_columns] = scaler.fit_transform(player_stats[selected_columns])

# print(player_stats.head())
# print(player_stats.describe())
# # print(player_stats.isnull().sum())

# sfs.fit(player_stats[selected_columns], player_stats["Next_Rating"])
# predictors = list(selected_columns[sfs.get_support()])