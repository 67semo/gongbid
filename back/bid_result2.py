# 상품해석을 위한 것으로 추정
from urllib.parse import urlencode
import pandas as pd
import requests
from back import config

global indiv_vot

def bid_rlt_ech(bidNo):
    # 개별투찰포인트조회
    url = "https://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoOpengCompt?"
    params = {
        "numOfRows" : 900,
        "pageNo" : 1,
        "ServiceKey" : config.encoding,
        "type" : "json",
        "bidNtceNo" : bidNo
    }
    qs = url + urlencode(params)
    qs = qs.replace('%25', '%')
    print(qs)
    return qs

def bid_rlt_bs(bidNo):
    # 입찰결과 개요 조회  base url
    '''
    복수예가, 에가별 추첨수, 예정가격
    '''
    url = "https://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoThngPreparPcDetail?"

    params = {
        "numOfRows" : 15,
        "pageNo" : 1,
        "ServiceKey" : config.decoding,
        "type" : "json",
        "inqryDiv" : 2,
        "bidNtceNo" : bidNo
    }

    qs = url + urlencode(params, safe='%')

    return qs

def read_bid_result_ech(qurl):
    resp = requests.get(qurl)
    body = resp.json()['response']['body']
    nd_dic = body['items']
    #print(list(nd_dic.keys()))
    df = pd.DataFrame(nd_dic).loc[:, ['bidNtceNo', 'prcbdrBizno', 'bidprcAmt']]
    return df

def read_bid_result_bs(qurl):
    resp = requests.get(qurl)
    msk_lst = ['bidNtceNo', 'plnprc']  # ['bssamt','PrearngPrcePurcnstcst'] 기초금액수집에서 수집
    body = resp.json()['response']['body']
    if body['totalCount'] == 0:
        errdic = {
            'bidNtceNo': 999,
            'plnprc': 0,
            'participants_num': 0
        }
        return pd.Series(errdic)
    nd_dic = body['items']
    #print(list(nd_dic.keys()))
    df = pd.DataFrame(nd_dic)
    # 참가자 수를 확인하기위해 추첨횟수의 합계에서 2로 나누웠다.(1개사에 2개씩이므로..)
    partici = pd.to_numeric(df['drwtNum'], errors='coerce').sum() / 2

    sr = pd.Series(nd_dic[0]).loc[msk_lst]
    sr['participants_num'] = str(int(partici))

    #sr_exp  = { 'bidNtceNo': '공고번호', 'plnprc': '예정가격', 'bssamt': '기초금액', 'PrearngPrcePurcnstcst': '예정가격순공사비', 'participants_num': '참가업체수'}
    return sr

def result_base(sample_df):
    global indiv_vot
    rate = 0.84245
    rt_lst = []
    ech_lst=[]
    for item in sample_df.itertuples():
        qur = bid_rlt_bs(item.bidNtceNo)
        print(qur)
        bid_rlt_serz = read_bid_result_bs(qur)
        if bid_rlt_serz['bidNtceNo'] == 999:
            continue
        print(bid_rlt_serz)
        rt_lst.append(bid_rlt_serz)

        qur1 = bid_rlt_ech(item.bidNtceNo)
        #print(qur1)
        thru_df = read_bid_result_ech(qur1)
        #print(thru_df)
        thru_df['bidprcAmt'] = pd.to_numeric(thru_df['bidprcAmt'], errors='coerce')
        thru_df = thru_df.dropna()
        thru_df['ejacul_rate']= (thru_df['bidprcAmt'].astype(int) - item.sumA * (1 - rate)) / (int(item.bssamt) * rate)
        ech_lst.append(thru_df)

    rt_df = pd.DataFrame(rt_lst)
    indiv_vot = pd.concat(ech_lst)
    indiv_vot.to_csv('acb.csv')
    return rt_df

def result_manager(ruf_df):
    df = result_base(ruf_df)
    #df = pd.merge([ruf_df, df1], on='bidNtceNo')
    #df = pd.merge(left=ruf_df, right=df1, on='bidNtceNo')
    print(df)
    return df

if __name__ == '__main__':
    #a = bid_rlt_ech(20230826044)
    dt = {
        'bidNtceNo':[20230826044, 20231206720],
        'bssamt': [113542000, 209638000],
        'sumA': [0, 0]
    }
    df01 = pd.DataFrame.from_dict(dt)
    print(df01)
    result_manager(df01).to_csv('result2.csv')

    '''
    df = pd.read_csv('../gui/abc.csv')
    df1 = result_base(df)
    df = pd.concat([df, df1], axis=1)
    df.to_csv('abd.csv', )
    print(df)
    
    for item in df.itertuples():
    qur = bid_rlt_ech(item.bidNtceNo)
    print(qur)

    '''

