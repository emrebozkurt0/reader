from flask import render_template, request, redirect, url_for
from app import app

from main.utils.publishers import Publishers
from main.utils.books import Books
from main.utils.authors import Authors
from main.utils.users import Users
from main.utils.comments import Comments

from main.utils.get_data import *
import mysql.connector
from .config import db_host, db_password, db_user


@app.route("/")
def admin():
    return render_template("admin.html")


@app.route("/books")
def books():
    books = get_table_data("Books")
    bookDetails = get_table_data("BookDetails")
    return render_template(
        "/crud/books/books.html", books=books, bookDetails=bookDetails
    )
@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        data = {
            "isbn": request.form["isbn"],
            "title": request.form["title"],
            "author_id": request.form["author_id"],
            "publication_year": request.form["publication_year"],
            "publisher_id": request.form["publisher_id"],
        }
        try:
            connection = mysql.connector.connect(
                host=db_host, user=db_user, password=db_password, database="reader"
            )
            book = Books(connection)
            book.add(data)
            return redirect(url_for("books"))
        except Exception as e:
            return f"Error occurred while adding the book: {e}", 500
    return render_template("/crud/books/add_book.html")


@app.route("/users")
def users():
    users = get_table_data("Users")
    subscriptions = get_table_data("Subscriptions")
    return render_template(
        "/crud/users/users.html", users=users, subscriptions=subscriptions
    )
@app.route("/users/add", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "username": request.form["username"],
            "date_of_birth": request.form["date_of_birth"],
            "gender": request.form["gender"],
            "subscription_id": request.form["subscription_id"],
        }
        try:
            connection = mysql.connector.connect(
                host=db_host, user=db_user, password=db_password, database="reader"
            )
            user = Users(connection)
            user.add(data)
            return redirect(url_for("users"))
        except Exception as e:
            return f"Error occurred while adding the user: {e}", 500
    return render_template("/crud/users/add_user.html")


@app.route("/publishers")
def publishers():
    publishers = get_table_data("Publishers")
    return render_template("/crud/publishers/publishers.html", publishers=publishers)
@app.route("/publishers/add", methods=["GET", "POST"])
def add_publisher():
    if request.method == "POST":
        data = {
            "publisher_name": request.form["name"],
        }
        try:
            connection = mysql.connector.connect(
                host=db_host, user=db_user, password=db_password, database="reader"
            )
            publisher = Publishers(connection)
            publisher.add(data)
            return redirect(url_for("publishers"))
        except Exception as e:
            return f"Error occurred while adding the publisher: {e}", 500
    return render_template("/crud/publishers/add_publisher.html")


@app.route("/authors")
def authors():
    authors = get_table_data("Authors")
    countries = get_table_data("Countries")
    return render_template(
        "/crud/authors/authors.html", authors=authors, countries=countries
    )
@app.route("/authors/add", methods=["GET", "POST"])
def add_author():
    if request.method == "POST":
        data = {
            "author_name": request.form["name"],
            "gender": request.form["gender"],
            "about": request.form["about"],
            "img_url": request.form["img_url"],
            "country_id": request.form["country_id"],
        }
        try:
            connection = mysql.connector.connect(
                host=db_host, user=db_user, password=db_password, database="reader"
            )
            author = Authors(connection)
            author.add(data)
            return redirect(url_for("authors"))
        except Exception as e:
            return f"Error occurred while adding the author: {e}", 500
    return render_template("/crud/authors/add_author.html")


@app.route("/comments")
def comments():
    comments = get_table_data("Comments")
    return render_template("/crud/comments/comments.html", comments=comments)
@app.route("/comments/add", methods=["GET", "POST"])
def add_comment():
    if request.method == "POST":
        data = {
            "user_id": request.form["user_id"],
            "book_id": request.form["book_id"],
            "content": request.form["comment_text"],
            "score": request.form["score"],
        }
        try:
            connection = mysql.connector.connect(
                host=db_host, user=db_user, password=db_password, database="reader"
            )
            comment = Comments(connection)
            comment.add(data)
            return redirect(url_for("comments"))
        except Exception as e:
            return f"Error occurred while adding the comment: {e}", 500
    return render_template("/crud/comments/add_comment.html")
