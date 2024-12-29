from flask import Blueprint, render_template, request, redirect, url_for, flash
from main.classes.authors import Authors
from main.utils.get_data import get_table_data, get_join_data
from main.utils.database import get_connection
from main.utils.decorators import login_required

authors_bp = Blueprint('authors', __name__)

@authors_bp.route("/authors")
@login_required
def authors():
    sort_column = request.args.get("sort", default=None)
    current_order = request.args.get("order", default="asc")
    next_order = "desc" if current_order == "asc" else ("unsorted" if current_order == "desc" else "asc")

    try:
        connection = get_connection()

        join_query = """
            SELECT 
                a.author_id, 
                a.author_name, 
                a.gender, 
                a.about, 
                a.img_url, 
                c.country_name
            FROM 
                Authors a
            LEFT JOIN 
                Countries c
            ON 
                a.country_id = c.country_id
        """

        if sort_column and current_order != "unsorted":
            sort_column = f"{sort_column} {current_order.upper()}"

        authors = get_join_data(join_query, sort_column)

        return render_template(
            "/crud/authors/authors.html",
            authors=authors,
            sort_column=sort_column,
            current_order=current_order,
            next_order=next_order,
        )
    except Exception as e:
        return f"Error occurred while fetching the authors: {e}", 500

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
        return redirect(url_for("authors.authors"))
    except Exception as e:
        return f"Error occurred while deleting the author: {e}", 500

@authors_bp.route("/authors/search", methods=["GET", "POST"])
@login_required
def search_authors():
    if request.method == "POST":
        filters = {
            "author_id": request.form.get("author_id"),
            "author_name": request.form.get("author_name"),
            "gender": request.form.get("gender"),
            "about": request.form.get("about"),
            "image_url": request.form.get("image_url"),
            "country_name": request.form.get("country_name"),
        }

        try:
            connection = get_connection()

            join_query = """
                SELECT 
                    a.author_id, 
                    a.author_name, 
                    a.gender, 
                    a.about, 
                    a.img_url, 
                    c.country_name
                FROM 
                    Authors a
                LEFT JOIN 
                    Countries c
                ON 
                    a.country_id = c.country_id
            """

            filter_conditions = []
            if filters.get("author_id"):
                filter_conditions.append(f"a.author_id = {filters['author_id']}")
            if filters.get("author_name"):
                filter_conditions.append(f"a.author_name LIKE '%{filters['author_name']}%'")
            if filters.get("gender"):
                filter_conditions.append(f"a.gender LIKE '%{filters['gender']}%'")
            if filters.get("about"):
                filter_conditions.append(f"a.about LIKE '%{filters['about']}%'")
            if filters.get("image_url"):
                filter_conditions.append(f"a.img_url LIKE '%{filters['image_url']}%'")
            if filters.get("country_name"):
                filter_conditions.append(f"c.country_name LIKE '%{filters['country_name']}%'")

            if filter_conditions:
                join_query += " WHERE " + " AND ".join(filter_conditions)

            authors = get_join_data(join_query)

            flash(f"{len(authors)} results found.", "success" if authors else "warning")
            return render_template(
                "/crud/authors/authors.html",
                authors=authors,
                sort_column=None,
                current_order=None,
                next_order=None,
            )
        except Exception as e:
            return f"Error occurred while searching for authors: {e}", 500

    return redirect(url_for("authors.authors"))

@authors_bp.route("/authors/top_100_authors")
@login_required
def top_authors():
    try:
        connection = get_connection()
        comment = Authors(connection)
        top_authors = comment.get_top_authors(limit=100)
        
        return render_template(
            "/crud/authors/top_100_authors.html",
            top_authors=top_authors
        )
    except Exception as e:
        return f"Error occurred while fetching the top 100 authors: {e}", 500