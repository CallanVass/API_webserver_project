from flask_jwt_extended import get_jwt_identity
from flask import abort
from models.user import User
from models.company import Company
from setup import db

def authorize(user_id=None):

    # Checking for user in header (decoded with jwt-get-identity) (Get email address)
    jwt_user_id = get_jwt_identity()

    # Check user email against the databasse
    stmt = db.select(User).where(User.id == jwt_user_id)

    # Get an instance of the model (stmt user model)
    user = db.session.scalar(stmt)

    # If it's not the case that the user is an admin or user_id is truthy and matches the token
    # i.e if user_id isn't passed in, they must be admin
    if not (user.is_admin or (user_id and jwt_user_id == user_id)):
        print("Stopped by user")
        abort(401)