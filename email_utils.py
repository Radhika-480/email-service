import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_welcome_email(to_email: str, password: str) -> bool:
    try:
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("welcome.html")

        # Render the template with email and password
        html = template.render(password=password, email=to_email)

        # Create the email message
        msg = MIMEMultipart("related")  # Use "related" for images
        msg["Subject"] = "Welcome to Our Store!"
        msg["From"] = EMAIL_USER
        msg["To"] = to_email

        # Attach the HTML content
        msg.attach(MIMEText(html, "html"))

        # Attach the image
        with open("assets/image.jpeg", "rb") as image_file:
            image = MIMEImage(image_file.read(), name="image.jpeg")
            image.add_header("Content-ID", "<welcome_image>")
            msg.attach(image)

        # Send the email
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
        return True

    except Exception as e:
        print("Error sending email:", e)
        return False