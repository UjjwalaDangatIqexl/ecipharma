from werkzeug.security import generate_password_hash, check_password_hash

# Define the password
password = "securepassword"

# Generate the hash
hashed_password = generate_password_hash(password, method='scrypt')
print(f"Generated hash: {hashed_password}")

# Check the password against the hash
is_valid = check_password_hash(hashed_password, password)
print(f"Password valid: {is_valid}")
