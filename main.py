import os
import requests

SID = os.environ["TWILIO_ACCOUNT_SID"]
TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

print("Exam Alert Bot started successfully!")
print("Twilio credentials found:", bool(SID and TOKEN))

# Test connection to Twilio
url = f"https://api.twilio.com/2010-04-01/Accounts/{SID}.json"

response = requests.get(url, auth=(SID, TOKEN), timeout=30)

if response.ok:
    print("Twilio connection: OK")
else:
    print("Twilio connection failed:", response.status_code)
