from datetime import timedelta

from dotenv import dotenv_values
from flask import Flask
from flask_jwt_extended import JWTManager


env_values = dotenv_values()
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = env_values['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager(app)

import src.routes

def main():
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()
