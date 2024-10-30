import streamlit as st
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Set up your email credentials
email_key = st.secrets["email_key"]
email_from = st.secrets["email_from"]
email_username = st.secrets["email_username"]
email_password = st.secrets["email_password"]

def send_email(email, key, filename):
    if key == email_key:
        smtp_send_email(email, filename)
    else:
        st.error('Invalid Key', icon="🚨")

def smtp_send_email(email_to, filename):
    print("Going to send email")

    try:
        # Create a multipart message
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = "Stocky - Stock Analysis File"

        # Attach the email body
        msg.attach(MIMEText("Hi, this is an automated email with attachment. Please do not reply.", 'plain'))

        # Attach the file
        if filename:
            with open(filename, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(filename)}")
                msg.attach(part)

        # Set up the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Change for other email services
            server.starttls()  # Secure the connection
            server.login(email_username, email_password)  # Log in to the server
            server.send_message(msg)  # Send the email

        st.success('Email sent, wohoo!', icon="✅")
        os.remove(filename)
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

