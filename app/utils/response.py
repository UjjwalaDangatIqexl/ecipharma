# app/utils/response.py
def create_response(success, message, data=None):
    response = {
        "status": {
            "message": message,
            "success": success
        }
    }
    if data:
        response["data"] = data
    return response
