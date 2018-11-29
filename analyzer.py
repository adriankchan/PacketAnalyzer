import csv

# Read data from csv into array
def csv_to_array (file_name):
    data = []

    with open(file_name, 'r') as csv_file:
        packet_reader = csv.reader(csv_file, delimiter=',')

        for row in packet_reader:
            data.append(row)

    return data

# Return int value of transmission count given an array, source, destination, protocol
def count_transmission(data, source, destination,protocol):
    packet_transferred = 0
    for row in data:
        if row[4] == protocol:
            if row[2] == source:
                if row[3] == destination:
                    packet_transferred = packet_transferred + 1

    return packet_transferred

# Print out the transmission count given an array, source, destination, protocol
def print_count_result(data, source, destination, protocol):
    count = count_transmission(data, source, destination, protocol)
    print ('Packets from ' + source + ' -> ' + destination + ' = ' + str(count))


# 'main', currently bundled with the analyzer.py due to the small size
file_name = input('Enter the CSV file name:')
data = csv_to_array(file_name)

# Loop for user to choose script function to use
# Allow for expansion flexibility if needed for later projects
# Q breaks, the loop, 0 runs the predefined script, 1 for packet count.
while 1:
    user_input = input('Select desired function:\n(0) for preset instructions\n(1) to count packets\n(q) to exit\n')
    if user_input == 'q':
        break
    if user_input == '0':
        print_count_result(data, '192.168.0.1', '192.168.0.2','UDP')
        print_count_result(data, '192.168.0.2', '192.168.0.1', 'UDP')
        break
    if user_input == '1':
        source_ip = input('Enter source IP:')
        destination_ip = input('Destination IP:')
        protocol = input('Enter Protocol:')
        print_count_result(data,source_ip,destination_ip, protocol)



