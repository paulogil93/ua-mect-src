import sys
import pandas as pd

# Get the file names from the CLI
f1 = sys.argv[1]
f2 = sys.argv[2]

# Read data and test datasets
df1 = pd.read_parquet(f1)
df2 = pd.read_parquet(f2)

# Define the DNS servers
dns_servers = ["192.168.108.226", "192.168.108.234"]

# Filter the flows where src_ip connects to DNS servers
dns_flows = df2[df2["dst_ip"].isin(dns_servers)]

# Count the number of flows for each src_ip
flow_counts = dns_flows["src_ip"].value_counts()

# Print the flow counts
print(flow_counts)