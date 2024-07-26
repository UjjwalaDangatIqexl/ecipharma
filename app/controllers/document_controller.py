from flask import Blueprint, request, jsonify, send_file
from app.services.document_service import process_document, get_document_by_id
import os

document_bp = Blueprint('document', __name__)


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


@document_bp.route('/process_document', methods=['POST'])
def handle_document():
    data = request.form
    user_id = data.get('user_id')

    if 'file' not in request.files:
        return jsonify(create_response(False, 'No file part')), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(create_response(False, 'No selected file')), 400

    # Save the file to a temporary location
    file_path = f'temp/{file.filename}'
    file.save(file_path)

    try:
        # Process the document
        document_id = process_document(file_path, user_id)
        return jsonify(create_response(True, 'Document processed successfully', {'document_id': str(document_id)})), 200
    except Exception as e:
        return jsonify(create_response(False, str(e))), 500


@document_bp.route('/document/<document_id>', methods=['GET'])
def get_document(document_id):
    try:
        document = get_document_by_id(document_id)
        if document:
            return jsonify(create_response(True, 'Document retrieved successfully', document)), 200
        else:
            return jsonify(create_response(False, 'Document not found')), 404
    except Exception as e:
        return jsonify(create_response(False, str(e))), 500


@document_bp.route('/document/<document_id>/file', methods=['GET'])
def get_document_file(document_id):
    try:
        document = get_document_by_id(document_id)
        if document:
            file_path = document['file_path']
            if os.path.exists(file_path):
                return send_file(file_path)
            else:
                return jsonify(create_response(False, 'File not found on server')), 404
        else:
            return jsonify(create_response(False, 'Document not found')), 404
    except Exception as e:
        return jsonify(create_response(False, str(e))), 500
