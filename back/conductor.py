# Gui로부터 호출되어 조건에 맞는 입찰을 정리 추출하여 리턴
import pandas as pd

from back import collector, filter
from . import config, parameter, bid_result
from . import filter_region_Indust as flt
from . import bid_result1 as br

def mk_qrUrl(dataDic, serv):    # 나라장터 검색(맨처음자료)
    url = "https://apis.data.go.kr/1230000/BidPublicInfoService04/" + parameter.desc[serv][0] + '?'
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

def mk_dic_region(no, ord):        # 공사기초금액조회 url생성
    bsDic = {
        'serviceKey': config.encoding,
        'numOfRows': 10,
        'inqryDiv': 2,
        'bidNtceNo': no,
        'bidNtceOrd': ord,
        'type': 'json'
    }
    url = mk_qrUrl(bsDic, 'region')
    return url

def mk_dic_licen(no, ord):        # 며허조회 url생성
    bsDic = {
        'serviceKey': config.encoding,
        'numOfRows': 10,
        'inqryDiv': 2,
        'bidNtceNo': no,
        'bidNtceOrd': ord,
        'type': 'json'
    }
    url = mk_qrUrl(bsDic, 'license')
    return url


def serchRBid(reqDic, vala):
    # require_dic 작성
    bsDic = {
        'serviceKey': config.encoding,
        'numOfRows': 100,
        'inqryDiv': 2,
        'bidClseExcpYn': 'N',
        'intrntnlDivCd': 1,
        'type': 'json'
    }
    bsDic.update(reqDic)
    # require_dic 을 기초로 url을 만들고 나라장터조회로 가져온 데이터중 변경 또는 취소된 비드를 제거한다.
    reqUrl = mk_qrUrl(bsDic, 'naraCon')
    print(reqUrl)
    ruf_bid_df = collector.select_samaple(reqUrl)
    ruf_bid_df = ruf_bid_df.drop_duplicates(['bidNtceNo'], keep='last')     # last 동일한 공고번호중 마지막 ver만 남기고 버린다.
    ruf_bid_df = ruf_bid_df[ruf_bid_df['ntceKindNm'] != "취소"]

    # 기초금액, valuA, 순공사원가 등 필요한 자료들 가져고고 데이터 프레임을 정리한다.
    base_amount = []
    for item in ruf_bid_df.itertuples():
        aa = mk_dic_bAmt(item.bidNtceNo)                # 기초금액조회 url생성
        rt_data = collector.get_detail(aa)[0]
        if rt_data != "zero_items":
            base_amount.append(rt_data)    # 기초금액, 예가변동폭, 순공사원가, A값등의 정보를 가져공

    df = pd.DataFrame(base_amount)
    width = df.query('rsrvtnPrceRngBgnRate == "-3" and rsrvtnPrceRngEndRate == "+3"')

    # A값에 대한 정리
    orgn = parameter.read_defintn('공사기초금액')
    except_a = parameter.read_defintn('A값', '세부')

    if vala:
        df1 = width[width['bidPrceCalclAYn'] == 'Y'][orgn]
        df1['sumA'] = df1[except_a].astype(int).sum(axis=1)
    else:
        df1 = width[width['bidPrceCalclAYn'] == 'N'][orgn]

    except_a = except_a + ['bidPrceCalclAYn', 'qltyMngcstAObjYn', 'envCnsrvcst', 'scontrctPayprcePayGrntyFee']  # 필요없는 항목들의 리스트
    df1.drop(except_a, axis=1, inplace=True)
    #df1.to_csv('ab.csv')           # 1차 필터링을 한 데이터프레임을 확인하기위한 화일

    # 지역 및 면허
    prmit_rgn = []
    prmit_lsn = []
    for item in df1.itertuples():
        rgn_url = mk_dic_region(item.bidNtceNo, item.bidNtceOrd)                # 참가지역조회 url생성
        lsn_url = mk_dic_licen(item.bidNtceNo, item.bidNtceOrd)
        prmit_rgn = prmit_rgn + collector.get_detail(rgn_url)
        prmit_lsn = prmit_lsn + collector.get_detail(lsn_url)

    df2 = pd.DataFrame(prmit_rgn)
    df2 = df2[df2['prtcptPsblRgnNm'].str.contains(reqDic['prtcptLmtRgnNm'])]
    df2 = flt.region(df2, reqDic['prtcptLmtRgnNm'])
    df2.to_csv('ac.csv')

    df3 = pd.DataFrame(prmit_lsn)
    df3 = flt.license(df3, [reqDic['indstrytyNm']])
    df3.to_csv('ad1.csv')

    result_sr = pd.merge(df2['bidNtceNo'], df3['bidNtceNo'])
    df1.reset_index()
    rslt_df = df1[df1['bidNtceNo'].isin(result_sr['bidNtceNo'])]
    return rslt_df

def bidsData(require_dic, valA):
    import time
    st_time = time.time()
    #print(require_dic)
    reg = [require_dic['prtcptLmtRgnNm']]
    ind = [require_dic['indstrytyNm']]
    #print(reg, ind)

    chkA_df = serchRBid(require_dic, valA)    # 초기정보 형성과 A값 검토
    tm1 = time.time()
    print(f"{tm1 - st_time: .5f} sec")
    chkA_df.to_csv('abc.csv', index=False)
    #print(chkA_df)
    resp_df = br.result_manager(chkA_df)
    return resp_df

'''    thound_div_col = ['bssamt', 'bssAmtPurcnstcst', 'sumA', 'plnprc']
    for col in thound_div_col:
        print(col)
        resp_df[col] = resp_df[col].apply(add_commas)'''




def add_commas(num):
    return f'{num:,}'




    #selected_bid_info = serchRBid(require_dic)      # 해당입찰 검색
    #finalDf = filter.filtering_bid(selected_bid_info, rgn, ind, valA)   # 필터링(지역, 면허)

    #finalDf = finalDf.drop(['bidNtceDtlUrl', 'rgn_mk'], axis=1)     # 필요 항목만 정리
    #bid_result.result_base(finalDf)             # 개찰결과 개
    #return finalDf, selected_bid_info