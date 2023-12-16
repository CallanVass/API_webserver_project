from flask import Blueprint, request
from models.internship import Internship, InternshipSchema
from models.company import Company
from setup import db
from flask_jwt_extended import jwt_required
from auth import authorize
from email_sending import send_email
from sqlalchemy.exc import IntegrityError


# Declaring a Blueprint and setting url_prefix
internships_bp = Blueprint("internships", __name__, url_prefix="/internships")

# Create an internship
@internships_bp.route("/", methods=["POST"])
@jwt_required() # JSON Web Token must be provided for verification
def create_internship():
    try:
        # Parse incoming POST body through the Internship schema 
        internship_info = InternshipSchema(only=["status", "position_type", "user_id",
                                                "company_id"]).load(request.json)
        
        # Check if an internship with the same details already exists in the database
        existing_internship = Internship.query.filter_by(
            status=internship_info["status"],
            position_type=internship_info["position_type"],
            user_id=internship_info["user_id"],
            company_id=internship_info["company_id"]
        ).first() # .first() returns the first result found or None if no result is found
        
        if existing_internship:
            # If an existing internship is found, return an error
            return {"error": "An internship with the same details already exists"}, 400
        # Align incoming POST body with required InternshipSchema parameters
        internship = Internship(
            status = internship_info["status"],
            position_type = internship_info["position_type"],
            user_id = internship_info["user_id"],
            company_id = internship_info["company_id"],
            )
        authorize(internship.id) # Admin and Company only
        # Add the internship and commit change to database
        db.session.add(internship)
        db.session.commit()
        # Return the newly created internship
        return InternshipSchema().dump(internship), 201
    except IntegrityError:
        # If internship isn't found, return error
        return {"error": "Internship id or user id doesn't exist"}, 404



# Get all internships Route
@internships_bp.route("/")
@jwt_required()  # JSON Web Token must be provided for verification
def all_internships():
    authorize() # Admin only
    stmt = db.select(Internship)
    internship = db.session.scalars(stmt).all()
    return InternshipSchema(many=True).dump(internship)


# Get one internship Route
@internships_bp.route("/<int:internships_id>")
@jwt_required() # JSON Web Token must be provided for verification
def get_user(internships_id):
    authorize() # Admin only
    # Select a single internship from the db
    stmt = db.select(Internship).filter_by(id=internships_id)
    internship = db.session.scalar(stmt)
    if internship:
        # If they exist, print them to the console and return them
        print(internship)
        return InternshipSchema().dump(internship)
    else:
        # If the internship does not exist, return an error
        return {"error": "internship not found"}, 404
    

# Update an internship Route
@internships_bp.route("/<int:internship_id>", methods=["PUT", "PATCH"])
@jwt_required() # JSON Web Token must be provided for verification
def update_internship(internship_id):
    # Parse incoming POST body through the Internship schema 
    internship_info = InternshipSchema(exclude=["id", "date_created"]).load(request.json)
    # Select an internship from the db
    stmt = db.select(Internship).filter_by(id=internship_id)
    internship = db.session.scalar(stmt)
    if internship:
        # Store variables to pass as parameters to the send_email function
        user_email = internship.users.email
        user_name = internship.users.name
        authorize() # Admin only
        # If the internship exists, accept these fields from the POST body
        internship.position_type = internship_info.get("position_type", internship.position_type)
        internship.status = internship_info.get("status", internship.status)
        # Commit changes to the database
        db.session.commit()
        # Send email using the send_email function
        send_email(user_email, user_name)
        # Return the internship
        return InternshipSchema().dump(internship), 200
    else:
        # If the internship isn't found, return an error
        return {"error": "internship not found"}, 404

# Delete an internship Route
@internships_bp.route("/<int:internship_id>", methods=["DELETE"])
@jwt_required() # JSON Web Token must be provided for verification
def delete_internship(internship_id):
    # Select a single internship from db using internship id
    stmt = db.select(Internship).filter_by(id=internship_id)
    internship = db.session.scalar(stmt)
    if internship:
        # If the internship exists, delete it and commit the change
        authorize() # Admin only
        db.session.delete(internship)
        db.session.commit()
        # Return successful message
        return {"message": "Internship deleted successfully"}, 200
    else:
        # If the internship does not exist, return an error
        return {"error": "Internship not found"}, 404