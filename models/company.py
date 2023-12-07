from setup import db, ma
from marshmallow import fields

# Create User Model
class Company(db.Model):

    # Name the table
    __tablename__ = "companies"

    # Primary Key 
    id = db.Column(db.Integer, primary_key=True)

    # Table Entities
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    ph_number = db.Column(db.Integer)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=True)

    # Other side of the relationship between Internship and Company
    internships = db.relationship("Internship", back_populates="companies")

class CompanySchema(ma.Schema):

    # Nesting Schema under Internship upon serialization 
    internships = fields.Nested("InternshipSchema", only=["id", "status", "position_type"], many=True)
    # Pass in accepted fields to the schema (for (de)serialization)
    class Meta:
        fields = ("id", "name", "email", "password", "ph_number", "is_admin", "internships")