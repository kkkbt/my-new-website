from app import db


#CREATE TABLE
class ProfileDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    staff = db.Column(db.String(250), unique=True, nullable=True)
    link_title = db.Column(db.String(250), unique=True, nullable=True)
    link_url = db.Column(db.String(250), unique=True, nullable=True)


##CREATE TABLE
class ApplicationDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)


##CREATE TABLE
class LibraryDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    link_title = db.Column(db.String(250), nullable=False)
    link_url = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)


##CREATE TABLE
class BiographyDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    time = db.Column(db.String(250), nullable=False)
    place = db.Column(db.String(250), nullable=False)
    member = db.Column(db.String(250), nullable=False)
    link_title = db.Column(db.String(250), nullable=False)
    link_url = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)
