import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
print(os.getenv("SECRET_KEY"))
print(os.getenv('SQLALCHEMY_DATABASE_URI'))

from app import view
from app import database