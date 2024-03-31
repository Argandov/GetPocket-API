#!/usr/bin/env python3

import requests
import sys
import json
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

POCKET_APP_NAME = os.environ.get("POCKET_APP_NAME")
POCKET_API_CONSUMER_KEY = os.environ.get("POCKET_API_CONSUMER_KEY")

url = "https://getpocket.com/v3/oauth/request"
headers = {
"Content-Type": "application/json; charset=UTF-8",
"X-Accept": "application/json"
}
payload = {
        "consumer_key": POCKET_API_CONSUMER_KEY,
        "redirect_uri": "https://google.com"
    }

response = requests.post(url, json=payload, headers=headers)

# REQUEST TOKEN:
data = response.json()
code = data["code"]

req_url = f"https://getpocket.com/auth/authorize?request_token={code}&redirect_uri=https://www.google.com"

print(f" - Code: {code}")
print(f" - Request URL; go to: {req_url}")

response = False
while response != True:
    verification = input(" > Authorized? y/n: ")
    if verification == "y":
        response = True
        print(" - Continuing...")

url = "https://getpocket.com/v3/oauth/authorize"
headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Accept": "application/json"
    }
payload = {
        "consumer_key": POCKET_API_CONSUMER_KEY,
        "code": code
    }

response = requests.post(url, json=payload, headers=headers)

if response.status_code = 200:
    print("OK. Application Authorized as:")
    res = response.text
    res = response.json()
    access_token = res["access_token"]
    username = res["username"]

    print(f" - Access Token: {access_token}")
    print(f" - Username: {username}")
    print("Completed.")
else:
    print(f"[X] Error: {response.status_code}")
