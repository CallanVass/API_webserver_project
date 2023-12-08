
import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Establishing configparser
config = configparser.ConfigParser()

# Telling configparser which file to read from
config.read("config.ini")

# Passing variables from configparser into this file
sender_email = config.get("Email", "sender_email")
password = config.get("Email", "password")
receiver_email = config.get("Email", "recipient_email")

# Create the MIME object for the email
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Internship Status Update"

# Add the email body
body = "This is the body of the email."
message.attach(MIMEText(body, "plain"))

# Establish a connection to the SMTP server
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    # Start the TLS connection (for secure connection)
    server.starttls()
    
    # Log in to the email account
    server.login(sender_email, password)
    
    # Send the email
    server.sendmail(sender_email, receiver_email, message.as_string())

print("Email sent successfully.")


