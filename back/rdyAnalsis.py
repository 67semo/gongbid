import pandas as pd

df1 = pd.read_csv("../gui/acb.csv", index_col=0)
df2 = pd.read_csv("../gui/acb2.csv", index_col=0)

bizNo = df1.prcbdrBizno.unique()
df11 = df2[df2['prcbdrBizno'].isin(bizNo)]
df12 = df1[df1['prcbdrBizno'].isin(df11.prcbdrBizno.unique())]

df21 = pd.concat([df11, df12], ignore_index=True)

print(df21)
df21.to_csv("../gui/acb.csv")