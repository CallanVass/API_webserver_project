from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ
import logging

# Create instance of the Flask application
app = Flask(__name__)

# Logging the terminal output using the logging module (by configuring the root logger)
logging.basicConfig(level = logging.DEBUG, # This can also be INFO, WARNING, ERROR, or CRITICAL
                    format = "[%(levelname)s] - %(message)s",
                    handlers = [
                        
                        # Print to console using StreamHandler
                        logging.StreamHandler(),
                        
                        # Print to file of choice using FileHandler
                        logging.FileHandler("server_log.txt") # Ensure you change your-
                        # -server_log_sample.txt file name to match the FileHandler name
                    ])

# Use environ to retrieve variables from .env files (.flaskenv)
app.config["JWT_SECRET_KEY"] = environ.get("JWT_SECRET_KEY")

# Once more user environ to retrieve variable
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("CONNECTION_STRING")

# Pass instances of Flask app to the modules
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Global Error Handling

@app.errorhandler(401)
def unauthorized(err):
    return {"error": str(err)}, 401

@app.errorhandler(404)
def not_found(err): 
    return {'error': str(err)}, 404