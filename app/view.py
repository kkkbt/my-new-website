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


@login_manager.user_loader
def load_user(user_id):
    return UserDatabase.query.get(int(user_id))


def databases_to_send(databases: dict = databases) -> dict:
    all_databases = {}
    for database_name in databases:
        columns = databases[database_name].columns
        all_databases[database_name] = [db.session.query(databases[database_name]).all(), columns]
    return all_databases

    # return


def create_dict_for_biography():
    return defaultdict(dict)


def create_dict_for_library():
    return defaultdict(list)


def create_dict_for_profile():
    def create_dict_for_profile2():
        return defaultdict(list)

    return defaultdict(create_dict_for_profile2)


@app.route('/')
def home():
    return render_template("index.html", contents=contents)


@app.route("/portfolio")
def portfolio():
    # d1 = {"id": 0, "kind": "プログラミング言語", "title": "ラインボット", "link_title": "Qiita記事", "date": "2019-08",
    #       "link_url": "https://qiita.com/KKkbt/items/2796d2e0abb66adf3f1c", "description": "line bot作った",
    #       "img": "fav.jpg"}
    # d2 = {"id": 1, "kind": "マークアップ言語", "title": "ウェブサイト", "link_title": "Homepage URL", "date": "2019-08",
    #       "link_url": "http://kkkbt.sakura.ne.jp/index.html", "description": "二年前に作った。", "img": "older_webpage.jpg"}
    # ds = [d1, d2]

    data = defaultdict(create_dict_for_biography)
    portfolio_database = db.session.query(PortfolioDatabase).all()

    # for d in ds:
    #     data[d["kind"]][d["title"]]["id"] = d["id"]
    #     data[d["kind"]][d["title"]]["date"] = d["date"]
    #     data[d["kind"]][d["title"]]["link_title"] = d["link_title"]
    #     data[d["kind"]][d["title"]]["link_url"] = d["link_url"]
    #     data[d["kind"]][d["title"]]["description"] = d["description"]
    #     data[d["kind"]][d["title"]]["img"] = d["img"]

    for d in portfolio_database:
        data[d.kind][d.title]["id"] = d.id
        data[d.kind][d.title]["date"] = d.date
        data[d.kind][d.title]["link_title"] = d.link_title
        data[d.kind][d.title]["link_url"] = d.link_url
        data[d.kind][d.title]["description"] = d.description
        data[d.kind][d.title]["img"] = d.img

    return render_template("contents.html", title='portfolio', data=data, img=True)


@app.route("/library")
def library():
    # d3 = {"id": 0, "kind": "リンク集", "title": "株式投資", "link_title": "バフェット・コード",
    #       "link_url": "https://www.buffett-code.com/",
    #       "description": "財務諸表が簡単に調べられる。"}
    # d1 = {"id": 1, "kind": "リンク集", "title": "株式投資", "link_title": "バフェットの財務諸表を読む力",
    #       "link_url": "https://www.amazon.co.jp/%E5%8F%B2%E4%B8%8A%E6%9C%80%E5%BC%B7%E3%81%AE%E6%8A%95%E8%B3%87%E5%AE%B6-%E3%83%90%E3%83%95%E3%82%A7%E3%83%83%E3%83%88%E3%81%AE%E8%B2%A1%E5%8B%99%E8%AB%B8%E8%A1%A8%E3%82%92%E8%AA%AD%E3%82%80%E5%8A%9B-%E5%A4%A7%E4%B8%8D%E6%B3%81%E3%81%A7%E3%82%82%E6%8A%95%E8%B3%87%E3%81%A7%E5%8B%9D%E3%81%A1%E6%8A%9C%E3%81%8F58%E3%81%AE%E3%83%AB%E3%83%BC%E3%83%AB-%E3%83%A1%E3%82%A2%E3%83%AA%E3%83%BC%E3%83%BB%E3%83%90%E3%83%95%E3%82%A7%E3%83%83%E3%83%88/dp/4198627053/ref=sr_1_1?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=%E3%83%BB%E3%83%90%E3%83%95%E3%82%A7%E3%83%83%E3%83%88%E3%81%AE%E8%B2%A1%E5%8B%99%E8%AB%B8%E8%A1%A8%E3%82%92%E8%AA%AD%E3%82%80%E5%8A%9B&qid=1595497396&sr=8-1",
    #       "description": "財務諸表が読めるようになる"}
    # d2 = {"id": 2, "kind": "作成ファイル", "title": "英語", "link_title": "TOEFL_iBTについて",
    #       "link_url": "http://kkkbt.sakura.ne.jp/files/TOEFL_iBT.pdf", "description": "トーフルで100点を超えた時。"}
    # ds = [d1, d2, d3]

    data = defaultdict(create_dict_for_library)
    library_database = db.session.query(LibraryDatabase).all()

    for d in library_database:
        one_data = {"id": d.id, "link_title": d.link_title, "link_url": d.link_url,
                    "description": d.description}
        data[d.kind][d.title].append(one_data)

    # biography_database = db.session.query(LibraryDatabase).all()

    # for d in biography_database:
    #     data[d.kind][d.title]["date"] = d.date
    #     data[d.kind][d.title]["place"] = d.place
    #     data[d.kind][d.title]["member"] = d.member
    #     data[d.kind][d.title]["link_title"] = d.link_title
    #     data[d.kind][d.title]["link_url"] = d.link_url
    #     data[d.kind][d.title]["description"] = d.description
    #     data[d.kind][d.title]["img"] = d.img
    #
    #     for key in BiographyDatabase.columns[2:]:
    #         if not data[d.kind][d.title][key]:
    #             del data[d.kind][d.title][key]
    return render_template("contents.html", title='library', data=data, img=False)


@app.route("/biography")
def biography():
    # d1 = {
    #     "kind": "部活動",
    #     "title": "国分寺高校サッカー部",
    #     "date": "2015年4月-2017年10月",
    #     "member": "国分寺高校サッカー部員約100名",
    #     "description": "高校三年間を捧げた。",
    #     "place": "国分寺高校",
    #     "link_title": "",
    #     "link_url": "",
    #     "img": "soccer-club-highschool.jpg"
    #     }

    # d2 = {
    #     "kind": "部活動",
    #     "title": "Tokyo Tech.",
    #     "date": "2018年4月-2019年12月",
    #     "member": "東工大フットサル部約30名",
    #     "description": "諸事情で途中で退部した。",
    #     "place": "東京工業大学",
    #     "link_title": "",
    #     "link_url": "",
    #     "img": "futsal-club-uni.jpg"}
    # biography_database = [d1, d2]

    data = defaultdict(create_dict_for_biography)

    biography_database = db.session.query(BiographyDatabase).all()

    for d in biography_database:
        data[d.kind][d.title]["id"] = d.id
        data[d.kind][d.title]["date"] = d.date
        data[d.kind][d.title]["place"] = d.place
        data[d.kind][d.title]["member"] = d.member
        data[d.kind][d.title]["link_title"] = d.link_title
        data[d.kind][d.title]["link_url"] = d.link_url
        data[d.kind][d.title]["description"] = d.description
        data[d.kind][d.title]["img"] = d.img

        # for key in BiographyDatabase.columns[2:]:
        #     if not data[d.kind][d.title][key]:
        #         del data[d.kind][d.title][key]

    return render_template("contents.html", title='biography', data=data, img=True)


@app.route("/profile")
def profile():
    # d1 = {"kind": "基本情報", "title": "趣味", "staff": "スポーツ", "examples": "サッカー"}
    # d2 = {"kind": "基本情報", "title": "趣味", "staff": "漫画", "examples": "なると"}
    # d3 = {"kind": "基本情報", "title": "能力指標", "staff": "資格", "examples": "サッカー"}
    # d4 = {"kind": "基本情報", "title": "能力指標", "staff": "プログラミング言語", "examples": "Python"}
    # d5 = {"kind": "基本情報", "title": "趣味", "staff": "漫画", "examples": "ワンピース"}
    # ds = [d1, d2, d3, d4, d5]

    profile_database = db.session.query(ProfileDatabase).all()

    data = defaultdict(create_dict_for_profile)

    for d in profile_database:
        data[d.kind][d.title][d.staff].append(d.examples)

    return render_template("contents.html", title='profile', data=data, img=False)


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
    all_databases = databases_to_send()
    return render_template("setting.html", title='setting', databases=all_databases)
    # return render_template("index.html", contents=contents)


@app.route("/setting/add/<string:obj>", methods=["GET", "POST"])
@login_required
def setting_add(obj):
    if request.method == "POST":
        # CREATE RECORD

        if obj == "profile":
            new_db = ProfileDatabase(
                kind=request.form["kind"],
                title=request.form["title"],
                staff=request.form["staff"],
                examples=request.form["examples"]
            )
        elif obj == "biography":
            new_db = BiographyDatabase(
                kind=request.form["kind"],
                title=request.form["title"],
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
                kind=request.form["kind"],
                title=request.form["title"],
                date=request.form["date"],
                link_title=request.form["link_title"],
                link_url=request.form["link_url"],
                description=request.form["description"],
                img=request.form["img"]
            )
        else:  # library
            new_db = LibraryDatabase(
                kind=request.form["kind"],
                title=request.form["title"],
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
