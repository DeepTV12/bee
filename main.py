import requests
import os
import time
from datetime import datetime

# Function to read tokens from datas.txt
def read_tokens(file_path):
    with open(file_path, 'r') as f:
        tokens = f.readlines()
    return [token.strip() for token in tokens]

# Function to get tasks using the provided authorization token
def get_tasks(token):
    url = 'https://api.beeharvest.life/tasks/user'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'origin': 'https://beeharvest.life',
        'referer': 'https://beeharvest.life/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Failed to get tasks for token: {token}")
        return []

# Function to check task using the provided authorization token and task_id
def check_task(token, task_id):
    url = 'https://api.beeharvest.life/tasks/check_task/'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'origin': 'https://beeharvest.life',
        'referer': 'https://beeharvest.life/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    data = {'taskId': task_id}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print(f"Task {task_id} checked successfully for token:")
    else:
        print(f"Failed to check task {task_id} for token:")

# Function to get the last run date
def get_last_run_date(run_file):
    if os.path.exists(run_file):
        with open(run_file, 'r') as f:
            return f.read().strip()
    return None

# Function to update the last run date
def update_last_run_date(run_file):
    with open(run_file, 'w') as f:
        f.write(datetime.now().strftime('%Y-%m-%d'))

# Main function to process tasks for all tokens
def process_tasks(file_path, run_file):
    last_run_date = get_last_run_date(run_file)
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Only proceed if tasks haven't been run today
    if last_run_date != current_date:
        tokens = read_tokens(file_path)

        for token in tokens:
            tasks = get_tasks(token)
            
            for task in tasks:
                task_id = task.get('id')
                if task_id:
                    check_task(token, task_id)

        # Update the last run date to today
        update_last_run_date(run_file)
    else:
        print("Tasks have already been run today.")

# Function to send the boost honey request every 2 minutes
def send_boost_request(token):
    url = 'https://api.beeharvest.life/user/boost/honey/next_level'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': f'Bearer {token}',
        'origin': 'https://beeharvest.life',
        'referer': 'https://beeharvest.life/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(f"Boost request sent successfully for token:")
    else:
        print(f"Failed to send boost request for token:")

# Function to send requests every 2 minutes
def send_boost_requests_every_2_minutes(file_path):
    tokens = read_tokens(file_path)
    while True:
        for token in tokens:
            send_boost_request(token)
        time.sleep(120)  # Wait for 2 minutes before sending the next request

# Run the script
if __name__ == '__main__':
    # Provide the path to datas.txt and a file to store the last run date
    run_file = 'last_run_date.txt'
    
    # Process tasks once per day
    process_tasks('datas.txt', run_file)

    # Start sending boost requests every 2 minutes
    send_boost_requests_every_2_minutes('datas.txt')
