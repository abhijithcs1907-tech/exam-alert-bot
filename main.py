import os
from twilio.rest import Client

SID = os.environ["TWILIO_ACCOUNT_SID"]
TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

client = Client(SID, TOKEN)

numbers = [
    "whatsapp:+919074526392",
    "whatsapp:+917994046289"
]

for number in numbers:
    message = client.messages.create(
        from_="whatsapp:+17372508034",
        to=number,
        body="🔔 Exam Alert Bot is working! Goethe + telc alerts coming soon 🇩🇪"
    )
    print("Message sent:", message.sid)
