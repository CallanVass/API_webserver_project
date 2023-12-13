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
        # Create a new company with the parsed data
        company = Company(
            email=company_info["email"],
            
            # Ensure password is hashed upon receival
            password=bcrypt.generate_password_hash(company_info["password"]).decode(
                "utf8"
            ),
            name=company_info.get("name", ""),
            ph_number=company_info.get("ph_number")
        )

        # Add and commit the new company to the database
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



# Login Route
@companies_bp.route("/login", methods=["POST"])
def company_login():
    # Parse incoming POST body through the schema
    company_info = CompanySchema(exclude=["id", "name", "is_admin", 
                                          "ph_number", "old_password"]).load(request.json)
    # Select user with email that matches the one in the POST body
    # Check the password hash matches
    stmt = db.select(Company).where(Company.email == company_info["email"])
    company = db.session.scalar(stmt)
    if company and bcrypt.check_password_hash(company.password, company_info["password"]):
        # Create a JWT token
        token = create_access_token(
            identity=company.id, expires_delta=timedelta(hours=5)
        ) 
        # Return token to the client
        return {
            "token": token,
            "company": CompanySchema(exclude=["password", "internships", "id", "ph_number"]).dump(company),
        }
    else:
        # If password or email doesn't match existing db data, return an error
        return {"error": "Invalid email or password"}, 401


# Get all companies Route
@companies_bp.route("/")
@jwt_required()  # JSON Web Token must be provided for verification
def all_companies():
    authorize() # Admin only
    # Select all companies from the db
    stmt = db.select(Company)
    companies = db.session.scalars(stmt).all()
    # Return the companies without their passwords
    return CompanySchema(many=True, exclude=["password"]).dump(companies)


# Get all companies (without internships)
@companies_bp.route("/no-internships")
@jwt_required()  # JSON Web Token must be provided for verification
def all_companies_no_internship():
    authorize() # Admin only
    # Select all companies from the db
    stmt = db.select(Company)
    companies = db.session.scalars(stmt).all()
    # Return the companies without their internships or passwords
    return CompanySchema(many=True, exclude=["password", "internships"]).dump(companies)


# Get one company Route
@companies_bp.route("/<int:company_id>")
@jwt_required() # JSON Web Token must be provided for verification
def get_company(company_id):
    authorize() # Admin only
    # Select a single company from the db
    stmt = db.select(Company).filter_by(id=company_id)
    company = db.session.scalar(stmt)
    if company:
        print(company)
        # If said company exists, return it to the body
        return CompanySchema(exclude=["password"]).dump(company)
    else:
        # If the company doesn't exist, return an error
        return {"error": "company not found"}, 404
    

# Update a company Route
@companies_bp.route("/<int:company_id>", methods=["PUT", "PATCH"])
@jwt_required() # JSON Web Token must be provided for verification
def update_company(company_id):
    try:
        # Parse incoming POST body through the schema
        company_info = CompanySchema(exclude=["id", "password"]).load(request.json, partial=True)
        # Select a single company from the db
        stmt = db.select(Company).filter_by(id=company_id)
        company = db.session.scalar(stmt)
        if company:
            authorize() # Admin only
            # Align incoming POST body with required CompanySchema parameters
            company.name = company_info.get("name", company.name)
            company.email = company_info.get("email", company.email)
            company.ph_number = company_info.get("ph_number", company.ph_number)
            # Commit company change to database
            db.session.commit()
            # Return company information back to the body
            return CompanySchema(exclude=["password", "internships"]).dump(company), 200
        else:
            return {"error": "company not found"}, 404
    except ValidationError:
        return {"error": "Password must be changed via update-password route"}, 409
    

# Update company password
@companies_bp.route("/update-password/<int:company_id>", methods=["PUT", "PATCH"])
@jwt_required() # JSON Web Token must be provided for verification
def update_company_password(company_id):
    try:
        # Parse incoming POST body through the schema, excluding all but password
        company_info = CompanySchema(exclude=["id", "email", "ph_number",
                                            "name"]).load(request.json, partial=True)
        # Select company from db 
        stmt = db.select(Company).filter_by(id=company_id)
        company = db.session.scalar(stmt)
        if company:
            authorize() # Admin only
            # If company exists, set old_password and check current-
            # -password (given password) hash matches existing password hash
            old_password = request.json.get("old_password")
            if old_password and bcrypt.check_password_hash(company.password, old_password):
                # If they match, pass the password parameter as new password
                new_password = company_info.get("password")
                if new_password:
                    # Hash the password and commit it
                    company.password = bcrypt.generate_password_hash(new_password).decode("utf8")
                    db.session.commit()
                    return {"success": "password reset successfully"}, 200
                else:
                    # If new password not provided, return error
                    return {"error": "New password not provided"}, 400
            else:
                # If old password doesn't match existing password, return error
                return {"error": "Old password incorrect"}, 400
        else:
            # If company cannot be found, return error
            return {"error": "company not found"}, 404
    # Error handling for password length
    except ValidationError:
        return {"error": "Password must be at least 8 characters in length"}, 409

 


# Delete a company Route
# WARNING: Internships cannot exist without a company, and will be cascade deleted
# upon the deletion of a company
@companies_bp.route("/<int:company_id>", methods=["DELETE"])
@jwt_required() # JSON Web Token must be provided for verification
def delete_company(company_id):
    # Select a single company from the db
    stmt = db.select(Company).filter_by(id=company_id)
    company = db.session.scalar(stmt)
    if company:
        # If company exists, delete it and commit the change
        authorize() # Admin only
        db.session.delete(company)
        db.session.commit()
        # Return successful delete message
        return {"message": "Company deleted successfully"}, 200
    else:
        # If company doesn't exist, return an error
        return {"error": "company not found"}, 404