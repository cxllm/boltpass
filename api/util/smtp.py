import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Specify the port as the one for STARTTLS and load info from .env file
port = 587
load_dotenv()
email = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASSWORD")
smtp_server = os.getenv("SMTP_SERVER")


def send_email(destination, subject, html_content, text_content):
    message = MIMEMultipart(
        "alternative"
    )  # This means HTML will be shown first, and if this fails then text (provides an alternative option)
    message["Subject"] = subject
    message["From"] = f"BoltPass <{email}>"
    message["To"] = destination
    # Convert the html and text into the correct format
    text = MIMEText(text_content, "plain")
    html = MIMEText(html_content, "html")
    # Attach them to message (this must be done in this order as the second one will be rendered first)
    message.attach(text)
    message.attach(html)
    # Open a connection to the SMTP server on the specified port
    with smtplib.SMTP(smtp_server, port) as server:
        # Connect using STARTTLS with SSL to provide a secure connection
        context = ssl.create_default_context()
        server.starttls(context=context)
        # Login using the login details from .env file
        server.login(email, password)
        # Send the email
        server.sendmail(email, destination, message.as_string())


def verification_email(user_email, user_id, url):
    verification_link = f"{url}api/user/{user_id}/verify-email?email={user_email}"
    html = f"""
<html>
    <body>
        <h1>Verify your email</h1>
        <p style="font-size:medium">Please verify your email by pressing <a href="{verification_link}">here</a></p>
        <i style="font-size:small">The link is provided below in case you cannot click on it:
            <br>
            {verification_link}
        </i>
    </body>
</html>
    """
    text = f"""Please verify your email by pressing on this link
    {verification_link}
    """
    send_email(user_email, "BoltPass User Verification", html, text)
