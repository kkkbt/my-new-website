# import os
#
# from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
# db = SQLAlchemy(app)
# print(os.getenv("SECRET_KEY"))
# print(os.getenv('SQLALCHEMY_DATABASE_URI'))

from app import app
from app import db


# # CREATE TABLE
# class ProfileDatabase(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     kind = db.Column(db.String(250), nullable=False)
#     title = db.Column(db.String(250), nullable=False)
#     staff = db.Column(db.String(250), unique=True, nullable=True)
#     link_title = db.Column(db.String(250), unique=True, nullable=True)
#     link_url = db.Column(db.String(250), unique=True, nullable=True)
#
#
# ##CREATE TABLE
# class ApplicationDatabase(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     description = db.Column(db.String(250), nullable=False)
#
#
# ##CREATE TABLE
# class LibraryDatabase(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     link_title = db.Column(db.String(250), nullable=False)
#     link_url = db.Column(db.String(250), nullable=False)
#     description = db.Column(db.String(250), nullable=False)
#
#
# ##CREATE TABLE
# class BiographyDatabase(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(250), unique=True, nullable=False)
#     time = db.Column(db.String(250), nullable=False)
#     place = db.Column(db.String(250), nullable=False)
#     member = db.Column(db.String(250), nullable=False)
#     link_title = db.Column(db.String(250), nullable=False)
#     link_url = db.Column(db.String(250), nullable=False)
#     description = db.Column(db.String(250), nullable=False)
#
#
# def databases_to_send(database_name: list, databases_data: list) -> dict:
#     all_databases = {}
#     for dn, dd in zip(database_name, databases_data):
#         try:
#             columns = db.session.query(dd).all()[0].__dict__
#             del columns["_sa_instance_state"], columns["id"]
#             columns = list(columns.keys())
#             columns.sort(reverse=True)
#         except IndexError:
#             columns = []
#         all_databases[dn] = [db.session.query(dd).all(), columns]
#     return all_databases
#
#
# @app.route('/')
# def home():
#     contents = ["profile", "application", "library", "biography", "investment", "contact"]
#     return render_template("index.html", contents=contents)
#
#
# @app.route("/application")
# def application():
#     database_name = ["application"]
#     database_data = [ApplicationDatabase]
#     database = databases_to_send(database_name, database_data)
#     return render_template("application.html", title='application', database=database)
#
#
# @app.route("/library")
# def library():
#     return render_template("library.html", title='library')
#
#
# @app.route("/biography")
# def biography():
#     return render_template("biography.html", title='biography')
#
#
# @app.route("/profile")
# def profile():
#     #
#     # try:
#     #     columns = db.session.query(ApplicationDatabase).all()[0].__dict__
#     #     del columns["_sa_instance_state"], columns["id"]
#     #     columns = list(columns.keys())
#     #     columns.sort(reverse=True)
#     # except IndexError:
#     #     columns = []
#     # all_databases[dn] = [db.session.query(dd).all(), columns]
#
#     return render_template("profile.html", title='profile')
#
#
# @app.route("/investment")
# def investment():
#     return render_template("investment.html", title='investment')
#
#
# @app.route("/contact")
# def contact():
#     return render_template("contact.html", title='contact')
#
#
# @app.route("/setting", methods=["GET", "POST", "DELETE"])
# def setting():
#     database_name = ["profile", "application", "library", "biography"]
#     databases_data = [ProfileDatabase, ApplicationDatabase, LibraryDatabase, BiographyDatabase]
#     all_databases = databases_to_send(database_name, databases_data)
#     return render_template("setting.html", title='setting', databases=all_databases)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
