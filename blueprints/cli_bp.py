from flask import Blueprint
from setup import db, bcrypt
from models.company import Company
from models.user import User
from models.internship import Internship
from datetime import date

# Declaring the blueprint
db_commands = Blueprint("db", __name__)

# Cli command to drop (delete) and create all tables
@db_commands.cli.command("create")
def db_create():

    # Drop table
    db.drop_all()

    # Create table
    db.create_all()

    # Printing Created Tables to ensure everything has worked as intended
    print("Dropped and Created Tables")


# Cli command to seed the database with users, companies, and internships
@db_commands.cli.command("seed")
def db_seed():
    # Creating users for the database
    users = [
        User(
            name = "Callan",
            email = "blissfulquiet@hotmail.com",
            password = bcrypt.generate_password_hash("spam").decode("utf-8"),
            is_admin = True
        ),
        User(
            name ="John",
            email ="john@spam.com",
            password = bcrypt.generate_password_hash("tisbutascratch").decode("utf-8"),
            is_admin = False
        )

    ]

    # Adding and commiting all the users to the database
    db.session.add_all(users)
    db.session.commit()

    # Creating companies for the database
    companies = [
    Company(
        name = "Meta",
        email = "meta@example.com",
        password = bcrypt.generate_password_hash("spam").decode("utf-8"),
        ph_number = "0412345679",
    ),
    Company(
        name = "Zyrtex LTD",
        email = "zyrtex@gmail.com",
        password = bcrypt.generate_password_hash("spam").decode("utf-8"),
        ph_number = "0412345678",
    ),
    Company(
        name = "Reddit",
        email = "reddit@reddit.com",
        password = bcrypt.generate_password_hash("spam").decode("utf-8"),
        ph_number = "0412345677",
    )
    ]
    
    
    # Adding and commiting all the companies to the database
    db.session.add_all(companies)
    db.session.commit()
    
    # Creating internships for the database
    internships = [
        Internship(
            status = "Company Interested",
            date_created = date.today(),
            position_type = "Front-end",
            user_id = 1,
            company_id = 1
        ),
        Internship(
            status = "Student Interview Pending",
            date_created = date.today(),
            position_type = "Front-end",
            user_id = 1,
            company_id = 1
        ),
        Internship(
            status = "Student Declined Interview",
            date_created = date.today(),
            position_type = "Front-end",
            user_id = 1,
            company_id = 1
        ),
    ]

    # Adding and commiting all internships to the database
    db.session.add_all(internships)
    db.session.commit()

    # Printing Database Seeded to ensure everything has worked as intended
    print("Database Seeded")