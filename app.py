from datetime import timedelta

from dotenv import dotenv_values
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

env_values = dotenv_values()
app = Flask(__name__)

DOCUMENTATION_URL = '/api/docs'
DOCUMENTATION_PATH = '/static/swagger.json'

app.config['JWT_SECRET_KEY'] = env_values['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

import src.routes

def main():
    swagger_ui_blueprint = get_swaggerui_blueprint(
        DOCUMENTATION_URL,
        DOCUMENTATION_PATH,
        config={'app_name': "KIU API"}
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=DOCUMENTATION_URL)

    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
