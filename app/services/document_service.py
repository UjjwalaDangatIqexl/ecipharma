from app.services.aws_textract_service import analyze_document
from app.services.mongodb_service import store_document_data, get_document_by_id as get_doc_by_id


def process_document(file_path):
    # Analyze the document using AWS Textract
    textract_response = analyze_document(file_path)

    # Process the response (you may need to adjust this based on your needs)
    document_data = {
        'file_path': file_path,
        'textract_response': textract_response
    }

    # Store the response in MongoDB
    document_id = store_document_data(document_data)
    return document_id


def get_document_by_id(document_id):
    return get_doc_by_id(document_id)
