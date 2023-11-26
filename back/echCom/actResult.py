'''
https://apis.data.go.kr/1230000/ScsbidInfoService/
getOpengResultListInfoOpengCompt?
serviceKey=HTUHdPFs%2Bqea3owdV7jymHuLsj5S0zQ3SOOzGSzH%2BwGebg3xSXgK2igtN14S2BMYeTMA6spbad3PQ5Ia8ZEtGg%3D%3D&
numOfRows=999&
pageNo=1&
bidNtceNo=20231120308&
bidClsfcNo=0&
rbidNo=0&
type=json

https://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoOpengCompt?serviceKey=HTUHdPFs%2Bqea3owdV7jymHuLsj5S0zQ3SOOzGSzH%2BwGebg3xSXgK2igtN14S2BMYeTMA6spbad3PQ5Ia8ZEtGg%3D%3D&
numOfRows=999&
pageNo=1&
bidClsfcNo=20231120308&
rbidNo=0&
type=json
'''

import requests

# url 만들기
def mk_qrUrl(dataDic):
    url = "https://apis.data.go.kr/1230000/ScsbidInfoService/getOpengResultListInfoOpengCompt?"
    for k, v in dataDic.items():
        url = url + k + '=' + str(v) + '&'
    return url[:-1]

def req_dic(bidNo):
    base_dic = {
        'serviceKey': 'HTUHdPFs%2Bqea3owdV7jymHuLsj5S0zQ3SOOzGSzH%2BwGebg3xSXgK2igtN14S2BMYeTMA6spbad3PQ5Ia8ZEtGg%3D%3D',
        'numOfRows': 999,
        'pageNo': 1,
        'bidClsfcNo': 0,
        'rbidNo': 0,
        'type': 'json'
    }
    base_dic['bidNtceNo'] = bidNo
    return base_dic

def collect_data(url):
    data = requests.get(url)
    resp_dt = data.json()['response']['body']['totalCount']
    print(resp_dt)

if __name__ == '__main__':
    rq_dic = req_dic(20231120308)
    a = mk_qrUrl(rq_dic)
    collect_data(a)
