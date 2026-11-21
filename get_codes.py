# Test script to generate the totp code every 30s (on :00 and :30)
from backend.util.totp import generate_code
from time import sleep
from datetime import datetime

key = input("> ")

while True:
    print(generate_code(key))
    sleep(30 - datetime.timestamp(datetime.now()) % 30)
