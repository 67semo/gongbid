import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Load the uploaded CSV file
file_path = 'abe.csv'
data = pd.read_csv(file_path)

# Set the range column as index for easier plotting
data.set_index('Unnamed: 0', inplace=True)
print(data.columns)

# Select a few columns for visualization
selected_columns = ['count', 'count.1', 'count.2', 'count.3', 'count.4']

# Prepare data for 3D dot plotting
fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')

# Plot dots for each data point in the selected columns
x_indices = np.arange(len(data.index))
for i, col in enumerate(data.columns):
    ax.scatter(x_indices, [i] * len(x_indices), data[col].values, label=col, s=10)

# Customize labels and title
ax.set_title('3D Dot Plot of Companies Across Bidding Zones')
ax.set_xlabel('Bidding Zone Range')
ax.set_ylabel('Company Count Columns')
ax.set_zlabel('Count of Companies')
ax.set_xticks(x_indices[::50])  # Fewer ticks for better readability
ax.set_xticklabels(data.index[::50], rotation=45, ha='right')

# Show legend
ax.legend(title='Company Count Columns')

# Show the plot
plt.tight_layout()
plt.show()

