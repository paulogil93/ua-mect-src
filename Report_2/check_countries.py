import sys
import pygeoip
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

# Add the 'country' column based on 'dst_ip' for df1
df1['country'] = df1['dst_ip'].apply(get_country)

# Get a list of unique countries from df1
unique_countries = df1['country'].unique()

# Add the 'country' column based on 'dst_ip' for df2
df2['country'] = df2['dst_ip'].apply(get_country)

# Find flows in df2 with new countries
new_flows = df2[~df2['country'].isin(unique_countries)]

new_countries = {}

# Generate SIEM alerts for new flows
for index, row in new_flows.iterrows():
    timestamp = row['timestamp']
    src_ip = row['src_ip']
    dst_ip = row['dst_ip']
    down_bytes = row['down_bytes']
    up_bytes = row['up_bytes']
    country = row['country']
    if country not in new_countries:
        new_countries[country] = 1
    else:
        new_countries[country] = new_countries[country] + 1
    siem_message = f"SIEM Alert: Anomaly detected - New country detected in network flows. Timestamp: {timestamp}, src_ip: {src_ip}, dst_ip: {dst_ip}, country: {country}, up_bytes: {up_bytes}, down_bytes: {down_bytes}"
    print(siem_message)

print(new_countries)