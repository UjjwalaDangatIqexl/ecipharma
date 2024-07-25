from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    customer_name = data.get('customer_name')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    mobile_number = data.get('mobile_number')

    if not all([customer_name, first_name, last_name, email, mobile_number]):
        return jsonify({"error": "Missing fields"}), 400

    user, message = UserService.create_user(customer_name, first_name, last_name, email, mobile_number)
    if user:
        return jsonify({"message": message}), 201
    return jsonify({"error": message}), 400


@auth_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if not all([email, otp]):
        return jsonify({"error": "Missing fields"}), 400

    user, message = UserService.verify_otp(email, otp)
    if user:
        return jsonify({"message": message}), 200
    return jsonify({"error": message}), 400


@auth_bp.route('/set_password', methods=['POST'])
def set_password():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Missing fields"}), 400

    user, message = UserService.set_password(email, password)
    if user:
        return jsonify({"message": message}), 200
    return jsonify({"error": message}), 400


@auth_bp.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Missing fields"}), 400

    user, message = UserService.authenticate_user(email, password)
    if user:
        return jsonify({"message": message, "user": {"name": user.first_name, "email": user.email}}), 200

    return jsonify({"error": message}), 401


@auth_bp.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    email = data.get('email')
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not email or not current_password or not new_password:
        return jsonify({"message": "Missing required fields"}), 400

    user, message = UserService.change_password(email, current_password, new_password)
    if user:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 400
