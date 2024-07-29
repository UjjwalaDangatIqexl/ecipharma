# app/document/controllers.py
from pathlib import Path

from flask import Blueprint, request, jsonify, send_file
from app.services.document_service import process_document, get_document_by_id
from app.utils.response import create_response
import os

document_bp = Blueprint('document', __name__)


@document_bp.route('/process_document', methods=['POST'])
def handle_document():
    data = request.form
    user_id = data.get('user_id')

    if not user_id:
        return jsonify(create_response(False, "Missing user_id")), 400

    if 'file' not in request.files:
        return jsonify(create_response(False, "No file part")), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(create_response(False, "No selected file")), 400

    # Ensure the temp directory exists
    temp_dir = 'temp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Save the file to a temporary location
    file_path = os.path.join(temp_dir, file.filename)
    print(f"Checking if file exists at: {file_path}")

    if os.path.exists(file_path):
        print("File exists.")
    else:
        print("File does not exist.")
    file.save(file_path)

    try:
        # Process the document
        document_id = process_document(file_path, user_id)
        return jsonify(create_response(True, "Document processed successfully", {"document_id": str(document_id)})), 200
    except Exception as e:
        return jsonify(create_response(False, str(e))), 500


@document_bp.route('/document/<document_id>/file', methods=['GET'])
def get_document_file(document_id):
    try:
        document = get_document_by_id(document_id)
        if document:
            file_path = Path(document['file_path']).resolve()
            print(f"Checking if file exists at: {file_path}")
            if file_path.exists():
                print(f"File found. Sending file...")
                return send_file(file_path)
            else:
                print(f"File not found at: {file_path}")
                return jsonify(create_response(False, 'File not found on server')), 404
        else:
            print("Document not found.")
            return jsonify(create_response(False, 'Document not found')), 404
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return jsonify(create_response(False, str(e))), 500
