from setup import db, ma
from marshmallow import fields

# Create User Model
class Internship(db.Model):

    # Name the table
    __tablename__ = "internships"

    # Primary Key 
    id = db.Column(db.Integer, primary_key=True)

    # Table Entities
    status = db.Column(db.String, nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    position_type = db.Column(db.String, nullable=False)

    # Foreign Keys (user_id & company_id)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # db.relationship defines a relationship between User and Internship
    user = db.relationship("User", back_populates="internships")

    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    # db.relationship defines a relationship between User and Company
    company = db.relationship("Company", back_populates="comments")

class UserSchema(ma.Schema):

    # Nesting Schema under Internship upon serialization 
    user = fields.Nested("UserSchema", only=["id", "name"])
    company = fields.Nested("CompanySchema", only=["id", "name"])

    # Pass in accepted fields to the schema (for (de)serialization)
    class Meta:
        fields = ("id", "status", "date_created", "position_type")