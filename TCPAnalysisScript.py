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

# Get number of bad ack
def num_bad_ack(df, server):

    client_count = 0
    server_count = 0
    prev_server_to_client = None

    # Get Bad ACK from client
    for index, row in df.iterrows():
        # Store the data for comparison
        if row['Source'] == server:
            prev_server_to_client = row
        # Check for bad ACK
        else:
            current_ack = row['ACK']
            if prev_server_to_client is not None:
                prev_len = prev_server_to_client['SEQ'] + prev_server_to_client['LEN']
                if (current_ack != prev_len and current_ack != 1 and current_ack - prev_len != 1 ):
                    client_count = client_count + 1

    # Get Bad ACK from server
    for index, row in df.iterrows():
        # Store the data for comparison
        if row['Source'] != server:
            prev_server_to_client = row
        # Check for bad ACK
        else:
            current_ack = row['ACK']
            if prev_server_to_client is not None:
                prev_len = prev_server_to_client['SEQ'] + prev_server_to_client['LEN']
                if (current_ack != prev_len and current_ack != 1 and current_ack - prev_len != 1 ):
                    print(row['No.'])
                    server_count = server_count + 1

    return (client_count, server_count)


# Get number of Data Packets
def num_data_packets(df):
    fromClient = 0
    fromServer = 0
    for index, row in df.iterrows():
        if ('SYN' not in row['Flag'] or 'FIN' not in row['Flag']) and row['LEN'] != 0:
            if (row['Source'] == '150.100.0.2'):
                fromServer = fromServer + 1
            if (row['Destination'] == '150.100.0.2'):
                fromClient = fromClient + 1
    return (fromClient, fromServer)


# Get number of Dedicated Packet
def num_dedicated_ack(df):
    fromClient = 0
    fromServer = 0
    for index, row in df.iterrows():
        if ('ACK' in row['Flag'] and row['LEN'] == 0) and not ('SYN' in row['Flag'] or 'FIN' in row['Flag']):
            if (row['Source'] == '150.100.0.2'):
                fromServer = fromServer + 1
            if (row['Destination'] == '150.100.0.2'):
                fromClient = fromClient + 1
    return (fromClient, fromServer)


# Get number of Control packet
def num_ctrl_packets(df):
    fromClient = 0
    fromServer = 0
    for index, row in df.iterrows():
        if ('SYN' in row['Flag'] or 'FIN' in row['Flag']) and (row['Source'] == '150.100.0.2'):
            fromServer = fromServer + 1
        if ('SYN' in row['Flag'] or 'FIN' in row['Flag']) and (row['Destination'] == '150.100.0.2'):
            fromClient = fromClient + 1

    return (fromClient, fromServer)

# Get number of new packer
def num_new_packets(df):

    totalFromClient = 0
    totalFromServer = 0
    fromClient = 0
    fromServer = 0

    prev_server_to_client = None
    prev_client_to_server = None

    for index, row in df.iterrows():
        if ('ACK' in row['Flag'] and row['Source'] == '150.100.0.2'):
            totalFromServer = totalFromServer + 1
        if ('ACK' in row['Flag'] and row['Destination'] == '150.100.0.2'):
            totalFromClient = totalFromClient + 1


    for index, row in df.iterrows():

        if prev_server_to_client is not None:
            if ('ACK' in row['Flag'] and row['Source'] == '150.100.0.2'):
                if (row['ACK'] == prev_server_to_client['ACK']):
                    fromServer = fromServer + 1
        if('ACK' in row['Flag'] and row['Source'] == '150.100.0.2'):
            prev_server_to_client = row

        if prev_client_to_server is not None:
            if ('ACK' in row['Flag'] and row['Destination'] == '150.100.0.2'):
                if (row['ACK'] == prev_client_to_server['ACK']):
                    fromClient = fromClient + 1
        if ('ACK' in row['Flag'] and row['Destination'] == '150.100.0.2'):
            prev_client_to_server = row

    return (totalFromClient - fromClient, totalFromServer - fromServer)

# Get number of new packer
def num_redundant_ack(df):
    fromClient = 0
    fromServer = 0

    prev_server_to_client = None
    prev_client_to_server = None

    for index, row in df.iterrows():

        if prev_server_to_client is not None:
            if ('ACK' in row['Flag'] and row['Source'] == '150.100.0.2'):
                if (row['ACK'] == prev_server_to_client['ACK']):
                    fromServer = fromServer + 1
        if('ACK' in row['Flag'] and row['Source'] == '150.100.0.2'):
            prev_server_to_client = row

        if prev_client_to_server is not None:
            if ('ACK' in row['Flag'] and row['Destination'] == '150.100.0.2'):
                if (row['ACK'] == prev_client_to_server['ACK']):
                    fromClient = fromClient + 1
        if ('ACK' in row['Flag'] and row['Destination'] == '150.100.0.2'):
            prev_client_to_server = row
    return (fromClient, fromServer)

# Output the data in the desired format
def output_data(ctrl, data, new, redundant, dedicated, bad):
    print("Client to Server Traffic")
    print ("#Data Pckt:" + str(data[0]) + ", #Ctrl Pckt:" + str(ctrl[0]) + ", #New Ack:" + str(new[0]) + ", #Redn Pckt:" +
           str(redundant[0]) + ", #Dedicated Ack:" + str(dedicated[0]) + ", #Bad Ack:" + str(bad[0]))
    print("Client to Server Traffic")
    print ("#Data Pckt:" + str(data[1]) + ", #Ctrl Pckt:" + str(ctrl[1]) + ", #New Ack:" + str(new[1]) + ", #Redn Pckt:" +
           str(redundant[1]) + ", #Dedicated Ack:" + str(dedicated[1]) + ", #Bad Ack:" + str(bad[1]))

# Data pre-processing based server and client
def filter(df, server, client):

    ip_filtered = filter_by_ip(df, client, server)
    protocol_filtered = filter_by_protocol(ip_filtered, 'TCP')
    df2 = make_dataframe_searchable(protocol_filtered)

    return df2


# Import CSV Files

# Choose between user-input for the csv file or fixed name
#file_name = input("Enter File Name:")
file_name = 'ServerTraffic-F2018.csv'
df = pd.read_csv(file_name)

# For this example, we know the server IP
server = '150.100.0.2'

# Generate the ip for the 30 client machines as shown in the network
client_list = []

for i in range(130,140):
    client_list.append('150.100.12.' + str(i))
for i in range(3,13):
    client_list.append('150.100.12.' + str(i))
for i in range(2,12):
    client_list.append('150.100.15.' + str(i))


for i in client_list:
    df2 = filter(df, server, i)

    ctrl = num_ctrl_packets(df2)
    data = num_data_packets(df2)
    new = num_new_packets(df2)
    redundant = num_redundant_ack(df2)
    dedicated = num_dedicated_ack(df2)
    bad = num_bad_ack(df2, server)
    print(">  " + i + "  <")
    output_data(ctrl, data, new, redundant, dedicated, bad)
