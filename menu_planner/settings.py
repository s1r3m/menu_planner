import os


DATABASE_URL = os.environ.get('DATABASE_URL')

SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
