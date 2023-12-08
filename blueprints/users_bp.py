from flask import Blueprint, request
from models.user import User, UserSchema
from setup import bcrypt, db
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from auth import authorize

# Declaring a Blueprint and setting url_prefix
users_bp = Blueprint("users", __name__, url_prefix="/users")

# Register route
@users_bp.route("/register", methods=["POST"])
@jwt_required() # Specifying you need a jwt access token to access page
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

    # 1 Parse incoming POST body through the schema
    user_info = UserSchema(exclude=["id", "name", "is_admin"]).load(request.json)

    # 2 Select user with email that matches the one in the POST body
    # 3 Check the password hash matches
    stmt = db.select(User).where(User.email == user_info["email"])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, user_info["password"]):
        # 4 Create a JWT token
        token = create_access_token(
            identity=user.id, expires_delta=timedelta(hours=5)
        ) 
        # 5 Return token to the client
        return {
            "token": token,
            "user": UserSchema(exclude=["password", "internships"]).dump(user),
        }
    else:
        return {"error": "Invalid email or password"}, 401


# Get all users Route
@users_bp.route("/")
@jwt_required()  # Specifying you need a jwt access token to access page
def all_users():
    authorize() # Admin only
    stmt = db.select(User)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=["password"]).dump(users)


# Get one user Route
@users_bp.route("/<int:user_id>")
@jwt_required()
def get_user(user_id):
    authorize()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        print(user)
        return UserSchema(exclude=["password"]).dump(user)
    else:
        return {"error": "user not found"}, 404
    

#Update a user Route
@users_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_user(user_id):
    user_info = UserSchema(exclude=["id", "date_created"]).load(request.json)
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        authorize(user.user_id)
        user.title = user_info.get("title", user.title)
        user.description = user_info.get("description", user.description)
        user.status = user_info.get("status", user.status)
        db.session.commit()
        return UserSchema().dump(user), 200
    else:
        return {"error": "user not found"}, 404

# Delete a user Route
@users_bp.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        authorize(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
    else:
        return {"error": "user not found"}, 404