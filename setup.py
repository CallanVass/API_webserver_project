from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ

# Create instance of the Flask application
app = Flask(__name__)

# Use environ to retrieve variables from .env files (.flaskenv)
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")

# Once more user environ to retrieve variable
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("CONNECTION_STRING")

# Pass instances of Flask app to the modules
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Error Handling