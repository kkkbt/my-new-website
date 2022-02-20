import ast

from werkzeug.security import check_password_hash

from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, current_user, logout_user

from app import app
from app import login_manager
from app.database import UserDatabase
from app.database_manager import initialize_user_database, create_columns, create_dict, get_current_data, \
    add, edit, delete
from app.email import send_email


@login_manager.user_loader
def load_user(user_id):
    return UserDatabase.query.get(int(user_id))


@app.route('/')
def home():
    logout_user()
    contents = ["profile", "portfolio", "library", "biography", "investment", "contact"]
    return render_template("index.html", contents=contents)


@app.route("/profile")
def profile():
    title = 'profile'
    data = create_dict(title)
    print(data)

    return render_template("contents.html", title=title, data=data, img=False)


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


@app.route("/investment")
def investment():
    return render_template("investment.html", title='investment')


@app.route("/biography")
def biography():
    title = 'biography'
    data = create_dict(title)

    return render_template("contents.html", title=title, data=data, img=True)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        nickname = request.form.get('nickname')
        email_subject = request.form.get('email_subject')
        email_content = request.form.get('email_content')
        send_email(nickname, email_subject, email_content)

        return redirect(url_for('contact'))

    return render_template("contact.html", title='contact')


@app.route("/login-setting", methods=["GET", "POST"])
def login_setting():
    if current_user.is_authenticated:
        return redirect(url_for('setting'))

    initialize_user_database()

    if request.method == "POST":
        name = request.form.get('name')
        user = UserDatabase.query.filter_by(name=name).first()

        password = request.form.get('password')
        hashed_password = user.password
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login_setting'))
        if not check_password_hash(hashed_password, password):
            flash("login失敗")

            return redirect(url_for('login_setting'))

        else:
            login_user(user)
            return redirect(url_for('setting'))
    explantion = "管理者用ページにログインします。"
    return render_template("login.html", title="login", explanation=explantion)


@app.route("/setting")
@login_required
def setting():
    current_data = get_current_data()
    columns = create_columns()

    return render_template("setting.html", title='setting', databases=current_data, columns=columns)


@app.route("/setting/add/<string:obj>", methods=["GET", "POST"])
@app.route("/setting/add/<string:obj>/<string:kind>", methods=["GET", "POST"])
@app.route("/setting/add/<string:obj>/<string:kind>/<string:title>", methods=["GET", "POST"])
@app.route("/setting/add/<string:obj>/<string:kind>/<string:title>/<string:staff>", methods=["GET", "POST"])
@login_required
def setting_add(obj, kind: str = "", title: str = "", staff: str = ""):
    if request.method == "POST":
        add(obj, kind, title, staff)

        return redirect(url_for('setting'))


@app.route("/setting/edit/<string:obj>", methods=["POST"])
@app.route("/setting/edit/<string:obj>/<string:name>", methods=["POST"])
@login_required
def setting_edit(obj, name=""):
    db_id_to_edit = request.args.get('id')
    edit(obj, db_id_to_edit, name)

    return redirect(url_for('setting'))


@app.route("/setting/delete/<string:obj>", methods=["GET", "DELETE"])
@login_required
def setting_delete(obj):
    which_db_to_delete = request.args.get('which_db_to_delete')
    which_db_to_delete = ast.literal_eval(which_db_to_delete)
    delete(obj, which_db_to_delete)

    return redirect(url_for('setting'))


@app.route("/login-secret-page", methods=["GET", "POST"])
def login_secret():
    if current_user.is_authenticated:
        return redirect(url_for('secret'))

    initialize_user_database()

    if request.method == "POST":
        name = request.form.get('name')
        user = UserDatabase.query.filter_by(name=name).first()

        password = request.form.get('password')
        hashed_password = user.password
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login_secret'))
        if not check_password_hash(hashed_password, password):
            flash("login失敗")

            return redirect(url_for('login_secret'))

        else:
            login_user(user)
            return redirect(url_for('setting'))
    explantion = "ユーザー専用ページにログインします。"
    return render_template("login.html", title='login', explanation=explantion)


@app.route("/secret")
@login_required
def secret():
    title = 'secret'
    data = create_dict(title)

    return render_template("contents.html", title=title, data=data, img=False)
    # return render_template("contents.html", title='secret')
