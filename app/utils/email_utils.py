# app/utils/email_utils.py
from flask_mail import Message
from flask import current_app
from app import mail


def send_email_otp(email, otp):
    msg = Message("Your OTP Code", sender=current_app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"Your OTP code is {otp}. Please use this to verify your email."
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")
