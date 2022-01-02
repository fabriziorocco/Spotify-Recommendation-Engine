import pandas as pd

df = pd.read_csv("spotify_raw.csv")

#Missing Values
df.dropna(inplace = True)
print(df.isnull().sum())
#no missing values

#Dropping useless features
# df.drop(["track_id"], axis =1, inplace = True)
# print (df)

#determining correlations
corr_df = df.corr(method = "pearson")
list_for_correlations = []
for g in range(len(corr_df.columns)):
    correlated_variables = []
    for i in range(len(corr_df[corr_df.columns[g]])):
        if corr_df[corr_df.columns[g]][i] > 0.65:
            correlated_variables.append(corr_df.index[i])
    dict_with_correlations = {corr_df.columns[g]:correlated_variables}
    list_for_correlations.append(dict_with_correlations)

print(list_for_correlations) #dictionaries with more than two values exhibit correlation
#we found high correlation between energy and loudness. We drop loudness
df.drop(["loudness"], axis =1, inplace = True)
print(df)
df.to_csv("spotify_pre_processed.csv", index=False)