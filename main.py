import os


from dotenv import load_dotenv
from flask import Flask, render_template


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/application")
def application():
    return render_template("application.html")

@app.route("/library")
def library():
    return render_template("library.html")


@app.route("/biography")
def biography():
    return render_template("biography.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/investment")
def investment():
    return render_template("investment.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == '__main__':

    app.run(debug=True)
