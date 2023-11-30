import pandas as pd
import re


def license():
    df = pd.read_csv('../gui/ad.csv')

    df['lcnsLmtNm'] = df['lcnsLmtNm'].apply(lambda x: re.sub(r'/|\b\d{4}\b', '', x))

    group_ex = df.groupby(['bidNtceNo', 'lmtGrpNo'])['lcnsLmtNm'].apply(list).reset_index(name='tlist')
    selec = ['실내건축공사업']
    gr = group_ex[group_ex['tlist'].apply(lambda x: x == selec)]
    print(gr)

def region():
    df = pd.read_csv('../gui/ac.csv')
    group_ex = df.groupby(['bidNtceNo', 'bidNtceOrd'])['prtcptPsblRgnNm'].apply(list).reset_index(name='tlist')
    selec = '인천광역시'
    group_ex['cnt'] = group_ex['tlist'].apply(lambda x: str_count(selec, x))
    print(group_ex)

def str_count(str, st_lst):
    print(str, st_lst)
    count = sum(1 for s in st_lst if str in s)
    if count == len(st_lst):
        return 1
    else: return 0

if __name__ == '__main__':
    region()