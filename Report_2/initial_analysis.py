import sys
import ipaddress
import pandas as pd
import matplotlib.pyplot as plt

def is_private_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False

# Get the file names from the CLI
f1 = sys.argv[1]
f2 = sys.argv[2]

# Read data and test datasets
df1 = pd.read_parquet(f1)
df2 = pd.read_parquet(f2)

# Print unique column values in data8.parquet
print("\nDistinct proto in data8: {0}".format(df1['proto'].unique()))
print("Distinct port in data8: {0}".format(df1['port'].unique()))

# Print unique column values in test8.parquet
print("\nDistinct proto in test8: {0}".format(df2['proto'].unique()))
print("Distinct port in test8: {0}".format(df2['port'].unique()))

# Read the dataset with timestamps for df1
df1['timestamp'] = pd.to_timedelta(df1['timestamp']*10, unit='ms')
df1.set_index('timestamp', inplace=True)

# Read the dataset with timestamps for df2
df2['timestamp'] = pd.to_timedelta(df2['timestamp']*10, unit='ms')
df2.set_index('timestamp', inplace=True)

# Plot the number of flows over time for df1 and df2
plt.figure(figsize=(12, 6))

interval = '10Min'

# Plot for df1
flows_count_df1 = df1.resample(interval).size()
plt.plot(flows_count_df1, label='data8', color='blue')

# Plot for df2
flows_count_df2 = df2.resample(interval).size()
plt.plot(flows_count_df2, label='test8', color='red')

plt.xlabel('Time')
plt.ylabel('Number of Flows')
plt.title('Number of Flows Over Time ({0} interval)'.format(interval))
plt.legend()
plt.show()

