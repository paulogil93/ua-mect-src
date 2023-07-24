import sys
import pandas as pd

# Get the file names from the CLI
f1 = sys.argv[1]
f2 = sys.argv[2]

# Read data and test datasets
df1 = pd.read_parquet(f1)
df2 = pd.read_parquet(f2)

# Calculate variance for each group of the first DataFrame
var1 = df1.groupby(['src_ip', 'dst_ip'])['timestamp'].var()

# Calculate variance for each group of the second DataFrame
var2 = df2.groupby(['src_ip', 'dst_ip'])['timestamp'].var()

# Merge the variances from both DataFrames based on src_ip and dst_ip
comparison = pd.concat([var1, var2], axis=1, keys=['data8', 'test8'])

# Calculate the difference in variances
comparison['variance_difference'] = comparison['test8'] - comparison['data8']

# Sort the DataFrame by variance_difference in ascending order
sorted_variances = comparison.sort_values(by='test8', ascending=True)

print("Anomalies:")
print(sorted_variances)