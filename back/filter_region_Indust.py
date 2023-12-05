import pandas as pd
import re

def license(df, license):
    df['lcnsLmtNm'] = df['lcnsLmtNm'].apply(lambda x: re.sub(r'/|\b\d{4}\b', '', x))        # 면허리스트 에서 코드부분(/9999형식)을 삭제
    group_ex = df.groupby(['bidNtceNo', 'lmtGrpNo'])['lcnsLmtNm'].apply(list).reset_index(name='tlist')
    print('license', group_ex)
    gr = group_ex[group_ex['tlist'].apply(lambda x: x == license)]
    return gr

def region(df, region):
    group_ex = df.groupby(['bidNtceNo', 'bidNtceOrd'])['prtcptPsblRgnNm'].apply(list).reset_index(name='tlist')         #참가 가능지역을 리스트화 한다.
    group_ex['cnt'] = group_ex['tlist'].apply(lambda x: str_count(region, x))
    rt_df = group_ex[group_ex['cnt'].apply(lambda x: x == True)]
    return rt_df

    #region 종속함
def str_count(str, st_lst):
    #print(str, st_lst)

    if len(st_lst) == 1:            # 리스트가 1개일경우는 인천광역시 만의 값만 받아들이기 위함.
        if st_lst[0] != str:
            return False

    count = sum(1 for s in st_lst if str in s)
    if count == len(st_lst):
        return True
    else: return False