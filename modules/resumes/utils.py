import os
import uuid
from werkzeug.utils import secure_filename
from config import Config


def allowed_file(filename):
    """
    Checks whether uploaded file is a PDF.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def generate_unique_filename(filename):
    """
    Creates unique filename to avoid overwriting files.
    """
    safe_name = secure_filename(filename)
    unique_id = uuid.uuid4().hex
    return f"{unique_id}_{safe_name}"


def ensure_upload_folder_exists():
    """
    Creates upload folder if it does not exist.
    """
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)