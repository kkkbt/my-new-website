from collections import defaultdict
# from datetime import date
import os
from werkzeug.security import check_password_hash

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user

from app import app
from app import db
from app import login_manager
from app.database import UserDatabase, PortfolioDatabase, LibraryDatabase, BiographyDatabase, ProfileDatabase, \
    initialize_user_database

contents = ["profile", "portfolio", "library", "biography", "investment", "contact"]

databases = {
    "profile": ProfileDatabase,
    "portfolio": PortfolioDatabase,
    "library": LibraryDatabase,
    "biography": BiographyDatabase
}


def create_columns():
    return {database_name: databases[database_name].columns for database_name in databases}


@login_manager.user_loader
def load_user(user_id):
    return UserDatabase.query.get(int(user_id))


def create_dict(obj):
    def func_for_library():
        return defaultdict(list)

    def func_for_biography_portfolio():
        return defaultdict(dict)

    def func_for_profile():
        def func_for_profile2():
            return defaultdict(list)

        return defaultdict(func_for_profile2)

    database = db.session.query(databases[obj]).all()

    if obj == "library":
        data = defaultdict(func_for_library)
        for d in database:
            one_data = {"id": d.id, "link_title": d.link_title, "link_url": d.link_url,
                        "description": d.description}
            data[d.kind][d.title].append(one_data)
    elif obj == "portfolio":
        data = defaultdict(func_for_biography_portfolio)

        for d in database:
            data[d.kind][d.title]["id"] = d.id
            data[d.kind][d.title]["date"] = d.date
            data[d.kind][d.title]["link_title"] = d.link_title
            data[d.kind][d.title]["link_url"] = d.link_url
            data[d.kind][d.title]["description"] = d.description
            data[d.kind][d.title]["img"] = d.img

    elif obj == "biography":
        data = defaultdict(func_for_biography_portfolio)

        for d in database:
            data[d.kind][d.title]["id"] = d.id
            data[d.kind][d.title]["date"] = d.date
            data[d.kind][d.title]["place"] = d.place
            data[d.kind][d.title]["member"] = d.member
            data[d.kind][d.title]["link_title"] = d.link_title
            data[d.kind][d.title]["link_url"] = d.link_url
            data[d.kind][d.title]["description"] = d.description
            data[d.kind][d.title]["img"] = d.img

    else:  # profile
        data = defaultdict(func_for_profile)
        for d in database:
            data[d.kind][d.title][d.staff].append((d.id, d.examples))

    return data


@app.route('/')
def home():
    return render_template("index.html", contents=contents)


@app.route("/portfolio")
def portfolio():
    title = 'portfolio'
    data = create_dict(title)

    return render_template("contents.html", title=title, data=data, img=True)


@app.route("/library")
def library():
    title = 'library'
    data = create_dict(title)

    return render_template("contents.html", title=title, data=data, img=False)


@app.route("/biography")
def biography():
    title = 'biography'
    data = create_dict(title)

    return render_template("contents.html", title=title, data=data, img=True)


@app.route("/profile")
def profile():
    title = 'profile'
    data = create_dict(title)

    return render_template("contents.html", title=title, data=data, img=False)


@app.route("/investment")
def investment():
    return render_template("investment.html", title='investment')


@app.route("/contact")
def contact():
    return render_template("contact.html", title='contact')


@app.route("/login-setting", methods=["GET", "POST"])
def login():
    initialize_user_database()

    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        hashed_password = os.getenv("HASHED_PW")
        user = UserDatabase.query.filter_by(name=name).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        if not check_password_hash(hashed_password, password):
            flash("login失敗")

            return redirect(url_for('login'))

        else:
            login_user(user)
            return redirect(url_for('setting'))
    return render_template("login.html", title='login')


@app.route("/setting")
@login_required
def setting():
    current_data = {database_name: create_dict(database_name) for database_name in databases}
    columns = create_columns()
    for i in ['library', 'profile']:
        print(current_data[i])
        print(columns[i])
    return render_template("setting.html", title='setting', databases=current_data, columns=columns)
    # return render_template("index.html", contents=contents)


@app.route("/setting/add/<string:obj>", methods=["GET", "POST"])
@app.route("/setting/add/<string:obj>/<string:kind>", methods=["GET", "POST"])
@app.route("/setting/add/<string:obj>/<string:kind>/<string:title>", methods=["GET", "POST"])
@app.route("/setting/add/<string:obj>/<string:kind>/<string:title>/<string:staff>", methods=["GET", "POST"])
@login_required
def setting_add(obj, kind: str = "", title: str = "", staff: str = ""):
    if request.method == "POST":
        # CREATE RECORD
        if not kind:
            kind = request.form["kind"]
        if not title:
            title = request.form["title"]

        if obj == "profile":
            if not staff:
                staff = request.form["staff"]

            new_db = ProfileDatabase(
                kind=kind,
                title=title,
                staff=staff,
                examples=request.form["examples"]
            )
        elif obj == "biography":
            new_db = BiographyDatabase(
                kind=kind,
                title=title,
                date=request.form["date"],
                place=request.form["place"],
                member=request.form["member"],
                link_title=request.form["link_title"],
                link_url=request.form["link_url"],
                description=request.form["description"],
                img=request.form["img"]
            )
        elif obj == "portfolio":
            new_db = PortfolioDatabase(
                kind=kind,
                title=title,
                date=request.form["date"],
                link_title=request.form["link_title"],
                link_url=request.form["link_url"],
                description=request.form["description"],
                img=request.form["img"]
            )
        else:  # library
            new_db = LibraryDatabase(
                kind=kind,
                title=title,
                link_title=request.form["link_title"],
                link_url=request.form["link_url"],
                description=request.form["description"],
            )
        db.session.add(new_db)
        db.session.commit()
        return redirect(url_for('setting'))


@app.route("/setting/edit/<string:obj>", methods=["POST"])
@login_required
def setting_edit(obj):
    db_id_to_edit = request.args.get('id')

    if obj == "profile":
        db_to_update = ProfileDatabase.query.get(db_id_to_edit)
        db_to_update.staff = request.form["staff"]
        db_to_update.examples = request.form["examples"]

    elif obj == "biography":
        db_to_update = BiographyDatabase.query.get(db_id_to_edit)
        db_to_update.date = request.form["date"]
        db_to_update.place = request.form["place"]
        db_to_update.member = request.form["member"]
        db_to_update.link_title = request.form["link_title"]
        db_to_update.link_url = request.form["link_url"]
        db_to_update.description = request.form["description"]
        db_to_update.img = request.form["img"]

    elif obj == "portfolio":
        db_to_update = PortfolioDatabase.query.get(db_id_to_edit)
        db_to_update.date = request.form["date"]
        db_to_update.link_title = request.form["link_title"]
        db_to_update.link_url = request.form["link_url"]
        db_to_update.description = request.form["description"]
        db_to_update.img = request.form["img"]

    else:  # library
        db_to_update = LibraryDatabase.query.get(db_id_to_edit)
        db_to_update.link_title = request.form["link_title"]
        db_to_update.link_url = request.form["link_url"]
        db_to_update.description = request.form["description"]

    db_to_update.kind = request.form["kind"]
    db_to_update.title = request.form["title"]
    db.session.commit()
    return redirect(url_for('setting'))


@app.route("/setting/delete/<string:obj>", methods=["GET", "DELETE"])
@login_required
def setting_delete(obj):
    db_id_to_delete = request.args.get('id')

    db_to_delete = databases[obj].query.get(db_id_to_delete)

    db.session.delete(db_to_delete)
    db.session.commit()
    return redirect(url_for('setting'))
