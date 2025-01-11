import requests
import os
import time
from datetime import datetime

# Function to read tokens from datas.txt
def read_tokens(file_path):
    with open(file_path, 'r') as f:
        tokens = f.readlines()
    return [token.strip() for token in tokens]

# Function to attempt boost in the given order
def try_boost(token):
    boost_types = ["farmer", "beehive", "bee", "honey"]
    base_url = "https://api.beeharvest.life/user/boost/{}/next_level"

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'origin': 'https://beeharvest.life',
        'referer': 'https://beeharvest.life/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    for boost_type in boost_types:
        url = base_url.format(boost_type)
        response = requests.post(url, headers=headers)
        
        if response.status_code == 200:
            print(f"Boost successful for {boost_type} using token.")
            return True
        else:
            print(f"Failed to boost {boost_type}, trying next...")

    print("All boost attempts failed.")
    return False

# Function to send boost requests every 2 minutes
def send_boost_requests_every_2_minutes(file_path):
    tokens = read_tokens(file_path)
    while True:
        for token in tokens:
            try_boost(token)
        time.sleep(120)  # Wait for 2 minutes before sending the next request

# Run the script
if __name__ == '__main__':
    # Start sending boost requests every 2 minutes
    send_boost_requests_every_2_minutes('datas.txt')
