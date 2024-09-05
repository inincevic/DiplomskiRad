import json, statistics

# opening the JSON data files for IPv4 communicaiton and IPv6 communication
with open('http_IPv4_capture_data.json', 'r') as file:
    full_http_traffic = json.load(file)
with open('coap_IPv4_capture_data_client_side.json', 'r') as file:
    coap_http_traffic = json.load(file)
with open('coap_IPv6_capture_data_client_side.json', 'r') as file:
    coap_http_traffic_IPv6 = json.load(file)


total_data_size = 0
all_durations = []

# analyzing data for client -> proxy communication
for record in full_http_traffic:
    if record['Port B'] == "8000":
        total_data_size = total_data_size + int(record['Bytes'])
        all_durations.append(float(record['Duration']))
        #print(record['Port B'])
        pass

print("Komunikacija na portu 8000.")
print("Komunikacija izmedu klijenta i posrednika (HTTP -> HTTP)")
print("Ukupna velicina prijenosa", total_data_size)
print("Prosijecno trajanje komunikacije", statistics.mean(all_durations))
print("---------------------------------------------------------")

total_data_size = 0
all_durations = []

# analyzing data for proxy -> server communication
for record in full_http_traffic:
    if record['Port B'] == "8002":
        total_data_size = total_data_size + int(record['Bytes'])
        all_durations.append(float(record['Duration']))
        #print(record['Port B'])
        pass

print("Komunikacija na portu 8002.")
print("Komunikacija izmedu posrednika (HTTP -> HTTP) i servera")
print("Ukupna velicina prijenosa", total_data_size)
print("Prosijecno trajanje komunikacije", statistics.mean(all_durations))
print("---------------------------------------------------------")

total_data_size = 0
all_durations = []

# analyzing data for client (HTTP) -> proxy (HTTP -> CoAP) communication
for record in coap_http_traffic:
    if record['Port B'] == "8000":
        total_data_size = total_data_size + int(record['Bytes'])
        all_durations.append(float(record['Duration']))
        #print(record['Port B'])
        pass

print("Komunikacija na portu 8000.")
print("Komunikacija izmedu klijenta i posrednika (HTTP -> CoAP)")
print("Ukupna velicina prijenosa", total_data_size)
print("Prosijecno trajanje komunikacije", statistics.mean(all_durations))
print("---------------------------------------------------------")

total_data_size = 0
all_durations = []

# analyzing data for client (HTTP) -> proxy (HTTP -> CoAP) communication in IPv6
for record in coap_http_traffic_IPv6:
    if record['Port B'] == "8000":
        total_data_size = total_data_size + int(record['Bytes'])
        all_durations.append(float(record['Duration']))
        #print(record['Port B'])
        pass

print("Komunikacija na portu 8000 i protokolu IPv6.")
print("Komunikacija izmedu klijenta i posrednika (HTTP -> CoAP)")
print("Ukupna velicina prijenosa", total_data_size)
print("Prosijecno trajanje komunikacije", statistics.mean(all_durations))