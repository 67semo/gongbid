import pandas as pd
import re

df = pd.read_csv('../gui/ad.csv')

df['lcns_lt'] = re.sub(r'/|\b\d{4}\b', '', str(df['lcnsLmtNm']))
#result = df.groupby('bidNtceNo').agg({'lcns_lt': list}).reset_index()
#result.to_csv('ab.csv')


#group_ex = df.groupby(['bidNtceNo', 'lmtGrpNo'])['lcns_lt'].apply(list).reset_index(name='tlist')
group_ex = df.groupby(['bidNtceNo', 'lmtGrpNo'])['lcns_lt']
#group_ex.to_csv('ab.csv')
