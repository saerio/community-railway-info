from flask import Blueprint, request, jsonify, current_app, session
from werkzeug.utils import secure_filename
import os
import uuid
import json

trainlib = Blueprint('trainlib', __name__)

# Define the upload folder path directly within the blueprint
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # Adjust path as necessary
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Make sure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Simplified authentication check
def is_authenticated():
    return session.get('user') == True

# Image upload route
@trainlib.route('/upload', methods=['POST'])
def upload_file():
    # Check if the user is authenticated
    if not is_authenticated():
        return jsonify({"error": "User is not authenticated"}), 403
    
    # Ensure the request contains a file
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # If no file is selected
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Check if the file is allowed
    if file and allowed_file(file.filename):
        # Generate a unique UUID for the file
        unique_filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save the file
        file.save(file_path)
        
        # Create metadata for the uploaded file
        metadata = {
            'original_filename': file.filename,
            'uploaded_by': 'unknown',  # Since we are only checking `user == True`, there's no user data to include
            'file_uuid': unique_filename
        }
        
        # Save the metadata to a JSON file
        metadata_file_path = os.path.join(UPLOAD_FOLDER, unique_filename + '.json')
        with open(metadata_file_path, 'w') as f:
            json.dump(metadata, f, indent=4)
        
        return jsonify({"message": "File uploaded successfully", "file_uuid": unique_filename}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400
