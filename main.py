from fastapi import FastAPI, HTTPException, status
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

def generate_password(length: int = 10) -> str:
    characters = string.ascii_letters + string.digits + "!@#$%&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

@app.get("/")
def root():
    return {"message": "Email Service is running 🚀"}

@app.post("/send-email", status_code=status.HTTP_200_OK)
def send_email(payload: EmailRequest):
    password = generate_password()
    success = send_welcome_email(payload.email, password)

    if success:
        return {
            "message": "Email sent successfully",
            "email": payload.email,
            "password": password  # for frontend to show to user (temp login)
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send welcome email"
        )
