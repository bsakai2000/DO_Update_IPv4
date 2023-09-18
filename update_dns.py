#!/usr/bin/env python3

import requests

# Must define a DigitalOcean token (do_token), the subdomain to modify (subdomain) and a domain name (domain_name)
import creds

# API to use
api = 'https://api.digitalocean.com'
# Authorization headers
headers = { 'Authorization' : 'Bearer ' + creds.do_token }

# Get the current record
def get_current_record():
    # Ask for all A records for this domain
    do_a_record = requests.get(api + '/v2/domains/' + creds.domain_name + '/records?type=A', headers = headers)

    # If we don't have a 200, fail
    if do_a_record.status_code != 200:
        print('Could not get current A record')
        print(do_a_record.json())
        exit()

    # Filter by subdomain
    records = do_a_record.json()['domain_records']
    records = filter(lambda record : record['name'] == creds.subdomain, records)
    records = list(records)

    # Return the first relevant record
    return records[0]

# Use ipify to get the current public IP address
def get_current_ip():
    return requests.get('https://api.ipify.org').text

# Update the A record 
def set_record(record_id, ipv4):
    # Set the data to the new IP address
    payload = { 'type' : 'A', 'data' : ipv4 }
    # Send the update request
    set_record = requests.patch(api + '/v2/domains/' + creds.domain_name + '/records/' + record_id, json = payload, headers = headers)
    # If we don't have a 200, fail
    if set_record.status_code != 200:
        print('Failed to update record')
        print(set_record.json())
        exit()


# Get the current record and the IP it should be
current_record = get_current_record()
current_ip = get_current_ip()
# If the record is inaccurate, update it
if current_record['data'] != current_ip:
    print('Records do not match')
    set_record(str(current_record['id']), current_ip)
