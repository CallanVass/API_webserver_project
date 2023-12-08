import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from setup import db
from models.user import User


# Establishing configparser
config = configparser.ConfigParser()

# Telling configparser which file to read from
config.read("config.ini")



def send_email(email, name):

    # Passing variables from configparser into this file
    sender_email = config.get("Email", "sender_email")
    password = config.get("Email", "password")
    receiver_email = email
    user_name = name

    # Create the MIME object for the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Internship Status Update"

    # Add the email body
    body = f"""
Dear {user_name}
There has been an update to one of your internship statuses.

Please log on to view the updated status.

Kind Regards,
The Partnerships Team
"""
    message.attach(MIMEText(body, "plain"))

    # Establish connection to the SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:

        # Start the TLS connection (for secure connection)
        server.starttls()
        
        # Log in to the email account
        server.login(sender_email, password)
        
        # Send the email itself
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent successfully.")


