import os
from twilio.rest import Client

SID = os.environ["TWILIO_ACCOUNT_SID"]
TOKEN = os.environ["TWILIO_AUTH_TOKEN"]

client = Client(SID, TOKEN)

message = client.messages.create(
    from_="whatsapp:+17372508034",
    to="whatsapp:+YOUR_NUMBER",
    body="🔔 Exam Alert Bot is working! Goethe + telc alerts coming soon 🇩🇪"
)

print("WhatsApp message sent:", message.sid)
