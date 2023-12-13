from flask import Blueprint, request
from models.user import User, UserSchema
from setup import bcrypt, db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from auth import authorize
from marshmallow import ValidationError

# Declaring a Blueprint and setting url_prefix
users_bp = Blueprint("users", __name__, url_prefix="/users")

# Register route
@users_bp.route("/register", methods=["POST"])
@jwt_required() # JSON Web Token must be provided for verification
def register():
    authorize() # Admin only
    try:
        # Parse incoming POST body through the User schema 
        # (excludes id and is_admin to ensure users can't make themselves admin)
        user_info = UserSchema(exclude=["id", "is_admin"]).load(request.json)
        # Create a new user with the parsed data
        user = User(
            email=user_info["email"],
            
            # Ensure password is hashed upon receival
            password=bcrypt.generate_password_hash(user_info["password"]).decode(
                "utf8"
            ),
            name=user_info.get("name", ""),
        )

        # Add and commit the new user to the database
        db.session.add(user)
        db.session.commit()

        # Return the new user (exludes password)
        return UserSchema(exclude=["password"]).dump(user), 201
    # Error handling for emails already in use
    except IntegrityError:
        return {"error": "Email address already in use"}, 409

# Login Route
@users_bp.route("/login", methods=["POST"])
def login():

    # Parse incoming POST body through the schema
    user_info = UserSchema(exclude=["id", "name", "is_admin"]).load(request.json)

    # Select user with email that matches the one in the POST body
    # Check the password hash matches
    stmt = db.select(User).where(User.email == user_info["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, user_info["password"]):
        # Create a JWT token
        token = create_access_token(
            identity=user.id, expires_delta=timedelta(hours=5)
        ) 
        # Return token to the client
        return {
            "token": token,
            "user": UserSchema(exclude=["password", "internships"]).dump(user),
        }
    else:
        return {"error": "Invalid email or password"}, 401


# Get all users Route
@users_bp.route("/")
@jwt_required() # JSON Web Token must be provided for verification
def all_users():
    try:
        authorize() # Admin only
        # Select all users
        stmt = db.select(User)
        users = db.session.scalars(stmt).all()
        # Return all the users, excluding their hashed passwords
        return UserSchema(many=True, exclude=["password"]).dump(users)
    except:
        return {"error": "You do not have the required permissions to access this page"}, 401


# Get one user Route
@users_bp.route("/<int:user_id>")
@jwt_required() # JSON Web Token must be provided for verification
def get_user(user_id):
    authorize() # Admin only
    # Select a user via user id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        # If the user exists, return them via dump
        print(user)
        return UserSchema(exclude=["password"]).dump(user)
    # Else, return error message
    else:
        return {"error": "user not found"}, 404
    

#Update a user Route
@users_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required() # JSON Web Token must be provided for verification
def update_user(user_id):
    # Parse incoming POST body through the schema
    user_info = UserSchema(exclude=["id", "date_created"]).load(request.json)
    # Select a user via user id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        # If the user exists, accept these fields from the POST body
        # If no value is passed, retain original value
        authorize(user.user_id)
        user.title = user_info.get("title", user.title)
        user.description = user_info.get("description", user.description)
        user.status = user_info.get("status", user.status)
        # Commit new details to the database
        db.session.commit()
        return UserSchema().dump(user), 200
    else:
        # If the user_id doesn't match a user, return an error
        return {"error": "user not found"}, 404
    

# Update company password
@users_bp.route("/update-password/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required() # JSON Web Token must be provided for verification
def update_user_password(user_id):
    try:
        # Parse incoming POST body through the schema, excluding all but password
        user_info = UserSchema(exclude=["id", "email",
                                            "name"]).load(request.json, partial=True)
        # Select user from db 
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)
        if user:
            authorize() # Admin only
            # If user exists, set old_password and check current-
            # -password (given password) hash matches existing password hash
            old_password = request.json.get("old_password")
            if old_password and bcrypt.check_password_hash(user.password, old_password):
                # If they match, pass the password parameter as new password
                new_password = user_info.get("password")
                if new_password:
                    # Hash the password and commit it
                    user.password = bcrypt.generate_password_hash(new_password).decode("utf8")
                    db.session.commit()
                    return {"success": "password reset successfully"}, 200
                
                else:
                    # If new password not provided, return error
                    return {"error": "New password not provided"}, 400
            else:
                # If old password doesn't match existing password, return error
                return {"error": "Old password incorrect"}, 400
        else:
            # If user cannot be found, return error
            return {"error": "user not found"}, 404
    # Error handling for password length
    except ValidationError:
        return {"error": "Password must be at least 8 characters in length"}, 409

# Delete a user Route
@users_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required() # JSON Web Token must be provided for verification
def delete_user(user_id):
    # Select user from db using user_id
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        # If user exists, delete and commit the change
        authorize() # Admin only
        db.session.delete(user)
        db.session.commit()
        # Return confirmation message
        return {"message": "User deleted successfully"}, 200
    else:
        # If user not found, return error
        return {"error": "user not found"}, 404