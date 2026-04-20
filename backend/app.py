from fastapi import FastAPI
from pydantic import BaseModel
from twilio.rest import Client
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SMSRequest(BaseModel):
    to: str
    message: str
    alert_type: str

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/api/send-sms")
def send_sms(data: SMSRequest):
    print("FROM VALUE:", os.getenv("TWILIO_FROM_NUMBER"))
    try:
        client = Client(
            os.getenv("TWILIO_SID"),
            os.getenv("TWILIO_AUTH")
        )

        msg = client.messages.create(
            body=data.message,
            from_="+16203495308",
            to=data.to
        )

        return {"success": True, "sid": msg.sid}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/register-phone")
def register(phone: dict):
    return {"success": True}
