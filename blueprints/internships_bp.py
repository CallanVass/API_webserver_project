from flask import Blueprint, request
from models.internship import Internship, InternshipSchema
from setup import db
from flask_jwt_extended import jwt_required
from auth import authorize
from email_sending import send_email
from sqlalchemy.exc import IntegrityError


# Declaring a Blueprint and setting url_prefix
internships_bp = Blueprint("internships", __name__, url_prefix="/internships")

# Create an internship
@internships_bp.route("/", methods=["POST"])
@jwt_required()
def create_internship():
    try:
        internship_info = InternshipSchema(only=["status", "position_type", "user_id",
                                                "company_id"]).load(request.json)
        
        # Check if an internship with the same details already exists in the database
        existing_internship = Internship.query.filter_by(
            status=internship_info["status"],
            position_type=internship_info["position_type"],
            user_id=internship_info["user_id"],
            company_id=internship_info["company_id"]
        ).first()
        # .first() returns the first result found or None if no result is found
        if existing_internship:
            return {"error": "An internship with the same details already exists"}, 400
        
        internship = Internship(
            status = internship_info["status"],
            position_type = internship_info["position_type"],
            user_id = internship_info["user_id"],
            company_id = internship_info["company_id"],
            )
        db.session.add(internship)
        db.session.commit()
        return InternshipSchema().dump(internship), 201
    except IntegrityError:
        return {"error": "Company id or user id doesn't exist"}, 404



# Get all internships Route
@internships_bp.route("/")
@jwt_required()  # Specifying you need a jwt access token to access page
def all_users():
    authorize() # Admin only
    stmt = db.select(Internship)
    internship = db.session.scalars(stmt).all()
    return InternshipSchema(many=True).dump(internship)


# Get one internship Route
@internships_bp.route("/<int:internships_id>")
@jwt_required()
def get_user(internships_id):
    authorize()
    stmt = db.select(Internship).filter_by(id=internships_id)
    user = db.session.scalar(stmt)
    if user:
        print(user)
        return InternshipSchema().dump(user)
    else:
        return {"error": "internship not found"}, 404
    

# Update an internship Route
@internships_bp.route("/<int:internship_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_internship(internship_id):
    internship_info = InternshipSchema(exclude=["id", "date_created"]).load(request.json)
    stmt = db.select(Internship).filter_by(id=internship_id)
    internship = db.session.scalar(stmt)
    if internship:
        user_email = internship.users.email
        user_name = internship.users.name
        authorize(internship_id)
        internship.position_type = internship_info.get("position_type", internship.position_type)
        internship.status = internship_info.get("status", internship.status)
        db.session.commit()
        send_email(user_email, user_name)
        return InternshipSchema().dump(internship), 200
    else:
        return {"error": "internship not found"}, 404

# Delete an internship Route
@internships_bp.route("/<int:internship_id>", methods=["DELETE"])
@jwt_required()
def delete_internship(internship_id):
    stmt = db.select(Internship).filter_by(id=internship_id)
    internship = db.session.scalar(stmt)
    if internship:
        authorize(internship_id)
        db.session.delete(internship)
        db.session.commit()
        return {"message": "Internship deleted successfully"}, 200
    else:
        return {"error": "Internship not found"}, 404