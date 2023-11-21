# Gui로부터 호출되어 조건에 맞는 입찰을 정리 추출하여 리턴
from back import collector, filter
from . import config, bid_result

def mk_qrUrl(dataDic):
    url = "https://apis.data.go.kr/1230000/BidPublicInfoService04/getBidPblancListInfoCnstwkPPSSrch01?"
    for k, v in dataDic.items():
        url = url + k + '=' + str(v) + '&'
    return url[:-1]

def serchRBid(reqDic):
    bsDic = {
        'serviceKey': config.gonggongky,
        'numOfRows': 100,
        'inqryDiv': 2,
        'bidClseExcpYn': 'N',
        'intrntnlDivCd': 1,
        'type': 'json'
    }
    bsDic.update(reqDic)
    reqUrl = mk_qrUrl(bsDic)

    ruf_bid_df = collector.select_samaple(reqUrl)
    ruf_bid_df = ruf_bid_df.drop_duplicates(['bidNtceNo'], keep='last')

    # 상세입찰 페이지에서 지역과 면허에 대한 제한정보를 담을 빈 리스트
    pm_rgnLst = []
    pm_indLst = []

    for item in ruf_bid_df.itertuples():
        # 입찰상세페이지(bidNtceDtlUrl)로부터 면허와 지역정보를 가져옴
        a = collector.crawl_dtl_page(item.bidNtceDtlUrl)
        pm_rgnLst.append(a[0])
        pm_indLst.append(a[1])

    ruf_bid_df['permit_regn'] = pm_rgnLst
    ruf_bid_df['permit_indu'] = pm_indLst

    global rgn
    global ind
    rgn = bsDic['prtcptLmtRgnNm']
    ind = bsDic['indstrytyNm']

    return ruf_bid_df



def bidsData(require_dic, valA):
    selected_bid_info = serchRBid(require_dic)      # 해당입찰 검색
    finalDf = filter.filtering_bid(selected_bid_info, rgn, ind)   # 필터링(지역, 면허)
    finalDf = finalDf.drop(['bidNtceDtlUrl', 'rgn_mk'], axis=1)     # 필요 항목만 정리
    bid_result.result_base(finalDf)             # 개찰결과 개
    #return finalDf, selected_bid_info