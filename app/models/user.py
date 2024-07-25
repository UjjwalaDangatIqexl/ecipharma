from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import logging


class User:
    def __init__(self, customer_name, first_name, last_name, email, mobile_number, password=None, otp=None):
        self.customer_name = customer_name
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.mobile_number = mobile_number
        self.password = password
        self.otp = otp

    def save_to_db(self):
        mongo = current_app.config['mongo']
        mongo.db.users.update_one({'_id': self.id}, {'$set': self.to_dict()}, upsert=True)

    @classmethod
    def find_by_email(cls, email):
        mongo = current_app.config['mongo']
        user_data = mongo.db.users.find_one({"email": email})
        if user_data:
            return cls.from_dict(user_data)
        return None

    @classmethod
    def from_dict(cls, data):
        user = cls(
            customer_name=data['customer_name'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            mobile_number=data['mobile_number'],
            password=data['password'],
            otp=data['otp']
        )
        user.id = data['_id']
        return user

    def to_dict(self):
        return {
            "_id": self.id,
            "customer_name": self.customer_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "mobile_number": self.mobile_number,
            "password": self.password,
            "otp": self.otp
        }

    def check_password(self, password):
        logging.info(
            f"Checking password for user {self.email}. Provided password: {password}, Stored hash: {self.password}")
        print(f"Stored password hash: {self.password}")
        print(f"Checking password: {password}")
        is_valid = check_password_hash(self.password, password)
        print(f"Password valid: {is_valid}")
        return is_valid
