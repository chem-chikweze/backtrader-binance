import csv 
import pandas as pd

df = pd.read_csv("dataset/track.csv")

# df = dfa["f"]
# df[1:]/df[0:]
# print(df.head() )

df["g"] = df["f"].div(df["f"].shift(1)).fillna(df["f"])

# applytab(df)
# df.to_csv("d.csv", index=False)

def applytab(row):
    print('\t'.join(map(str,row.values)))

for index, row in df.iterrows():
    applytab(row)