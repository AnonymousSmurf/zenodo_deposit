# Zenodo Deposit

Zenodo Deposit is a Python Flask application that provides RESTful APIs to create a deposition on Zenodo and upload files to a given deposition.

## Features

- **Create Deposition**: Create a new deposition on Zenodo with specified metadata.
- **Upload File**: Upload a file to a specific deposition on Zenodo.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/zenodo-uploader.git
   ```

2. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**: Copy the `.env.example` file to `.env` and update the values for your specific Zenodo credentials and configuration:

   ```env
   ZENODO_ACCESS_TOKEN=YOUR_TOKEN
   ZENODO_BASE_URL=https://zenodo.org/api/
   DEPOSITION_ENDPOINT=deposit/depositions
   ```

5. **Start the Server**:

   ```bash
   python zenodo_deposit.py
   ```

## Usage

### Create Deposition

**Endpoint**: `/create-deposition`
**Method**: `POST`
**Body**: JSON with metadata as per Zenodo's schema.

**Example**:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "metadata": {
    "upload_type": "dataset",
    "title": "Sample Dataset",
    "creators": [
      {
        "name": "Doe, John",
        "affiliation": "Zenodo"
      }
    ],
    "description": "This is a sample dataset for testing purposes.",
    "access_right": "open",
    "license": "cc-zero"
  }
}' http://127.0.0.1:5000/create-deposition
```

### Upload File

**Endpoint**: `/upload-file/<deposition_id>`
**Method**: `POST`
**Body**: Multipart file data.

**Example**:

```bash
curl -X POST -F "file=@test.txt" http://127.0.0.1:5000/upload-file/<deposition_id>
```

Replace `<deposition_id>` with the actual deposition ID.