import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'nani-digitals-dev-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'nani_digitals.db').replace('\\', '/')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    UPLOAD_FOLDER = os.path.join('static', 'images', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
