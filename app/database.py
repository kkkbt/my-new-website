from app import db
from flask_login import UserMixin


class UserDatabase(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(50), unique=True)
    columns = ["name", "password"]


class SecretDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    staff = db.Column(db.String(50), nullable=False)
    examples = db.Column(db.String(1000), nullable=False)

    columns = ["kind", "title", "staff", "examples"]


class ProfileDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    staff = db.Column(db.String(50), nullable=False)
    examples = db.Column(db.String(50), nullable=False)

    columns = ["kind", "title", "staff", "examples"]


class PortfolioDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.String(50), nullable=True)
    link_title = db.Column(db.String(50), nullable=True)
    link_url = db.Column(db.String(1000), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    img = db.Column(db.String(50), nullable=False)

    columns = ["kind", "title", "date", "link_title", "link_url", "description", "img"]


class LibraryDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    link_title = db.Column(db.String(50), nullable=False)
    link_url = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(1000), nullable=True)

    columns = ["kind", "title", "link_title", "link_url", "description"]


class BiographyDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.String(50), nullable=True)
    place = db.Column(db.String(50), nullable=True)
    member = db.Column(db.String(50), nullable=True)
    link_title = db.Column(db.String(50), nullable=True)
    link_url = db.Column(db.String(1000), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    img = db.Column(db.String(50), nullable=False)

    columns = ["kind", "title", "date", "place", "member", "link_title", "link_url", "description", "img"]


class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.String(50), nullable=True)
    place = db.Column(db.String(50), nullable=True)
    member = db.Column(db.String(50), nullable=True)
    link_title = db.Column(db.String(50), nullable=True)
    link_url = db.Column(db.String(1000), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    img = db.Column(db.String(50), nullable=False)

db.create_all()
