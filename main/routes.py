from flask import render_template, request
from app import app
from main.utils.get_data import *

""" @app.route('/')
def home():
    return render_template("home.html") """


@app.route("/")
def admin():
    return render_template("admin.html")


@app.route("/books")
def books():
    books = get_table_data("Books")
    bookDetails = get_table_data("BookDetails")
    return render_template("/crud/books.html", books=books, bookDetails=bookDetails)


@app.route("/users")
def users():
    users = get_table_data("Users")
    subscriptions = get_table_data("Subscriptions")
    return render_template("/crud/users.html", users=users, subscriptions=subscriptions)


@app.route("/publishers")
def publishers():
    publishers = get_table_data("Publishers")
    return render_template("/crud/publishers.html", publishers=publishers)


@app.route("/authors")
def authors():
    authors = get_table_data("Authors")
    countries = get_table_data("Countries")
    return render_template("/crud/authors.html", authors=authors, countries=countries)


@app.route("/comments")
def comments():
    comments = get_table_data("Comments")
    return render_template("/crud/comments.html", comments=comments)