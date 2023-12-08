from setup import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf
from datetime import datetime

VALID_STATUSES = ("Company Interested", "Student Interview Pending" , "Student Declined Interview", "Company Offered Position", "Student Accepted Offer", "Student Declined Offer", "Student Offered Employment", "Student Completed Internship")
VALID_POSITIONS = ("Front-end", "Back-end", "Full-stack")

# Create User Model
class Internship(db.Model):

    # Name the table
    __tablename__ = "internships"

    # Primary Key 
    id = db.Column(db.Integer, primary_key=True)

    # Table Entities
    status = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date(), default=datetime.now().strftime("%Y-%m-%d"))
    position_type = db.Column(db.String, nullable=False)

    # Foreign Keys (user_id & company_id)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # db.relationship defines a relationship between User and Internship
    users = db.relationship("User", back_populates="internships")

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    # db.relationship defines a relationship between User and Company
    companies = db.relationship("Company", back_populates="internships")

class InternshipSchema(ma.Schema):

    # Nesting Schema under Internship upon serialization 
    users = fields.Nested("UserSchema", only=["id", "name"])
    companies = fields.Nested("CompanySchema", only=["id", "name"])
    status = fields.String(validate=OneOf(VALID_STATUSES))
    position_type = fields.String(validate=OneOf(VALID_POSITIONS))

    # Pass in accepted fields to the schema (for (de)serialization)
    class Meta:
        fields = ("id", "status", "date_created", "position_type", "companies", "users")