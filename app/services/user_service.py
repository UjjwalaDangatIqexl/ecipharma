import random
import string
import logging

from werkzeug.security import generate_password_hash
from app.utils.email_utils import send_email_otp
from app.models.user import User


class UserService:
    @staticmethod
    def create_user(customer_name, first_name, last_name, email, mobile_number):
        if User.find_by_email(email):
            return None, "Email already exists"

        otp = ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit OTP
        user = User(
            customer_name=customer_name,
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile_number=mobile_number,
            otp=otp
        )
        user.save_to_db()

        # send_email_otp(email, otp)
        send_email_otp(email, otp)

        return user, {"message": "created user successfully", "success": True}

    @staticmethod
    def verify_otp(email, entered_otp):
        user = User.find_by_email(email)
        if user and user.otp == entered_otp:
            user.otp = "-1"  # Invalidate the OTP
            user.save_to_db()
            return user, {"message": "OTP verified", "success": True}
        return None, "Invalid OTP"

    @staticmethod
    def set_password(email, password):
        user = User.find_by_email(email)
        hashed_password = generate_password_hash(password, method='scrypt')
        print(f"generated password: {hashed_password}")
        if user and user.otp == "-1":  # Ensure OTP has been verified
            user.password = hashed_password
            user.save_to_db()
            return user, {"message": "Password set successfully", "success": True}
        return None, "OTP verification required"

    def authenticate_user(email, password):
        user = User.find_by_email(email)
        if user:
            if user.check_password(password):
                return user, {"message": "Authentication successful", "success": True}
            else:
                logging.warning(f"Password mismatch for user {email}.")
        else:
            logging.warning(f"User {email} not found.")
        return None, {"message": "Invalid email or password", "success": True}

    def change_password(email, current_password, new_password):
        user = User.find_by_email(email)
        if user:
            if user.check_password(current_password):
                hashed_new_password = generate_password_hash(new_password, method='scrypt')
                user.password = hashed_new_password
                user.save_to_db()
                return user, {"message": "Password changed successfully", "success": True}
            else:
                return None, {"message": "Current password is incorrect", "success": True}
        return None, {"message": "User not found", "success": True}
