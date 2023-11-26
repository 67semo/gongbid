# Gui로부터 호출되어 조건에 맞는 입찰을 정리 추출하여 리턴
import pandas as pd

from back import collector, filter
from . import config, bid_result

def mk_qrUrl(dataDic, serv):    # 나라장터 검색(맨처음자료)
    url = "https://apis.data.go.kr/1230000/BidPublicInfoService04/" + config.desc[serv][0] + '?'
    for k, v in dataDic.items():
        url = url + k + '=' + str(v) + '&'
    return url[:-1]

def sub_data(desc):
    return config.read_defintn(desc)

def mk_dic_bAmt(no):        # 공사기초금액조회 url생성
    bsDic = {
        'serviceKey': config.encoding,
        'numOfRows': 10,
        'inqryDiv': 2,
        'bidNtceNo': no,
        'type': 'json'
    }
    url = mk_qrUrl(bsDic, 'gongAmtCon')
    return url

def serchRBid(reqDic, vala):
    bsDic = {
        'serviceKey': config.encoding,
        'numOfRows': 100,
        'inqryDiv': 2,
        'bidClseExcpYn': 'N',
        'intrntnlDivCd': 1,
        'type': 'json'
    }
    bsDic.update(reqDic)
    reqUrl = mk_qrUrl(bsDic, 'naraCon')
    #print(reqUrl)
    ruf_bid_df = collector.select_samaple(reqUrl)
    ruf_bid_df = ruf_bid_df.drop_duplicates(['bidNtceNo'], keep='last')     # last 동일한 공고번호중 마지막 ver만 남기고 버린다.
    ruf_bid_df = ruf_bid_df[ruf_bid_df['ntceKindNm'] != "취소"]

    # 기초금액, valuA, 순공사원가
    base_amount = []
    for item in ruf_bid_df.itertuples():
        #print(item.bidNtceNo, item.bidNtceOrd)
        aa = mk_dic_bAmt(item.bidNtceNo)                # 기초금액조회 url생성
        base_amount.append(collector.get_detail(aa))    # 기초금액, 예가변동폭, 순공사원가, A값등의 정보를 가져공

    df = pd.DataFrame(base_amount)
    width = df.query('rsrvtnPrceRngBgnRate == "-3" and rsrvtnPrceRngEndRate == "+3"')



    # 항목정리
    orgn = config.read_defintn('공사기초금액')
    except_a = config.read_defintn('A값', '세부')
    print(orgn, except_a)
    if vala:
        df1 = width[width['bidPrceCalclAYn'] == 'Y'][orgn]
        df1['sumA'] = df1[except_a].astype(int).sum()
    else:
        df1 = width[width['bidPrceCalclAYn'] == 'N'][[x for x in orgn if x not in except_a]]


    #return df1
    print(df1)
    df1.to_csv('ab.csv')



def bidsData(require_dic, valA):
    chkA_df = serchRBid(require_dic, valA)    # 초기정보 형성과 A값 검토
    #for item in chkA_df.itertuples:



    #selected_bid_info = serchRBid(require_dic)      # 해당입찰 검색
    #finalDf = filter.filtering_bid(selected_bid_info, rgn, ind, valA)   # 필터링(지역, 면허)

    #finalDf = finalDf.drop(['bidNtceDtlUrl', 'rgn_mk'], axis=1)     # 필요 항목만 정리
    #bid_result.result_base(finalDf)             # 개찰결과 개
    #return finalDf, selected_bid_info