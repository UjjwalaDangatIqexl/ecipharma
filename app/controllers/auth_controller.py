from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

auth_bp = Blueprint('auth', __name__)


def create_response(success, message, user=None):
    response = {
        "status": {
            "message": message,
            "success": success
        }
    }
    if user:
        response["user"] = user
    return response


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    customer_name = data.get('customer_name')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    mobile_number = data.get('mobile_number')

    if not all([customer_name, first_name, last_name, email, mobile_number]):
        return jsonify(create_response(False, "Missing fields")), 400

    user, message = UserService.create_user(customer_name, first_name, last_name, email, mobile_number)
    if user:
        user_data = {
            "customer_name": user.customer_name,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "mobile_number": user.mobile_number
        }
        return jsonify(create_response(True, message, user_data)), 201
    return jsonify(create_response(False, message)), 400


@auth_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if not all([email, otp]):
        return jsonify(create_response(False, "Missing fields")), 400

    user, message = UserService.verify_otp(email, otp)
    if user:
        return jsonify(create_response(True, message)), 200
    return jsonify(create_response(False, message)), 400


@auth_bp.route('/set_password', methods=['POST'])
def set_password():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify(create_response(False, "Missing fields")), 400

    user, message = UserService.set_password(email, password)
    if user:
        return jsonify(create_response(True, message)), 200
    return jsonify(create_response(False, message)), 400


@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify(create_response(False, "Missing fields")), 400

    user, message = UserService.authenticate_user(email, password)
    if user:
        user_data = {"name": user.first_name, "email": user.email}
        return jsonify(create_response(True, message, user_data)), 200
    return jsonify(create_response(False, message)), 401


@auth_bp.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    email = data.get('email')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not all([email, current_password, new_password]):
        return jsonify(create_response(False, "Missing fields")), 400

    user, message = UserService.change_password(email, current_password, new_password)
    if user:
        return jsonify(create_response(True, message)), 200
    return jsonify(create_response(False, message)), 400
