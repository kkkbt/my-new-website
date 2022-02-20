import os
from collections import defaultdict
from werkzeug.security import generate_password_hash

from flask import request

from app import db
from app.database import ProfileDatabase, PortfolioDatabase, LibraryDatabase, BiographyDatabase, UserDatabase, \
    SecretDatabase

databases = {
    "profile": ProfileDatabase,
    "portfolio": PortfolioDatabase,
    "library": LibraryDatabase,
    "biography": BiographyDatabase,
    "user": UserDatabase,
    "secret": SecretDatabase
}


def initialize_user_database():
    if db.session.query(UserDatabase).all():
        return

    name = os.environ.get("NAME")
    pw = os.environ.get("HASHED_PW")
    first_user = UserDatabase(password=pw, name=name)

    db.session.add(first_user)
    db.session.commit()
    return


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

    if obj == "profile" or obj == "secret":
        data = defaultdict(func_for_profile)
        for d in database:
            data[d.kind][d.title][d.staff].append((d.id, d.examples))

    elif obj == "portfolio":
        data = defaultdict(func_for_biography_portfolio)

        for d in database:
            data[d.kind][d.title]["id"] = d.id
            data[d.kind][d.title]["date"] = d.date
            data[d.kind][d.title]["link_title"] = d.link_title
            data[d.kind][d.title]["link_url"] = d.link_url
            data[d.kind][d.title]["description"] = d.description
            data[d.kind][d.title]["img"] = d.img

    elif obj == "library":
        data = defaultdict(func_for_library)
        for d in database:
            one_data = {"id": d.id, "link_title": d.link_title, "link_url": d.link_url,
                        "description": d.description}
            data[d.kind][d.title].append(one_data)

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

    elif obj == "user":
        data = {}
        for d in database:
            data[d.name] = d.id

    else:
        raise ValueError

    return data


def create_columns():
    return {database_name: databases[database_name].columns for database_name in databases}


def get_current_data():
    return {database_name: create_dict(database_name) for database_name in databases}


def add(obj, kind, title, staff):
    new_data = []
    new_datum = {}

    if obj == "user":
        new_datum["name"] = request.form["name"]
        password = generate_password_hash(request.form["password"])
        print(password)
        new_datum["password"] = password
        new_data.append(new_datum)
    else:
        # CREATE RECORD
        if not kind:
            new_datum["kind"] = request.form["kind"]
        else:
            new_datum["kind"] = kind

        if not title:
            new_datum["title"] = request.form["title"]
        else:
            new_datum["title"] = title

        if obj == "profile" or obj == "secret":
            if not staff:
                new_datum["staff"] = request.form["staff"]
            else:
                new_datum["staff"] = staff
            examples = request.form.getlist("examples")

            for example in examples:
                if example:
                    print(example)
                    new_datum["examples"] = example
                    new_data.append(new_datum.copy())
            print(new_data)

        elif obj == "portfolio":
            new_datum["date"] = request.form["date"]
            new_datum["link_title"] = request.form["link_title"]
            new_datum["link_url"] = request.form["link_url"]
            new_datum["description"] = request.form["description"]
            new_datum["img"] = request.form["img"]
            new_data.append(new_datum)

        elif obj == "library":  # library

            new_datum["link_title"] = request.form["link_title"]
            new_datum["link_url"] = request.form["link_url"]
            new_datum["description"] = request.form["description"]
            new_data.append(new_datum)

        elif obj == "biography":
            new_datum["date"] = request.form["date"]
            new_datum["place"] = request.form["place"]
            new_datum["member"] = request.form["member"]
            new_datum["link_title"] = request.form["link_title"]
            new_datum["link_url"] = request.form["link_url"]
            new_datum["description"] = request.form["description"]
            new_datum["img"] = request.form["img"]
            new_data.append(new_datum)

        else:
            raise ValueError

    for datum in new_data:
        new_db = databases[obj](**datum)
        db.session.add(new_db)
    db.session.commit()

    return


def edit(obj, db_id_to_edit, name):
    db_to_update = databases[obj].query.get(db_id_to_edit)

    if obj == "user":
        db_to_update.name = name
        password = generate_password_hash(request.form["password"])
        db_to_update.password = password
    else:
        if obj == "profile" or obj == "secret":
            staff = request.form["staff"]
            examples = request.form.getlist("examples")
            db_to_update.staff = staff
            db_to_update.examples = examples

        elif obj == "portfolio":
            db_to_update.date = request.form["date"]
            db_to_update.link_title = request.form["link_title"]
            db_to_update.link_url = request.form["link_url"]
            db_to_update.description = request.form["description"]
            db_to_update.img = request.form["img"]

        elif obj == "library":  # library
            db_to_update.link_title = request.form["link_title"]
            db_to_update.link_url = request.form["link_url"]
            db_to_update.description = request.form["description"]

        elif obj == "biography":
            db_to_update.date = request.form["date"]
            db_to_update.place = request.form["place"]
            db_to_update.member = request.form["member"]
            db_to_update.link_title = request.form["link_title"]
            db_to_update.link_url = request.form["link_url"]
            db_to_update.description = request.form["description"]
            db_to_update.img = request.form["img"]

        else:
            raise ValueError

        db_to_update.kind = request.form["kind"]
        db_to_update.title = request.form["title"]
    db.session.commit()
    return


def delete(obj, db_id_to_delete):
    db_to_delete = databases[obj].query.get(db_id_to_delete)

    db.session.delete(db_to_delete)
    db.session.commit()
