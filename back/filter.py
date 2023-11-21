
import re

def filtering_bid(df, region, indust):
    print(region, indust)
    # 취소상태에 있는 bid 와 관련 공고 제거
    msk = list(df[df.ntceKindNm=="취소"].bidNtceNo)

    ftd1 = df[df.bidNtceNo.isin(msk) == False]

    # 지격제한 필터링
    rgn_mk = []
    for a in ftd1.permit_regn:
        b = a[0]
        c = re.sub(r'[\[\]\'\s]', '', b)
        #c = b.split(',')

        if c == region and len(a) == 1:
            rgn_mk.append(1)
        else:
            rgn_mk.append(0)

    ftd1['rgn_mk'] = rgn_mk
    ftd2 = ftd1[ftd1['rgn_mk'] == 1]
    print('취소와 지역 정리 남은 것',ftd2)

    # 면허제한 필터링
    msk = []

    for a in ftd2.permit_indu:
        a1 = a[0]
        b = re.sub(r'[\[\]\'(\(0-9{4}\)]', '', a1)
        print(b, len(a))
        if indust == '실내건축':
            if indust in b and len(a) == 1:
                msk.append(1)
            else:
                msk.append(0)

        if indust == '기계설비':
            if (b == '기계설비,가스공사업' or b == '기계설비,가스공사업주력분야:기계설비공사') and len(a) == 1:
                msk.append(1)
            else:
                msk.append(0)

    ftd2['rgn_mk'] = msk
    ftd2.to_csv('rt1.csv', index=False)
    ret_df = ftd2[ftd2.rgn_mk == 1]
    ret_df.to_csv('rt.csv', index=False)
    return ret_df