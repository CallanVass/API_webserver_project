from setup import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp, Length, And

# Create Company Model
class Company(db.Model):

    # Name the table
    __tablename__ = "companies"

    # Primary Key 
    id = db.Column(db.Integer, primary_key=True)

    # Table Entities
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    ph_number = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=True)

    # Other side of the relationship between Internship and Company
    internships = db.relationship("Internship", back_populates="companies", cascade='all, delete-orphan')

class CompanySchema(ma.Schema):
    
    # Nesting Schema under Internship upon serialization 
    internships = fields.Nested("InternshipSchema", only=["id", "status", "position_type"], many=True)
    password = fields.String(validate=And(
        Length(min=8, error="Password must be 10 numbers in length")
    ))

    # old_password field is used when resetting company passwords
    old_password = fields.Raw()
    ph_number = fields.String(required=True, validate=And(
        Regexp("^[0-9]+$", error="Phone number must only contain numbers"),
        Length(max=10, min=10, error="Phone number must be 10 numbers in length")
    ))
    # Pass in accepted fields to the schema (for (de)serialization)
    class Meta:
        fields = ("id", "name", "email", "password", "ph_number", "is_admin", "internships", "old_password")