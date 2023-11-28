import pandas as pd
import re

df = pd.read_csv('../gui/ad.csv')

df['lcns_lt'] = re.sub(r'/|\b\d{4}\b', '', str(df['lcnsLmtNm']))
result = df.groupby(['bidNtceNo', 'lmtGrpNo']).agg({'lcnsLmtNm': list, 'lcns_lt': list}).reset_index()
print(result)
