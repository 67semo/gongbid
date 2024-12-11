import pandas as pd
import numpy as np

# Step 1: 확률 분포 시리즈 정의 (예제 데이터)
index = pd.IntervalIndex.from_tuples([(0.975 + i * (1.025 - 0.975) / 200, 0.975 + (i + 1) * (1.025 - 0.975) / 200) for i in range(200)])
probabilities = np.random.rand(200)  # 확률 분포값 예제 (랜덤 값)
probabilities = probabilities / probabilities.sum()  # 확률 정규화
prob_series = pd.Series(probabilities, index=index)

# Step 2: 상위 5% 확률값 기준 구간 추출
threshold = prob_series.quantile(0.95)  # 상위 5% 임계값 계산
top_5_percent_intervals = prob_series[prob_series >= threshold].index  # 상위 5% 구간 추출

# Step 3: 상위 5% 구간에서 무작위로 포인트 선택
def random_point_from_interval(interval):
    return np.random.uniform(interval.left, interval.right)  # 구간 내 임의의 포인트

random_interval = np.random.choice(top_5_percent_intervals)  # 상위 구간 중 하나를 무작위 선택
random_point = random_point_from_interval(random_interval)  # 선택된 구간 내에서 무작위 포인트 생성

print(f"Randomly selected point: {random_point}")
