from flask import Blueprint, request
from models.internship import Internship, InternshipSchema
from setup import db
from flask_jwt_extended import jwt_required
from auth import authorize

# Declaring a Blueprint and setting url_prefix
internships_bp = Blueprint("internships", __name__, url_prefix="/internships")

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
    

# #Update an internship Route
@internships_bp.route("/<int:internship_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_internship(internship_id):
    internship_info = InternshipSchema(exclude=["id", "date_created"]).load(request.json)
    stmt = db.select(Internship).filter_by(id=internship_id)
    internship = db.session.scalar(stmt)
    if internship:
        authorize(internship_id)
        internship.position_type = internship_info.get("position_type", internship.position_type)
        internship.status = internship_info.get("status", internship.status)
        db.session.commit()
        return InternshipSchema().dump(internship), 200
    else:
        return {"error": "internship not found"}, 404

# # Delete an internship Route
# @internships_bp.route("/<int:internships_id>", methods=["DELETE"])
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
#         return {"error": "User not found"}, 404