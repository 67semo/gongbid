# Gui로부터 호출되어 조건에 맞는 입찰을 정리 추출하여 리턴
#from itertools import groupby
#from lib2to3.pgen2.tokenize import group

import pandas as pd
#from pyparsing import Empty

#from Scripts.jsonpointer import ptr_group

from back import collector, filter

from back import config, parameter
#from back import filter_region_Indust as flt
from back import bid_result3 as br

def mk_qrUrl(dataDic, serv):    # 나라장터 검색(맨처음자료)
    url = "http://apis.data.go.kr/1230000/BidPublicInfoService05/" + parameter.desc[serv][0] + '?'
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


def serchRBid(reqDic, vala, Ncost):
    # require_dic 작성
    bsDic = {
        'serviceKey': config.encoding,
        'numOfRows': 100,
        'inqryDiv': 2,              # 개찰일기준
        'bidClseExcpYn': 'N',
        'intrntnlDivCd': 1,
        'type': 'json'
    }
    bsDic.update(reqDic)

    # require_dic 을 기초로 url을 만들고 나라장터조회로 가져온 데이터중 변경 또는 취소된 비드를 제거한다.
    reqUrl = mk_qrUrl(bsDic, 'naraCon')
    ruf_bid_df = collector.select_samaple(reqUrl)
    # first filltering for effective bid(excepte changed ver, cahceled)
    ruf_bid_df = ruf_bid_df.drop_duplicates(['bidNtceNo'], keep='last')     # last 동일한 공고번호중 마지막 ver만 남기고 버린다.
    ruf_bid_df = ruf_bid_df[ruf_bid_df['ntceKindNm'] != "취소"]

    # 기초금액, valuA, 순공사원가 등 필요한 자료들 가져오고 데이터 프레임을 정리한다.
    base_amount = []
    for item in ruf_bid_df.itertuples():
        aa = mk_dic_bAmt(item.bidNtceNo)                # 각종가격조회 url생성
        rt_data = collector.get_detail(aa)[0]

        if rt_data != "zero_items":
            rt_data['opengDt'] = item.opengDt
            rt_data['bidNtceDtlUrl'] = item.bidNtceDtlUrl
            base_amount.append(rt_data)    # 기초금액, 예가변동폭, 순공사원가, A값등의 정보를 추가

    df = pd.DataFrame(base_amount)

    # 복수예비가 3% 이외의 것은 제외
    width = df.query('rsrvtnPrceRngBgnRate == "-3" and rsrvtnPrceRngEndRate == "+3"')
    width.to_csv('fltWidth.csv')

    # A값에 대한 정리
    orgn = parameter.read_defintn('공사기초금액')
    except_a = parameter.read_defintn('A값', '세부')

    if vala:
        df1 = width[width['bidPrceCalclAYn'] == 'Y']
        df1['sumA'] = df1[except_a].astype(int).sum(axis=1)
    else:
        df1 = width[width['bidPrceCalclAYn'] == 'N']

    except_a = except_a + ['bidPrceCalclAYn', 'qltyMngcstAObjYn', 'envCnsrvcst', 'scontrctPayprcePayGrntyFee']  # 필요없는 항목들의 리스트
    df1.drop(except_a, axis=1, inplace=True)

    # filltering for net-cost
    if Ncost == True:
        df1 = df1[df1['bssAmtPurcnstcst'] != '']
    else:
        df1 = df1[df1['bssAmtPurcnstcst'] == '']
    df1.to_csv('effect_df.csv')  # 1차 필터링을 한 데이터프레임을 확인하기위한 화일

    return df1

    # 지역 및 면허
def fillter_rDf(roughDf, area, licenLt):
    print(roughDf, area, licenLt)

    #licenLt = [item for item in licenLt if item not in [None, "", " "]]

    prmit_rgn = []
    prmit_lsn = []
    for item in roughDf.itertuples():
        rgn_url = mk_dic_region(item.bidNtceNo, item.bidNtceOrd)  # 참가지역조회 url생성
        lsn_url = mk_dic_licen(item.bidNtceNo, item.bidNtceOrd)
        print(f"lincense : {lsn_url}")
        prmit_rgn = prmit_rgn + collector.get_detail(rgn_url)
        prmit_lsn = prmit_lsn + collector.get_detail(lsn_url)

    permit_area_df = pd.DataFrame(prmit_rgn)
    permit_area_df.to_csv('permitArea.csv')
    groupedArea_bidDf = permit_area_df.groupby(['bidNtceNo', 'bidNtceOrd'])['prtcptPsblRgnNm'].apply(list).reset_index(name='permitArea')
    #print(groupedArea_bidDf)
    area_mask = groupedArea_bidDf[groupedArea_bidDf['permitArea'].apply(lambda x: str_count(area, x))]
    flt_area_roughDf = roughDf[roughDf['bidNtceNo'].isin(area_mask['bidNtceNo'])]
    flt_area_df = pd.merge(flt_area_roughDf, area_mask, on=['bidNtceNo', 'bidNtceOrd'])
    flt_area_df.to_csv('flt_area_df.csv')

    permit_licen_df = pd.DataFrame(prmit_lsn)
    permit_licen_df['lcnsLmtNm'] = permit_licen_df['lcnsLmtNm'].apply(lambda x: replace_with_reference(x, licenLt))
    permit_licen_df.to_csv('permitLisn.csv')
    licen_tempGroup = permit_licen_df.groupby(['bidNtceNo', 'bidNtceOrd'])['lcnsLmtNm'].apply(list).reset_index(name='permitLicen')

    licen_tempGroup.to_csv("flt_licen_dfp.csv")
    print(licenLt)
    licen_tempGroup = licen_tempGroup[licen_tempGroup['permitLicen'].apply(lambda x: set(x) == set(licenLt))]

    licen_tempGroup.to_csv('flt_licen_df.csv')
    final_effec_bid = pd.merge(flt_area_df, licen_tempGroup, on=['bidNtceNo', 'bidNtceOrd'])
    print(final_effec_bid)

    return final_effec_bid

def replace_with_reference(value, referenceLst):
    for ref in referenceLst:
        if value.startswith(ref):
            return ref
    return value

def str_count(str, st_lst):
    count = sum(1 for s in st_lst if str in s)
    #print(str, st_lst)
    if count == len(st_lst):
        return True
    else: return False


# 메인호출 시작포인트
def bidsData(require_dic, addl_dic):
    import time
    st_time = time.time()

    BValA = addl_dic['valA']
    BNcost = addl_dic['sun_wanga']
    print(BNcost)

    ruf_df = serchRBid(require_dic, BValA, BNcost)    # 초기정보 형성과 A값, 순공사원가 검토
    if ruf_df.empty:
        return pd.DataFrame()
    licenLst = sorted(addl_dic['industry'])
    print(f"sezrched bid : \n {type(ruf_df)}")
    effective_df = fillter_rDf(ruf_df, require_dic['prtcptLmtRgnNm'], licenLst)

    #chkA_df = "Nothing"
    tm1 = time.time()
    print(f"{tm1 - st_time: .5f} sec")
    effective_df.to_csv('final_bidsinfo.csv', index=False)
    # 빈데이터 프레임인 경우 빈 데이터 프레임을 리턴
    if effective_df.empty:
        resp_df = pd.DataFrame()
    else:
        resp_df = br.result_manager(effective_df)
    resp_df.to_csv("freturn_df.csv")
    return resp_df

'''    thound_div_col = ['bssamt', 'bssAmtPurcnstcst', 'sumA', 'plnprc']
    for col in thound_div_col:
        print(col)
        resp_df[col] = resp_df[col].apply(add_commas)'''




def add_commas(num):
    return f'{num:,}'






if __name__ == '__main__':
    req_dic = {'inqryBgnDt': '202409140000',
               'inqryEndDt': '202412022359',
               'prtcptLmtRgnNm': '인천광역시',
               'indstrytyNm': '전문소방시설공사업',
               'presmptPrceBgn': '10000000',
               'presmptPrceEnd': '60000000'}
    add_dic = {'industry': ['전문소방시설공사업', '일반소방시설공사업(전기)'],
               'valA': True,
               'sun_wanga': False}


    df = bidsData(req_dic, add_dic)
    if df.empty:
        print("no data")
    else: df.to_csv('abc.csv')

    '''
    http://apis.data.go.kr/1230000/BidPublicInfoService05/getBidPblancListInfoCnstwkPPSSrch02?serviceKey=HTUHdPFs%2Bqea3owdV7jymHuLsj5S0zQ3SOOzGSzH%2BwGebg3xSXgK2igtN14S2BMYeTMA6spbad3PQ5Ia8ZEtGg%3D%3D&numOfRows=100&inqryDiv=2&bidClseExcpYn=N&intrntnlDivCd=1&type=json&inqryBgnDt=202410270000&inqryEndDt=202411252359&prtcptLmtRgnNm=인천광역시&indstrytyNm=기계설비,가스공사업&presmptPrceBgn=129000000&presmptPrceEnd=194000000
    # url을 주고 입찰개요 데이터 프레임를 얻는다.
    url = 'http://apis.data.go.kr/1230000/BidPublicInfoService04/getBidPblancListInfoCnstwkPPSSrch01?serviceKey=HTUHdPFs%2Bqea3owdV7jymHuLsj5S0zQ3SOOzGSzH%2BwGebg3xSXgK2igtN14S2BMYeTMA6spbad3PQ5Ia8ZEtGg%3D%3D&numOfRows=100&inqryDiv=2&bidClseExcpYn=N&intrntnlDivCd=1&type=json&inqryBgnDt=202409210000&inqryEndDt=202410202359&prtcptLmtRgnNm=인천광역시&indstrytyNm=실내건축공사업&presmptPrceBgn=101000000&presmptPrceEnd=151000000'
    result = collector.select_samaple(url)
    print(result)
    '''


    # print((add_commas(12344645656)))

    # finalDf = filter.filtering_bid(selected_bid_info, rgn, ind, valA)   # 필터링(지역, 면허)

    # finalDf = finalDf.drop(['bidNtceDtlUrl', 'rgn_mk'], axis=1)     # 필요 항목만 정리
    # bid_result.result_base(finalDf)             # 개찰결과
    # return finalDf, selected_bid_info