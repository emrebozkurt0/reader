from flask import render_template, request
from app import app

""" @app.route('/')
def home():
    return render_template("home.html") """


@app.route("/")
def admin():
    return render_template("admin.html")


@app.route("/books")
def books():
    return render_template("/crud/books.html")


@app.route("/users")
def users():
    return render_template("/crud/users.html")


@app.route("/publishers")
def publishers():
    return render_template("/crud/publishers.html")


@app.route("/authors")
def authors():
    return render_template("/crud/authors.html")
