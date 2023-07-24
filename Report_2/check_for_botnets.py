import sys
import pygeoip
import ipaddress
import pandas as pd

gi=pygeoip.GeoIP('./GeoIP.dat')
gi2=pygeoip.GeoIP('./GeoIPASNum.dat')

# Function to get country code from IP
def get_country(ip):
    try:
        return gi.country_name_by_addr(ip)
    except Exception:
        return 'Unknown'

# Get the file names from the CLI
f1 = sys.argv[1]
f2 = sys.argv[2]

# Read data and test datasets
df1 = pd.read_parquet(f1)
df2 = pd.read_parquet(f2)

# Filter rows with private source and destination IP addresses
private_ips = df1[(df1['src_ip'].apply(lambda ip: ipaddress.ip_address(ip).is_private)) & 
                 (df1['dst_ip'].apply(lambda ip: ipaddress.ip_address(ip).is_private))]

# Get unique pairs of private source and destination IP addresses
unique_pairs = private_ips[['src_ip', 'dst_ip', 'proto', 'port']].drop_duplicates()

unique_pairs = unique_pairs.groupby(['dst_ip', 'proto', 'port']).size().reset_index(name='count')

# Print the result
print(unique_pairs)