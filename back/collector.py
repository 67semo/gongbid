from time import sleep
from traceback import print_tb

import requests, math, re
import bs4
import pandas as pd

def clean_text(bf_str):
    rt_str = re.sub(r'[\n\t\r\[\] ]', '', bf_str)
    rt_str = re.sub(r'\xa0', ',', rt_str)
    rt_str = rt_str.strip()
    return rt_str

def selec_str(str):
    pattern = r'\[[^\[\]]+\]'
    matches = re.findall(pattern, str)
    return matches


def select_samaple(qurl):
    resp = requests.get(qurl, timeout=50)

    body = resp.json()['response']['body']
    print(body['numOfRows'], body['pageNo'], body['totalCount'])
    circle = math.ceil(body['totalCount'] / body['numOfRows'])
    #print(circle)
    nd_dic_lst = body['items']
    nd_col = ['bidNtceNo', 'bidNtceOrd', 'ntceKindNm', 'bidNtceNm', 'bidNtceDtlUrl', 'opengDt']
    df = pd.DataFrame(nd_dic_lst).loc[:, nd_col]
    df.to_csv('abc.csv', index=False)  #첫수집
    return df

def get_detail(qurl):
    print(qurl)
    for _ in range(5):
        try:
            resp = requests.get(qurl, timeout=10)
            if resp.status_code == 200:
                break
        except requests.exceptions.RequestException as e:
            print("An error occurred:", e)
        sleep(2)
    else:
        print("Failed after 3 attempts.")
    chk_bit = resp.json()['response']['body']['totalCount']
    print(chk_bit)
    if chk_bit == 0:
        print('zero')
        return ["zero_items"]
    data = resp.json()['response']['body']['items']

    return data

# g2b의 디테일페이지에서 참가가능 지역과 면허내용을 조회
def crawl_dtl_page(url):
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    searc = soup.findAll('div',{'class':'section'})[3]

    ser_regn = searc.findAll('div',{'class':'tb_inner'})[1].text    # 지역
    ser_ind = searc.findAll('div', {'class':'limitDtl'})[1].text    # 면허

    # 참가 가능 면허 리스트
    ser_indus = selec_str(ser_ind)
    ser_indu_lst = []
    for i in range(len(ser_indus)):
        indls = ser_indus[i].split('과')
        if len(indls) > 1 :
            for j in range(len(indls)):
                ser_indu_lst.append(clean_text(indls[j]))
        else:
            ser_indu_lst.append(clean_text(ser_indus[i]))

    # 참가가능지역 리스트
    permit_rgn = clean_text(ser_regn)
    permit_rgn = permit_rgn.split(',')
    if permit_rgn[-1] == "":                # 끝에 있는 ','로 인하여 리스트가 하나더 추가되어 있으면 꼬리를 자른다.
        permit_rgn = permit_rgn[:-1]

    search_lst = [permit_rgn]
    search_lst.append(ser_indu_lst)

    return search_lst

if __name__ == '__main__':
    url = 'http://apis.data.go.kr/1230000/BidPublicInfoService04/getBidPblancListInfoCnstwkPPSSrch01?serviceKey=HTUHdPFs%2Bqea3owdV7jymHuLsj5S0zQ3SOOzGSzH%2BwGebg3xSXgK2igtN14S2BMYeTMA6spbad3PQ5Ia8ZEtGg%3D%3D&numOfRows=100&inqryDiv=2&bidClseExcpYn=N&intrntnlDivCd=1&type=json&inqryBgnDt=202409210000&inqryEndDt=202410202359&prtcptLmtRgnNm=인천광역시&indstrytyNm=실내건축공사업&presmptPrceBgn=101000000&presmptPrceEnd=151000000'
    df = select_samaple(url)
    print(df)