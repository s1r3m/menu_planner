from flask import Flask

from routes import routes
from api.weeks import weeks_api
from settings import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

app.register_blueprint(routes)
app.register_blueprint(weeks_api)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)
