import os
from fastapi import FastAPI, HTTPException, Request, APIRouter
from twilio.rest import Client
from dotenv import load_dotenv

import requests

load_dotenv()

app = FastAPI()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

router = APIRouter(prefix="/notification-mgr")

@router.post("/send-sms/")
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

@router.post("/send-whatsapp/")
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

@router.get("/health")
async def health_check():
    try:
        instance_id = requests.get("http://169.254.169.254/latest/meta-data/instance-id", timeout=1).text
        az = requests.get("http://169.254.169.254/latest/meta-data/placement/availability-zone", timeout=1).text
        return {
            "status": "healthy",
            "instance_id": instance_id,
            "availability_zone": az
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

app.include_router(router)