import sys
import pandas as pd

# Get the file names from the CLI
f1 = sys.argv[1]
f2 = sys.argv[2]

# Read data and test datasets
df1 = pd.read_parquet(f1)
df2 = pd.read_parquet(f2)

# Group the DataFrame by src_ip and dst_ip and calculate the sum of up_bytes and down_bytes
grouped_df = df1.groupby(['src_ip', 'dst_ip']).agg({'up_bytes': 'sum', 'down_bytes': 'sum'})

# Calculate the total sum of bytes for each pair of src_ip and dst_ip
grouped_df['total_bytes'] = grouped_df['up_bytes'] + grouped_df['down_bytes']

# Sort the DataFrame by the total sum of bytes in descending order
grouped_df = grouped_df.sort_values('up_bytes', ascending=False)

# Display the resulting DataFrame
print(grouped_df.head(50))