
import pandas as pd

# Simulate the data based on the provided structure
data = {
    'prcbdrBizno': [1018609399, 1058156661, 1058652224, 1078706456, 1098187282],
    '20241118413': [1.004864, None, 0.996760, 0.993741, 1.002784],
    '20241118818': [1.004864, None, 0.995796, 0.993739, 1.002167],
    '20241126017': [1.004937, 0.995081, 0.992990, None, 0.998571],
    '20241126745': [1.004938, 1.005652, 1.002445, 0.998739, None],
}
df = pd.DataFrame(data)

# Step 1: Set 'prcbdrBizno' as the index
df.set_index('prcbdrBizno', inplace=True)

# Step 2: Flatten the bidding points into a single column
bidding_points = df.stack()
print(f"bidding_points : {bidding_points}")

# Step 3: Define bins to categorize the bidding points (you can adjust the range and intervals)
bins = pd.cut(bidding_points, bins=200)
print(f"bins : {bins}")

# Step 4: Count the distribution of bidding points for each business code
distribution = bidding_points.groupby([bidding_points.index.get_level_values(0), bins]).count()
print(f"distribution : {distribution}")
# Step 5: Create a pivot table to show the distribution for each business code
result_df = distribution.unstack(fill_value=0)

print(result_df)


