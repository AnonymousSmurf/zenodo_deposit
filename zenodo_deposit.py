import json
from decouple import config
from flask import Flask, request, jsonify
import requests

# Load the metadata schema from an external JSON file.
with open('metadata_schema.json', 'r') as f:
    metadata_schema = json.load(f)

app = Flask(__name__)

# Retrieve configurations from environment variables.
BASE_URL = config('ZENODO_BASE_URL')
DEPOSITION_ENDPOINT = config('DEPOSITION_ENDPOINT')
ACCESS_TOKEN = config('ZENODO_ACCESS_TOKEN')

class ZenodoUploader:
    def __init__(self, base_url, deposition_endpoint, access_token):
        # Initialize ZenodoUploader with API details.
        self.base_url = base_url
        self.deposition_endpoint = deposition_endpoint
        self.access_token = access_token

    def create_new_deposition(self, metadata):
        # Create a new deposition on Zenodo.
        url = f"{self.base_url}{self.deposition_endpoint}?access_token={self.access_token}"
        headers = {"Content-Type": "application/json"}

        data = json.dumps({"metadata": metadata})
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError(f"Failed to create new deposition. Response: {response.text}")

    def upload_file_to_deposition(self, deposition_id, file_path):
        # Upload a file to an existing deposition on Zenodo.
        url = f"{self.base_url}{self.deposition_endpoint}/{deposition_id}/files?access_token={self.access_token}"
        print(url)
        data = {'name': file_path.split('/')[-1]}
        with open(file_path, 'rb') as fp:
            files = {'file': fp}
            response = requests.post(url, data=data, files=files)

        if response.status_code == 201:
            return response.json()
        else:
            raise ValueError(f"Failed to upload file. Response: {response.text}")

    def _validate_metadata(self, metadata):
        # Validate metadata against the loaded schema.
        required_keys = metadata_schema.get("required", [])
        return all(key in metadata for key in required_keys)

# Create an instance of the ZenodoUploader class.
uploader = ZenodoUploader(BASE_URL, DEPOSITION_ENDPOINT, ACCESS_TOKEN)

@app.route('/create-deposition', methods=['POST'])
def create_deposition():
    # API endpoint to create a new deposition.
    metadata = request.json.get('metadata')
    if not uploader._validate_metadata(metadata):
        return jsonify({'error': 'Metadata does not match the required schema!'}), 400

    try:
        response = uploader.create_new_deposition(metadata)
        return jsonify(response), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/upload-file/<deposition_id>', methods=['POST'])
def upload_file(deposition_id):
    # API endpoint to upload a file to a deposition.
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    file_path = file.filename
    file.save(file_path)

    try:
        response = uploader.upload_file_to_deposition(deposition_id, file_path)
        return jsonify(response), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# Entry point for the application.
if __name__ == '__main__':
    app.run(debug=True)
