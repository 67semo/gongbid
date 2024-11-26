import pandas as pd
import matplotlib.pyplot as plt

def pivo(lts_df):
    istb_df = lts_df.pivot(index='prcbdrBizno', columns='bidNtceNo', values='ejacul_rate')
    #istb_df.to_csv('distb_df.csv')
    #print(istb_df)
    return istb_df

# 등분 구간 나누고 카운트 하여 return Serize
def divsCnt(sr):
    mi = 0.975
    ma = 1.025
    offs = (ma - mi) / 200
    div = []
    for i in range(201):
        div.append(mi + offs * i)
    #print(len(div), div, div[200])
    rDistrib = pd.cut(sr, bins=div).value_counts().sort_index()
    #print(rDistrib, sr)
    return rDistrib

def showgrahp(df):

    fig, ax = plt.subplots(figsize=(20, 4))

    ax.plot(range(200), df['thrd_pt'], label= 'bid_record')
    ax.plot(range(200), df['normal'], label='normal')
    ax.plot(range(200), df['yield'], label='thru point')
    ax.grid(True)
    ax.legend()
    plt.xticks(range(0, 200, 5))
    plt.show()

def diffu(v, p):
    const_lt = [0.187012987, 0.233766234, 0.311688312, 0.467532468]
    delta_lt = [0.007792208, 0.004770739, 0.004212004, 0.00472255]
    rlt = []

    def calcul(d, c=1):
        for i in range(4):
            l = (const_lt[i] - delta_lt[i] * d) * v
            if l <= 0:
                l = 0
            rlt.append(l)
        k = sum(const_lt) * v - sum(rlt)
        m = sum(const_lt)
        rlt.append(v)
        for i in [3, 2, 1, 0]:
            l = const_lt[i] * (v + k / m )
            rlt.append(l)
        if c == 0:
            rlt.reverse()
        #print(rlt, p)
        return rlt

    if p <= 100:
        d = 100 - p
        calt = calcul(d)
    else:
        d = p - 101
        calt = calcul(d, 0)
    return calt

def collection(df):
    # 보정작업
    th_li = [[0 for _ in range(200)] for _ in range(200)]
    # print(f"빈바닥 : {th_li}")

    for d, e in enumerate(df):
        a = 0
        if e != 0:
            a = diffu(e, d)
            if d < 4:
                th_li[d][:d + 5] = a[4 - d:]
            elif d > 145:
                th_li[d][d - 4:] = a[:200 - d]
            else:
                th_li[d][d - 4:d + 5] = a

    th_df = pd.DataFrame(th_li)
    th_df.to_csv('aca.csv')

    dh_Sr = th_df.sum(axis=0)
    return dh_Sr

if __name__ == '__main__':
    df = pd.read_csv('../gui/acb.csv')
    sizs = pivo(df)
    sizs.to_csv('abf.csv')
    print(sizs.describe())
    point_lst = []
    for sr in sizs.itertuples():
        a = divsCnt(sr)
        point_lst.append(a)

    po_df = pd.concat(point_lst, axis=1)
    po_df.to_csv('abe.csv')
    sum_df = po_df.sum(axis=1)
    #print(sum_df)
    #showgrahp(sum_df)

    dh_Sr = collection(sum_df)

    # 보정계수 맨나중의 값(1)은 임의 의 조정겂으로 앞으로도 많은 연구가 필요함
    corrt =  sum(dh_Sr) / sizs.count().mean()

    #print(sizs.count().mean())
    corrected_sum = [x + corrt for x in dh_Sr]
    nor_df = pd.read_csv('aaa.csv')         # 에정가격 포인트
    nor_sr = divsCnt(nor_df['saYld'])
    nor_sr1 = [x * sum(corrected_sum)/sum(nor_sr) for x in nor_sr]

    #print(nor_sr1)
    ans_dic = {'thrd_pt': corrected_sum, 'normal': nor_sr1}
    ans_df = pd.DataFrame(ans_dic)
    ans_df['yield'] = ans_df['normal']/ans_df['thrd_pt']
    mn = ans_df['normal'].max() / ans_df['yield'].max()
    ans_df['yield'] = ans_df['yield'] * mn
    ans_df.to_csv('aab.csv')
    showgrahp(ans_df)











    '''
    df = pd.read_csv('abc.csv')
    pivo(df)
    siz = sizs.loc[1228197987, :]
    ditrib = divsCnt(siz)
    print(type(ditrib))
    showgrahp(ditrib)
    '''