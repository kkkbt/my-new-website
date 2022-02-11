import os

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
print(os.getenv("SECRET_KEY"))


@app.route('/')
def home():
    contents = ["profile", "library", "biography", "investment", "contact"]
    return render_template("index.html", contents=contents)


@app.route("/application")
def application():
    return render_template("application.html", title='application')


@app.route("/library")
def library():
    return render_template("library.html", title='library')


@app.route("/biography")
def biography():
    return render_template("biography.html", title='biography')


@app.route("/profile")
def profile():
    return render_template("profile.html", title='profile')


@app.route("/investment")
def investment():
    return render_template("investment.html", title='investment')


@app.route("/contact")
def contact():
    return render_template("contact.html", title='contact')


if __name__ == '__main__':
    app.run(debug=True)
