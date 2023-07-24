import sys
import pyarrow.parquet as pq

# Specify the path to your parquet file
parquet_file = sys.argv[1]

# Read the parquet file
table = pq.read_table(parquet_file)

# Slice the table to get the first 1000 rows
sliced_table = table.slice(0, 1000)

# Convert the sliced table back to a parquet file
output_file = sys.argv[2]
pq.write_table(sliced_table, output_file)
