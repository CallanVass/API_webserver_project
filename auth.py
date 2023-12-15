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

def authorize_company(company_id=None, user_id=None):


        # Checking for user in header (decoded with jwt-get-identity) (Get email address)
    jwt_user_id = get_jwt_identity()

    # Check user email against the databasse
    user_stmt = db.select(User).where(User.id == jwt_user_id)

    # Get an instance of the model (stmt user model)
    user = db.session.scalar(user_stmt)

    # If it's not the case that the user is an admin or user_id is truthy and matches the token
    # i.e if user_id isn't passed in, they must be admin
    if not (user.is_admin or (user_id and jwt_user_id == user_id)):
        print("Stopped by user")
        abort(401)
    # Checking for company in header (decoded with jwt-get-identity) (Get company ID)
    jwt_company_id = get_jwt_identity()

    # Check company ID against the database
    stmt = db.select(Company).where(Company.id == jwt_company_id)

    # Get an instance of the model (stmt company model)
    company = db.session.scalar(stmt)
    # If it's not the case that the company is an admin or company_id is truthy and matches the token
    # i.e if company_id isn't passed in, they must be admin
    if company.is_admin:
        print("Stopped by company")
        abort(401)

# def company_not_allowed():
#     # Check user email against the databasse
#     user_stmt = db.select(User).where(User.id == User.id)

#     # Get an instance of the model (stmt user model)
#     user = db.session.scalar(user_stmt)
#     # jwt_company_id = get_jwt_identity()
#     stmt = db.select(Company).where(Company.id == Company.id)
#     company = db.session.scalar(stmt)
#     if company not in user:
#         print("Stopped by company")
#         abort(401)
#     # Query the database for a user
#     # If the the user isn't a company, abort

    # if (company.is_admin):
    #     print("Stopped by company")
    #     abort(401)
