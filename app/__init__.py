import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Define the WSGI application object
app = Flask(__name__)
# CORS
CORS(app)
# Configurations
app.config.from_object('config')
app.static_url_path = app.config.get('STATIC_FOLDER')
app.static_folder = app.root_path + app.static_url_path

LOGGER = app.logger

LOGGER.info(f'static folder: {app.static_folder}')

app_files_folder = os.path.join(app.static_folder, 'files')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_test.controllers import mod_test as test_module
from app.mod_api.routes import mod_api as api_module
# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(test_module)

# register api
app.register_blueprint(api_module)
# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
