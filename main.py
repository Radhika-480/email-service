from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr
from email_utils import send_welcome_email
import secrets
import string

app = FastAPI()

# Serve static files (images, css, etc.)
app.mount("/static", StaticFiles(directory="assets"), name="static")

class EmailRequest(BaseModel):
    email: EmailStr

def generate_password(length=10):
    characters = string.ascii_letters + string.digits + "!@#$%&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.post("/send-email")
def send_email(payload: EmailRequest):
    password = generate_password()
    success = send_welcome_email(payload.email, password)
    if success:
        return {"message": "Email sent successfully", "password": password}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")