import pandas as pd

df = pd.read_csv('abc.csv')
print(df)
distb_df = df.pivot(index='prcbdrBizno', columns='bidNtceNo', values='ejacul_rate')
distb_df.to_csv('distb_df.csv')
print(distb_df)