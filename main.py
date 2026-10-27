import os
import requests

SID = os.environ["TWILIO_ACCOUNT_SID"]
TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

numbers = [
    "whatsapp:+919074526392",
    "whatsapp:+917994046289"
]

url = f"https://api.twilio.com/2010-04-01/Accounts/{SID}/Messages.json"

for number in numbers:
    data = {
        "From": "whatsapp:+17372508034",
        "To": number,
        "Body": "🔔 Exam Alert Bot is working! Goethe + telc alerts coming soon 🇩🇪"
    }

    response = requests.post(
        url,
        data=data,
        auth=(SID, TOKEN),
        timeout=30
    )

    print("Status:", response.status_code)
    print("Response:", response.text)
