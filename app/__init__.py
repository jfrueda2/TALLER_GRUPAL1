from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='plantillas')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@db:3306/producto_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes

with app.app_context():
    db.create_all()