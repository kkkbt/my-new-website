from flask import render_template

from app import app, db
from app.database import ApplicationDatabase, LibraryDatabase, BiographyDatabase, ProfileDatabase

contents = ["profile", "application", "library", "biography", "investment", "contact"]


def databases_to_send(database_name: list, databases_data: list) -> dict:
    all_databases = {}
    for dn, dd in zip(database_name, databases_data):
        try:
            columns = db.session.query(dd).all()[0].__dict__
            del columns["_sa_instance_state"], columns["id"]
            columns = list(columns.keys())
            columns.sort(reverse=True)
        except IndexError:
            columns = []
        all_databases[dn] = [db.session.query(dd).all(), columns]
    return all_databases


@app.route('/')
def home():
    return render_template("index.html", contents=contents)


@app.route("/application")
def application():
    database_name = ["application"]
    database_data = [ApplicationDatabase]
    database = databases_to_send(database_name, database_data)
    return render_template("application.html", title='application', database=database)


@app.route("/library")
def library():
    return render_template("library.html", title='library')


@app.route("/biography")
def biography():
    return render_template("biography.html", title='biography')


@app.route("/profile")
def profile():
    #
    # try:
    #     columns = db.session.query(ApplicationDatabase).all()[0].__dict__
    #     del columns["_sa_instance_state"], columns["id"]
    #     columns = list(columns.keys())
    #     columns.sort(reverse=True)
    # except IndexError:
    #     columns = []
    # all_databases[dn] = [db.session.query(dd).all(), columns]

    return render_template("profile.html", title='profile')


@app.route("/investment")
def investment():
    return render_template("investment.html", title='investment')


@app.route("/contact")
def contact():
    return render_template("contact.html", title='contact')


@app.route("/setting", methods=["GET", "POST", "DELETE"])
def setting():
    # database_name = ["profile", "application", "library", "biography"]
    # databases_data = [ProfileDatabase, ApplicationDatabase, LibraryDatabase, BiographyDatabase]
    # all_databases = databases_to_send(database_name, databases_data)
    # return render_template("setting.html", title='setting', databases=all_databases)
    return render_template("index.html", contents=contents)
