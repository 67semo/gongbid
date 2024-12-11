import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def cal_thru(sr):
    threshold = sr.quantile(0.95)  # 상위 5% 임계값 계산
    top_5_percent_intervals = sr[sr >= threshold].index  # 상위 5% 구간 추출

    random_interval = np.random.choice(top_5_percent_intervals)  # 상위 구간 중 하나를 무작위 선택
    interval_list = [float(x) for x in random_interval.strip('()[]').split(',')]
    random_point = random_point_from_interval(interval_list)  # 선택된 구간 내에서 무작위 포인트 생성
    return random_point

# Step 3: 상위 5% 구간에서 무작위로 포인트 선택
def random_point_from_interval(interval):

    return np.random.uniform(interval[0], interval[1])  # 구간 내 임의의 포인트


if __name__ == '__main__':
    yld_sr = pd.read_csv('yield.csv', index_col='Unnamed: 0')['yield']
    point = cal_thru(yld_sr)
    print(point)
