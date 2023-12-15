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

    return qs

def bid_rlt_bs(bidNo):
    # 입찰결과 개요 조회  base url
    '''
    복수예가, 에가별 추첨수, 예정가격
    '''
    url = "https://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoCnstwkPreparPcDetail?"

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
    body = resp.json()['response']['body']
    nd_dic = body['items']
    #print(list(nd_dic.keys()))
    df = pd.DataFrame(nd_dic)
    # 참가자 수를 확인하기위해 추첨횟수의 합계에서 2로 나누웠다.(1개사에 2개씩이므로..)
    partici = pd.to_numeric(df['drwtNum'], errors='coerce').sum() / 2

    msk_lst = ['bidNtceNo', 'plnprc']         # ['bssamt','PrearngPrcePurcnstcst'] 기초금액수집에서 수집
    sr = pd.Series(nd_dic[0]).loc[msk_lst]
    sr['participants_num'] = str(int(partici))

    #sr_exp  = { 'bidNtceNo': '공고번호', 'plnprc': '예정가격', 'bssamt': '기초금액', 'PrearngPrcePurcnstcst': '예정가격순공사비', 'participants_num': '참가업체수'}
    return sr

def result_base(sample_df):
    global indiv_vot
    rate = 0.87745
    rt_lst = []
    ech_lst=[]
    for item in sample_df.itertuples():
        qur = bid_rlt_bs(item.bidNtceNo)
        #print(qur)
        bid_rlt_serz = read_bid_result_bs(qur)
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
    df1 = result_base(ruf_df)
    #df = pd.merge([ruf_df, df1], on='bidNtceNo')
    df = pd.merge(left=ruf_df, right=df1, on='bidNtceNo')
    #print(df)
    return df

if __name__ == '__main__':
    pd.set_option('display.max_columns', 15)
    pd.set_option('display.max_colwidth', 30)
    pd.set_option('display.unicode.east_asian_width', True)

    df = pd.read_csv('../gui/abc.csv')
    df1 , ech_df = result_base(df)
    df = pd.concat([df, df1], axis=1)
    df.drop(columns=['bidNtceNo'], inplace=True)
    df.to_csv('abd.csv')
    ech_df.to_csv('abc.csv')
    print(df.dtypes)


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

