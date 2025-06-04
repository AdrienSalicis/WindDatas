import pandas as pd

def merge_datasets(df1, df2, col1, col2):
    if col1 not in df1.columns or col2 not in df2.columns:
        return pd.DataFrame()

    df1_clean = df1[['time', col1]].dropna().copy()
    df2_clean = df2[['time', col2]].dropna().copy()

    df1_clean['time'] = pd.to_datetime(df1_clean['time'])
    df2_clean['time'] = pd.to_datetime(df2_clean['time'])

    merged = pd.merge(df1_clean, df2_clean, on='time')
    return merged
