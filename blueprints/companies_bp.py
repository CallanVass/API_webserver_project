from flask import Blueprint, request
from models.company import Company, CompanySchema
from setup import bcrypt, db
from sqlalchemy.exc import IntegrityError, DataError
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from auth import authorize
from marshmallow import ValidationError



# Declaring a Blueprint and setting url_prefix
companies_bp = Blueprint("companies", __name__, url_prefix="/companies")

# Register route
@companies_bp.route("/register", methods=["POST"])
@jwt_required() # Specifying you need a jwt access token to access page
def register_company():
    authorize() # Admin only
    try:
        # Parse incoming POST body through the Company schema 
        # (excludes id and is_admin to ensure companies can't make themselves admin)
        company_info = CompanySchema(exclude=["id", "is_admin"]).load(request.json)
        # Create a new user with the parsed data
        company = Company(
            email=company_info["email"],
            
            # Ensure password is hashed upon receival
            password=bcrypt.generate_password_hash(company_info["password"]).decode(
                "utf8"
            ),
            name=company_info.get("name", ""),
            ph_number=company_info.get("ph_number")
        )

        # Add and commit the new user to the database
        db.session.add(company)
        db.session.commit()

        # Return the new user (exludes password)
        return CompanySchema(exclude=["password"]).dump(company), 201
    # Error handling for emails already in use
    except IntegrityError:
        return {"error": "Email address or phone number already in use"}, 409
    except DataError:
        return {"error": "Phone number already in user"}, 409
    except ValidationError:
        return {"error": "Phone number must be 10 numbers in length"}, 409



# # Login Route
@companies_bp.route("/login", methods=["POST"])
def company_login():

    # 1 Parse incoming POST body through the schema
    company_info = CompanySchema(exclude=["id", "name", "is_admin", "ph_number"]).load(request.json)

    # 2 Select user with email that matches the one in the POST body
    # 3 Check the password hash matches
    stmt = db.select(Company).where(Company.email == company_info["email"])
    company = db.session.scalar(stmt)
    if company and bcrypt.check_password_hash(company.password, company_info["password"]):
        # 4 Create a JWT token
        token = create_access_token(
            identity=company.id, expires_delta=timedelta(hours=5)
        ) 
        # 5 Return token to the client
        return {
            "token": token,
            "company": CompanySchema(exclude=["password", "internships", "id", "ph_number"]).dump(company),
        }
    # else:
    #     return {"error": "Invalid email or password"}, 401


# # Get all companies Route
# @companies_bp.route("/")
# @jwt_required()  # Specifying you need a jwt access token to access page
# def all_companies():
#     authorize() # Admin only
#     stmt = db.select(User)
#     companies = db.session.scalars(stmt).all()
#     return UserSchema(many=True, exclude=["password"]).dump(companies)


# # Get one user Route
# @companies_bp.route("/<int:user_id>")
# @jwt_required()
# def get_user(user_id):
#     authorize()
#     stmt = db.select(User).filter_by(id=user_id)
#     user = db.session.scalar(stmt)
#     if user:
#         print(user)
#         return UserSchema(exclude=["password"]).dump(user)
#     else:
#         return {"error": "user not found"}, 404
    

# #Update a user Route
# @companies_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
# @jwt_required()
# def update_user(user_id):
#     user_info = UserSchema(exclude=["id", "date_created"]).load(request.json)
#     stmt = db.select(User).filter_by(id=user_id)
#     user = db.session.scalar(stmt)
#     if user:
#         authorize(user.user_id)
#         user.title = user_info.get("title", user.title)
#         user.description = user_info.get("description", user.description)
#         user.status = user_info.get("status", user.status)
#         db.session.commit()
#         return UserSchema().dump(user), 200
#     else:
#         return {"error": "user not found"}, 404

# # Delete a user Route
# @companies_bp.route("/<int:user_id>", methods=["DELETE"])
# @jwt_required()
# def delete_user(user_id):
#     stmt = db.select(User).filter_by(id=user_id)
#     user = db.session.scalar(stmt)
#     if user:
#         authorize(user_id)
#         db.session.delete(user)
#         db.session.commit()
#         return {"message": "User deleted successfully"}, 200
#     else:
#         return {"error": "user not found"}, 404