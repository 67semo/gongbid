import pandas as pd
import re

pd.set_option('display.max_column', 10)
pd.set_option('display.max_colwidth', 20)
pd.set_option('display.unicode.east_asian_width', True)

def license():
    df = pd.read_csv('../gui/ad.csv')
    df['lcnsLmtNm'] = df['lcnsLmtNm'].apply(lambda x: re.sub(r'/|\b\d{4}\b', '', x))        # 면허리스트 에서 코드부분(/9999형식)을 삭제
    group_ex = df.groupby(['bidNtceNo', 'lmtGrpNo'])['lcnsLmtNm'].apply(list).reset_index(name='tlist')
    print('license', group_ex)
    selec = ['기계설비,가스공사업']
    gr = group_ex[group_ex['tlist'].apply(lambda x: x == selec)]
    return gr

def region():
    df = pd.read_csv('../gui/ac.csv')
    group_ex = df.groupby(['bidNtceNo', 'bidNtceOrd'])['prtcptPsblRgnNm'].apply(list).reset_index(name='tlist')         #참가 가능지역을 리스트화 한다.
    selec = '인천광역시'
    group_ex['cnt'] = group_ex['tlist'].apply(lambda x: str_count(selec, x))
    rt_df = group_ex[group_ex['cnt'].apply(lambda x: x == True)]
    return rt_df

def str_count(str, st_lst):
    #print(str, st_lst)

    if len(st_lst) == 1:            # 리스트가 1개일경우는 인천광역시 만의 값만 받아들이기 위함.
        if st_lst[0] != str:
            return False

    count = sum(1 for s in st_lst if str in s)
    if count == len(st_lst):
        return True
    else: return False

if __name__ == '__main__':
    df1 = license()
    df2 = region()
    itsn = pd.merge(df1, df2, on='bidNtceNo')
    print(itsn)