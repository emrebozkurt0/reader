from flask import Blueprint, render_template, request, redirect, url_for
from main.classes.books import Books
from main.utils.get_data import *
from main.utils.database import get_connection

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
            connection = get_connection()
            book = Books(connection)
            book.add(data)
            return redirect(url_for("books.books"))
        except Exception as e:
            return f"Error occurred while adding the book: {e}", 500
    return render_template("/crud/books/add_book.html")

@books_bp.route("/books/update/<int:id>", methods=["GET", "POST"])
def update_book(id):
    if request.method == "POST":
        data = {
            "isbn": request.form["isbn"],
            "title": request.form["title"],
            "author_id": request.form["author_id"],
            "publication_year": request.form["publication_year"],
            "publisher_id": request.form["publisher_id"],
        }
        try:
            connection = get_connection()
            book = Books(connection)
            book.update(data,id)
            return redirect(url_for("books.books"))
        except Exception as e:
            return f"Error occurred while updating the book: {e}", 500
    else:
        try:
            connection = get_connection()
            book = Books(connection)
            book_data = book.get_by_id(id)
            return render_template("/crud/books/update_book.html", book=book_data)
        except Exception as e:
            return f"Error occurred while fetching the book data: {e}", 500

@books_bp.route("/books/delete/<int:id>", methods=["POST"])
def delete_book(id):
    try:
        connection = get_connection()
        book = Books(connection)
        book.delete(id)
        return redirect(url_for("books.books"))
    except Exception as e:
        return f"Error occurred while deleting the book: {e}", 500