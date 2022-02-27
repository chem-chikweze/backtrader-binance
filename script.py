import csv 
import pandas as pd
import numpy as np
from pandas.core.indexes.base import Index

def new_name(name = "dataset/4hr.csv"):
    new_csv = name.split("/")[-1].split(".")[0]
    return new_csv

def sort(name = "dataset/4hr.csv" ):
    df = pd.read_csv(name)
    rslt_df = df.sort_values(by = 'change')
    print(rslt_df.columns)
    # rslt_df = rslt_df.drop(columns =['number','sign'], axis = 1)
    print(rslt_df)
    sort_name = new_name(name)
    rslt_df.to_csv("dataset/sort{}.csv".format(sort_name), index=False)

def my_floor(a, precision=0):
    return np.true_divide(np.floor(a * 10**precision), 10**precision)

def decimal_place(df, dp= 3 ):
    d = my_floor(df, dp)
    return d


def difference_between_zig_and_dataclose(name="dataset/diff.csv"):
    df = pd.read_csv(name)
    print(df)
    df["ratio"] = df['act']/df["zig"]
    df["perfect"] = df["zig"].div(df["zig"].shift(1)).fillna(df["zig"])
    
    new_csv = name.split("/")[-1].split(".")[0]
    df.to_csv("{}diff.csv".format(new_csv), index=False)

def seperate_zigs(df, name):
    # row_0 = decimal_place(df.iloc[0::2])
    # row_1 = decimal_place( df.iloc[1::2])    
    row_0 = (df.iloc[0::2])
    row_1 = ( df.iloc[1::2])
    row_0.to_csv("dataset/{}low.csv".format(name), index= False)
    row_1.to_csv("dataset/{}high.csv".format(name), index= False)
    # return pd.concat([row_0, row_1], axis=1)



def createZigAbstract(name="dataset/4hr.csv"):
    df = pd.read_csv(name)
    df['change'] = df['number'].div(df['number'].shift(1))
    # df['change'] = df.div(df['number'].shift(1)).fillna(df['change']).astype(int)
    new_csv = name.split("/")[-1].split(".")[0]
    df.to_csv("dataset/{}diff.csv".format(new_csv), index=False)
    sorted_df = df['change'].sort_values()

    # seperate 
    seperate_zigs(df['change'], new_csv)

    sorted_df.to_csv("dataset/SORT{}.csv".format(new_csv), index=False)
    decimal_place(sorted_df, new_csv).to_csv("dataset/DECP{}.csv".format(new_csv), index=False)

def tabb (self):
    df = pd.read_csv("dataset/track.csv")

    # df = dfa["f"]
    # df[1:]/df[0:]
    # print(df.head())

    df["g"] = df["f"].div(df["f"].shift(1)).fillna(df["f"])
    # applytab(df)
    # df.to_csv("d.csv", index=False)

    def applytab(row):
        print('\t'.join(map(str,row.values)))

    for index, row in df.iterrows():
        applytab(row)

name = "dataset/stan1hr.csv"
createZigAbstract(name)
# sort(name)
# sort()
# decimal_place()