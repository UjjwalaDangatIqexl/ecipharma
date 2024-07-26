class Document:
    def __init__(self, file_path, textract_response, user_id):
        self.file_path = file_path
        self.textract_response = textract_response
        self.user_id = user_id

    def to_dict(self):
        return {
            'file_path': self.file_path,
            'textract_response': self.textract_response,
            'user_id': self.user_id
        }
