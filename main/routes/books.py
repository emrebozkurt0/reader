from flask import Blueprint, render_template, request, redirect, url_for,flash
from main.classes.books import Books
from main.classes.bookdetails import BookDetails
from main.utils.get_data import *
from main.utils.database import get_connection
from main.utils.decorators import login_required

books_bp = Blueprint('books', __name__)

@books_bp.route("/books")
@login_required
def books():
    sort_column = request.args.get("sort", default=None)
    current_order = request.args.get("order", default="asc")
    next_order = "desc" if current_order == "asc" else ("unsorted" if current_order == "desc" else "asc")

    try:
        connection = get_connection()
        if sort_column and current_order != "unsorted":
            books = get_table_data("Books", sort_column=f"{sort_column} {current_order.upper()}")
        else:
            books = get_table_data("Books")
        bookDetails = get_table_data("BookDetails")

        return render_template(
            "/crud/books/books.html",
            books=books,
            bookDetails=bookDetails,
            sort_column=sort_column,
            current_order=current_order,
            next_order=next_order,
        )
    except Exception as e:
        return f"Error occurred while fetching the books: {e}", 500

@books_bp.route("/books/detailed_books")
@login_required
def detailed_books():
    sort_column = request.args.get("sort", default=None)
    current_order = request.args.get("order", default="asc")
    next_order = "desc" if current_order == "asc" else ("unsorted" if current_order == "desc" else "asc")

    try:
        connection = get_connection()
        join_query = """
        SELECT 
            b.book_id, 
            b.title, 
            b.isbn, 
            b.publication_year, 
            p.publisher_name AS publisher_name, 
            a.author_name AS author_name, 
            bd.rating, 
            bd.language, 
            bd.page_number, 
            bd.counts_of_review
        FROM 
            Books b
        LEFT JOIN 
            BookDetails bd
        ON 
            b.book_id = bd.book_id
        LEFT JOIN 
            Publishers p
        ON 
            b.publisher_id = p.publisher_id
        LEFT JOIN 
            Authors a
        ON 
            b.author_id = a.author_id;
        """
        if sort_column and current_order != "unsorted":
            join_query += f" ORDER BY {sort_column} {current_order.upper()}"

        cursor = connection.cursor()
        cursor.execute(join_query)
        detailed_books = cursor.fetchall()
        cursor.close()

        return render_template(
            "/crud/books/detailed_books.html",
            detailed_books=detailed_books,
            sort_column=sort_column,
            current_order=current_order,
            next_order=next_order,
        )
    except Exception as e:
        return f"Error occurred while fetching the detailed books: {e}", 500



@books_bp.route("/books/add", methods=["GET", "POST"])
@login_required
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
            flash("Book added successfully.","success")
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
            flash("Book updated successfully.","success")
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

@books_bp.route("/books/details/<int:id>",methods=["GET"])
def get_details(id):
        try:
            connection = get_connection()
            details = BookDetails(connection)
            details_data = details.get_by_id(id)
            book = Books(connection)
            book_data = book.get_by_id(id)
            return render_template("/crud/books/book_details.html",details=details_data,book=book_data)
        except Exception as e:
            return f"Error occurred while fetching the book data: {e}", 500

@books_bp.route("/books/delete/<int:id>", methods=["POST"])
def delete_book(id):
    try:
        connection = get_connection()
        book = Books(connection)
        book.delete(id)
        flash("Book deleted successfully.","success")
        return redirect(url_for("books.books"))
    except Exception as e:
        return f"Error occurred while deleting the book: {e}", 500
    
@books_bp.route("/books/search", methods=["GET", "POST"])
@login_required
def search_books():
    if request.method == "POST":
        filters = {
            "book_id": request.form.get("book_id"),
            "isbn": request.form.get("isbn"),
            "title": request.form.get("title"),
            "author_id": request.form.get("author_id"),
            "publication_year": request.form.get("publication_year"),
            "publisher_id": request.form.get("publisher_id"),
        }

        try:
            connection = get_connection()
            book = Books(connection)
            results = book.search(filters)
            flash(f"{len(results)} results found.", "success" if results else "warning")
            return render_template(
                "/crud/books/books.html",
                books=results,
                sort_column=None,
                current_order=None,
                next_order=None,
            )
        except Exception as e:
            return f"Error occurred while searching for books: {e}", 500

    return redirect(url_for("books.books"))
