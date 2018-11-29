import pandas as pd


# Return a dataframe filtered with the source and destination
def filter_by_ip(df, src, dest):

    filtered = df.loc[(df['Source'] == src) & (df['Destination'] == dest)]
    return filtered


# Return a dataframe filtered with by the Protocol
def filter_by_protocol(df, protocol):
    filtered = df.loc[df['Protocol'] == protocol]
    return filtered


# Search for the packets using the following search terms
# SYN
# SYN, ACK
# FIN, ACK
def filter_by_tcp_exchange(df, search_term):
    filtered = df[df['Info'].str.contains(search_term)]
    return filtered


# Import CSV Files
file_name = 'ServerTraffic-F2018.csv'
df = pd.read_csv(file_name)

# Run the desired IP through the filtering
ip_filtered = filter_by_ip(df,'150.100.12.11', '150.100.0.2')
protocol_filtered = filter_by_protocol(ip_filtered, 'TCP')

output = filter_by_tcp_exchange(protocol_filtered, 'FIN, ACK')
