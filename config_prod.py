import os

class ProductionConfig:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-secret-key-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///nani_digitals.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join('static', 'images', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
