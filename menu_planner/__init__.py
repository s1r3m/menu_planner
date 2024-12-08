import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from extensions import db, login_manager

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_format = logging.Formatter("%(asctime)s %(levelname)s: %(filename)s -- %(message)s")

# Console Handler (StreamHandler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logger_format)
logger.addHandler(console_handler)

# # File Handler (RotatingFileHandler)
# if not (__name__ == '__main__'):
#     file_handler = RotatingFileHandler("logs/menu_planner.log", maxBytes=1_000_000, backupCount=5)
#     file_handler.setLevel(logging.DEBUG)
#     file_handler.setFormatter(logger_format)
#     logger.addHandler(file_handler)


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    # Initialize extensions.
    db.init_app(app)
    login_manager.init_app(app)

    # Setup LoginManager.
    login_manager.login_view = "routes.login"

    # Register blueprints or routes
    from routes import routes

    # from api.weeks import weeks_api
    app.register_blueprint(routes)

    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)

    # Log app start-up.
    app.logger.info('Flask application initialized!')

    return app


app = create_app()


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
