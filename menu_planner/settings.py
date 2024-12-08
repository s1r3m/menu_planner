import os

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')

# DB.
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://menu_planner:menu_planner@localhost/menu_planner')

# Flask.
SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
