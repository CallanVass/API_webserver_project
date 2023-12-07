from setup import app
# Importing the blueprints from blueprints folder
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users_bp
# from blueprints.companies_bp import companies_bp
# from blueprints.internships_bp import internships_bp


# Registering the blueprints (which allow us to modularise clicommands and routes)
app.register_blueprint(db_commands)

app.register_blueprint(users_bp)

# app.register_blueprint(companies_bp)

# app.register_blueprint(internships_bp)

# Prints routes upon Flask startup
print(app.url_map)