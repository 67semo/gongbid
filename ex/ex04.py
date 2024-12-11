# 일정구단 랜덤한 값산출

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: 확률 분포 시리즈 정의 (예제 데이터)
index = pd.IntervalIndex.from_tuples([(0.975 + i * (1.025 - 0.975) / 200, 0.975 + (i + 1) * (1.025 - 0.975) / 200) for i in range(200)])
probabilities = np.random.rand(200)  # 확률 분포값 예제 (랜덤 값)
probabilities = probabilities / probabilities.sum()  # 확률 정규화
prob_series = pd.Series(probabilities, index=index)
print(prob_series)

# Step 2: 상위 5% 확률값 기준 구간 추출
threshold = prob_series.quantile(0.95)  # 상위 5% 임계값 계산
top_5_percent_intervals = prob_series[prob_series >= threshold].index  # 상위 5% 구간 추출

# Step 3: 상위 5% 구간에서 무작위로 포인트 선택
def random_point_from_interval(interval):
    return np.random.uniform(interval.left, interval.right)  # 구간 내 임의의 포인트

random_interval = np.random.choice(top_5_percent_intervals)  # 상위 구간 중 하나를 무작위 선택
random_point = random_point_from_interval(random_interval)  # 선택된 구간 내에서 무작위 포인트 생성

# 확률 값 가져오기
random_point_probability = prob_series[random_interval]

print(f"Randomly selected point: {random_point}")
print(f"Probability of the interval: {random_point_probability}")

# Step 4: 확률 분포 그래프 그리기
plt.figure(figsize=(10, 6))

# 그래프 플롯
interval_centers = [interval.mid for interval in prob_series.index]  # 구간 중심 계산
plt.plot(interval_centers, prob_series.values, label='Probability Distribution', color='blue')

# 상위 5% 구간 표시
for interval in top_5_percent_intervals:
    plt.axvspan(interval.left, interval.right, color='red', alpha=0.3, label='Top 5% (if not overlapped)')

# 선택된 포인트 표시
plt.scatter(random_point, random_point_probability, color='black', label='Selected Point', zorder=5)

# 그래프 레이블과 범례 추가
plt.title("Probability Distribution with Selected Point")
plt.xlabel("Interval Midpoints")
plt.ylabel("Probability")
plt.legend()
plt.grid()
plt.show()
