import pandas as pd


# Return a dataframe filtered with the client and server
def filter_by_ip(df, src, dest):

    filtered = df.loc[((df['Source'] == src) & (df['Destination'] == dest)) | ((df['Source'] == dest) & (df['Destination'] == src))]
    return filtered


# Return a dataframe filtered with by the Protocol
def filter_by_protocol(df, protocol):
    filtered = df.loc[df['Protocol'] == protocol]
    return filtered

# Function to extract the important values from the info column
def extract_values(row):

    delimited = row["Info"].split('[')[1].replace(']','')
    delimited = delimited.replace(', ',',')
    data = delimited.split(' ')

    if len(data) == 5:
        flag = data[0]
        seq = int(data[1].split('=')[1])
        ack = None
        win = int(data[2].split('=')[1])
        length = int(data[3].split('=')[1])
    else:
        flag = data[0]
        seq = int(data[1].split('=')[1])
        ack = int(data[2].split('=')[1])
        win = int(data[3].split('=')[1])
        length = int(data[4].split('=')[1])

    output = pd.DataFrame([flag, seq, ack, win, length]).T
    output.columns = ['Flag', 'SEQ', 'ACK', 'WIN', 'LEN']

    return output


# Convert the Info column into searchable columns
def make_dataframe_searchable(df):
    temp = pd.DataFrame()
    for index, row in df.iterrows():
        temp = temp.append(extract_values(row))

    df.reset_index(drop=True, inplace=True)
    temp.reset_index(drop=True, inplace=True)
    df2 = df.join(temp)

    return df2

def search_bad_ack(df, server, client):

    prev_server_to_client = None
    prev_client_to_server = None
    count = 0
    for index, row in df.iterrows():
        # Add logic to calculate packets
        print(row['SEQ'])

        #Keep track of the most recent exchanges
        if row['Source'] == server:
            prev_server_to_client = row
        if row['Source'] == client:
            prev_client = row



# Import CSV Files
file_name = 'ServerTraffic-F2018.csv'
df = pd.read_csv(file_name)

ip_filtered = filter_by_ip(df,'150.100.12.11', '150.100.0.2')
protocol_filtered = filter_by_protocol(ip_filtered, 'TCP')

# Run the desired IP through the filtering
df2 = make_dataframe_searchable(protocol_filtered)
# print(df2)

search_bad_ack(df2)