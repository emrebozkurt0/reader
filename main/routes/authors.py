from flask import Blueprint, render_template, request, redirect, url_for,flash
from main.classes.authors import Authors
from main.utils.get_data import get_table_data
from main.utils.database import get_connection
from main.utils.decorators import login_required

authors_bp = Blueprint('authors', __name__)

@authors_bp.route("/authors")
@login_required
def authors():
    authors = get_table_data("Authors")
    countries = get_table_data("Countries")
    return render_template("/crud/authors/authors.html", authors=authors, countries=countries)

@authors_bp.route("/authors/add", methods=["GET", "POST"])
@login_required
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
            connection = get_connection()
            author = Authors(connection)
            author.add(data)
            flash("Author added successfully.","success")
            return redirect(url_for("authors.authors"))
        except Exception as e:
            return f"Error occurred while adding the author: {e}", 500
    return render_template("/crud/authors/add_author.html")

@authors_bp.route("/authors/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_author(id):
    if request.method == "POST":
        data = {
            "author_name": request.form["name"],
            "gender": request.form["gender"],
            "about": request.form["about"],
            "img_url": request.form["img_url"],
            "country_id": request.form["country_id"],
        }
        try:
            connection = get_connection()
            author = Authors(connection)
            author.update(id, data)
            flash("Authoer updated successfully.","success")
            return redirect(url_for("authors.authors"))
        except Exception as e:
            return f"Error occurred while updating the author: {e}", 500
    else:
        try:
            connection = get_connection()
            author = Authors(connection)
            author_data = author.get_by_id(id)
            return render_template("/crud/authors/update_author.html", author=author_data)
        except Exception as e:
            return f"Error occurred while fetching the author data: {e}", 500


@authors_bp.route("/authors/delete/<int:id>", methods=["POST"])
@login_required
def delete_author(id):
    try:
        connection = get_connection()
        author = Authors(connection)
        author.delete(id)
        flash("Author deleted successfully.","success")
        return redirect(url_for("authors.authors"))
    except Exception as e:
        return f"Error occurred while deleting the author: {e}", 500
