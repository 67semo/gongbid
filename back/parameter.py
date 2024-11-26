import pandas as pd
import os

# 공공데이터포털 parameter
desc = {
    'license': ['getBidPblancListInfoLicenseLimit02', '참가제한면허'],
    'region': ['getBidPblancListInfoPrtcptPsblRgn02', '참가제한지역'],
    'valuea': ['getBidPblancListBidPrceCalclAInfo02', 'A값'],
    'naraCon': ['getBidPblancListInfoCnstwkPPSSrch02', '나라장터검색조건에 의한 입찰공고공사조회'],
    'naraThg': ['getBidPblancListInfoThngPPSSrch02', '나라장터검색조건에 의한 입찰공고물품조회'],
    'gongCon': ['getBidPblancListInfoCnstwk02', '입찰공고목록 정보에 대한 공사조회'],
    'gongSer': ['getBidPblancListInfoServc02', '입찰공고목록 정보에 대한 용역조회'],
    'gongThg': ['getBidPblancListInfoThng02', '입찰공고목록 정보에 대한 물품조회'],
    'gongAmtThg': ['getBidPblancListInfoThngBsisAmount02', '입찰공고목록 정보에 대한 물품기초금액조회'],
    'gongAmtCon': ['getBidPblancListInfoCnstwkBsisAmount02', '입찰공고목록 정보에 대한 공사기초금액조회'],
    'gongAmtSer': ['getBidPblancListInfoCnstwkBsisAmount02', '입찰공고목록 정보에 대한 용역기초금액조회']
}

def read_defintn(desc, ds='구분'):
    file = "D:\\Python3\\gongbid\\back\\gonggo.csv"
    #file = '/home/kohenil/project/python/bid2/back/gonggo.csv'
    df = pd.read_csv(file)
    return list(df[df[ds] == desc]['코드'])

if __name__ == '__main__':
    a = read_defintn('A값')    # 공사기초금액, 지역, 면허
    print(a)