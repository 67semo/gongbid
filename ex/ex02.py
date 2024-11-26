# 순공사원가를 기준으로 한 투찰 보인트 분석
import pandas as pd

df = pd.read_csv('../gui/acb.csv')
#순공사원가
val = 563224473 * .98
df['ejacul_rate'] = df['bidprcAmt']/val
print(df)
df.to_csv('../gui/acb.csv')