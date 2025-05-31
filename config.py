import os

# Your Google Cloud API Key
API_KEY = "AIzaSyDJSdM-u47flu1t2rH_9ugwWUaHnTjB_ds"

LANGUAGES = {
    "hi": "Hindi",
    "or": "Odia",
    "bn": "Bengali"
}

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change')
    UPLOAD_FOLDER = os.path.join('static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
