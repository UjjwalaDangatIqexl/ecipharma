from flask import Blueprint, request, jsonify
from app.services.document_service import process_document, get_document_by_id

document_bp = Blueprint('document', __name__)


@document_bp.route('/process_document', methods=['POST'])
def handle_document():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to a temporary location
    file_path = f'temp/{file.filename}'
    file.save(file_path)

    try:
        # Process the document
        document_id = process_document(file_path)
        return jsonify({'document_id': str(document_id)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@document_bp.route('/document/<document_id>', methods=['GET'])
def get_document(document_id):
    try:
        document = get_document_by_id(document_id)
        if document:
            return jsonify(document), 200
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
