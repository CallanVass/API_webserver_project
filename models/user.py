from setup import db, ma
from marshmallow import fields

# Create User Model
class User(db.Model):
    # Name the table
    __tablename__ = "users"
    # Primary Key 
    id = db.Column(db.Integer, primary_key=True)

    # Table Entities
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Other side of the relationship between Internship and Company
    internships = db.relationship("Internship", back_populates="users")


class UserSchema(ma.Schema):

    # Nesting Schema under Internship upon serialization 
    internships = fields.Nested("InternshipSchema", many=True)
    email = fields.Email(required=True)
    # old_password field is used when resetting user passwords
    old_password = fields.Raw()

    # Pass in accepted fields to the schema (for (de)serialization)
    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "internships", "old_password")