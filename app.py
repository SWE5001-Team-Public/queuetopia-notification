import os
from fastapi import FastAPI, HTTPException, Request
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.post("/send-sms/")
async def send_sms(request: Request):
    try:
        data = await request.json()
        to = data["to"]
        body = data["body"]
        message = client.messages.create(
            to=to,
            from_=TWILIO_PHONE_NUMBER,
            body=body
        )
        return {"status": "SMS sent", "message_sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send-whatsapp/")
async def send_whatsapp(request: Request):
    try:
        data = await request.json()
        to = data["to"]
        body = data["body"]
        message = client.messages.create(
            to=f"whatsapp:{to}",
            from_="whatsapp:" + TWILIO_WHATSAPP_NUMBER,
            body=body
        )
        return {"status": "WhatsApp sent", "message_sid": message.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
