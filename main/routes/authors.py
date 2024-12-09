from flask import Blueprint, render_template, request, redirect, url_for
from main.utils.authors import Authors
from main.utils.get_data import get_table_data
import mysql.connector
from ..config import db_host, db_user, db_password

authors_bp = Blueprint('authors', __name__)

@authors_bp.route("/authors")
def authors():
    authors = get_table_data("Authors")
    countries = get_table_data("Countries")
    return render_template("/crud/authors/authors.html", authors=authors, countries=countries)

@authors_bp.route("/authors/add", methods=["GET", "POST"])
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
            return redirect(url_for("authors.authors"))
        except Exception as e:
            return f"Error occurred while adding the author: {e}", 500
    return render_template("/crud/authors/add_author.html")
