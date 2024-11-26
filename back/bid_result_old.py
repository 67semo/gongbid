from urllib.parse import urlencode
import pandas as pd
import requests
from back import config

def bid_rlt_bs(bidNo):
    # 입찰결과 개요 조회  base url
    url = "https://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoCnstwkPreparPcDetail?"

    params = {
        #"numOfRows" : 15,
        "pageNo" : 1,
        "ServiceKey" : config.decoding,
        "type" : "json",
        "inqryDiv" : 2,
        "bidNtceNo" : bidNo
    }

    qs = url + urlencode(params, safe='%')

    return qs

def read_bid_result_bs(qurl):
    resp = requests.get(qurl)
    body = resp.json()['response']['body']
    nd_dic = body['items']
    #print(list(nd_dic.keys()))
    df = pd.DataFrame(nd_dic)
    # 참가자 수를 확인하기위해 추첨횟수의 합계에서 2로 나누웠다.(1개사에 2개씩이므로..)
    partici = pd.to_numeric(df['drwtNum'], errors='coerce').sum() / 2

    msk_lst = ['bidNtceNo', 'plnprc', 'bssamt', 'PrearngPrcePurcnstcst']
    sr = pd.Series(nd_dic[0]).loc[msk_lst]
    sr['participants_num'] = partici

    #sr_exp  = { 'bidNtceNo': '공고번호', 'plnprc': '예정가격', 'bssamt': '기초금액', 'PrearngPrcePurcnstcst': '예정가격순공사비', 'participants_num': '참가업체수'}
    return sr

def result_base(sample_df):
    for item in sample_df.itertuples():
        qur = bid_rlt_bs(item.bidNtceNo)
        bid_rlt_serz = read_bid_result_bs(qur)
        #print(bid_rlt_serz)

if __name__ == '__main__':
    '''
    df = pd.read_csv('../gui/abc.csv', index_col=None)
    print(df)
    '''
    a = bid_rlt_bs(20230826044)
    print(a)
