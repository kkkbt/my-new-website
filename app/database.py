from app import db
from flask_login import UserMixin


class UserDatabase(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(1000), unique=True)
    columns = ["name", "password"]


class ProfileDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    staff = db.Column(db.String(250), nullable=False)
    examples = db.Column(db.String(250), nullable=True)

    columns = ["kind", "title", "staff", "examples"]


class PortfolioDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=True)
    date = db.Column(db.String(250), nullable=True)
    link_title = db.Column(db.String(250), nullable=True)
    link_url = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    img = db.Column(db.String(250), nullable=True)

    columns = ["kind", "title", "date", "link_title", "link_url", "description", "img"]


class LibraryDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    link_title = db.Column(db.String(250), nullable=True)
    link_url = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)

    columns = ["kind", "title", "link_title", "link_url", "description"]


class BiographyDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    date = db.Column(db.String(250), nullable=True)
    place = db.Column(db.String(250), nullable=True)
    member = db.Column(db.String(250), nullable=True)
    link_title = db.Column(db.String(250), nullable=True)
    link_url = db.Column(db.String(250), nullable=True)
    description = db.Column(db.String(250), nullable=True)
    img = db.Column(db.String(250), nullable=True)

    columns = ["kind", "title", "date", "place", "member", "link_title", "link_url", "description", "img"]


db.create_all()
