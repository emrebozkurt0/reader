from flask import Blueprint,render_template, request, redirect, url_for
from main.utils.books import Books
from main.utils.get_data import *
import mysql.connector
from ..config import db_host, db_password, db_user

books_bp = Blueprint('books', __name__)

@books_bp.route("/books")
def books():
    books = get_table_data("Books")
    bookDetails = get_table_data("BookDetails")
    return render_template("/crud/books/books.html", books=books, bookDetails=bookDetails)

@books_bp.route("/books/add", methods=["GET", "POST"])
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
            return redirect(url_for("books.books"))
        except Exception as e:
            return f"Error occurred while adding the book: {e}", 500
    return render_template("/crud/books/add_book.html")
