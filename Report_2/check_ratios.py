import sys
import pandas as pd

# Get the file names from the CLI
f1 = sys.argv[1]
f2 = sys.argv[2]

# Read data and test datasets
df1 = pd.read_parquet(f1)
df2 = pd.read_parquet(f2)

# Group the DataFrame by src_ip and dst_ip and calculate the sum of up_bytes and down_bytes
grp2 = df2.groupby(['src_ip', 'dst_ip']).agg({'up_bytes': 'sum', 'down_bytes': 'sum'})

# Calculate the ratio column
grp2['ratio'] = grp2['up_bytes'] / grp2['down_bytes']

# Sort the DataFrame by the absolute difference between ratio and 1

grp2['diff'] = abs(grp2['ratio'] - 1)
rdf2 = grp2.sort_values('diff')

# Print the resulting differences
print(rdf2.head(20))

