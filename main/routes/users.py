from flask import Blueprint, render_template, request, redirect, url_for,flash
from main.classes.users import Users
from main.utils.get_data import get_table_data, get_join_data
from main.utils.database import get_connection
from main.utils.decorators import login_required

users_bp = Blueprint('users', __name__)

@users_bp.route("/users")
@login_required
def users():
    sort_column = request.args.get("sort", default=None)
    current_order = request.args.get("order", default="asc")
    next_order = "desc" if current_order == "asc" else ("unsorted" if current_order == "desc" else "asc")
    try:
        join_query = """
            SELECT 
                u.user_id, 
                u.name, 
                u.email, 
                u.username, 
                u.date_of_birth, 
                u.gender, 
                s.subscription_plan, 
                u.role
            FROM 
                Users u
            LEFT JOIN 
                Subscriptions s
            ON 
                u.subscription_id = s.subscription_id
        """
        
        if sort_column and current_order != "unsorted":
            sort_column = f"{sort_column} {current_order.upper()}"

        users = get_join_data(join_query, sort_column)
        
        return render_template(
            "/crud/users/users.html",
            users=users,
            sort_column=sort_column,
            current_order=current_order,
            next_order=next_order,
        )
    except Exception as e:
        return f"Error occurred while fetching the users: {e}", 500

@users_bp.route("/users/add", methods=["GET", "POST"])
@login_required
def add_user():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "username": request.form["username"],
            "date_of_birth": request.form["date_of_birth"],
            "gender": request.form["gender"],
            "subscription_id": request.form["subscription_id"],
            "role": request.form["role"]
        }
        try:
            connection = get_connection()
            user = Users(connection)
            user.add(data)
            flash("User added successfully.","success")
            return redirect(url_for("users.users"))
        except Exception as e:
            return f"Error occurred while adding the user: {e}", 500
    return render_template("/crud/users/add_user.html")

@users_bp.route("/users/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_user(id):
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "username": request.form["username"],
            "date_of_birth": request.form["date_of_birth"],
            "gender": request.form["gender"],
            "subscription_id": request.form["subscription_id"],
            "role": request.form["role"]
        }
        try:
            connection = get_connection()
            user = Users(connection)
            user.update(data, id)
            flash("User updated successfully.","success")
            return redirect(url_for("users.users"))
        except Exception as e:
            return f"Error occurred while updating the user: {e}", 500
    else:
        try:
            connection = get_connection()
            user = Users(connection)
            user_data = user.get_by_id(id)
            subscriptions = get_table_data("Subscriptions")
            return render_template("/crud/users/update_user.html", user=user_data, subscriptions=subscriptions)
        except Exception as e:
            return f"Error occurred while fetching the user data: {e}", 500


@users_bp.route("/users/delete/<int:id>", methods=["POST"])
@login_required
def delete_user(id):
    try:
        connection = get_connection()
        user = Users(connection)
        user.delete(id)
        flash("User deleted successfully.","success")
        return redirect(url_for("users.users"))
    except Exception as e:
        return f"Error occurred while deleting the user: {e}", 500

users_bp.route("/users/search", methods=["GET", "POST"])
@login_required
def search_users():
    if request.method == "POST":
        filters = {
            "author_id": request.form.get("author_id"),
            "author_name": request.form.get("author_name"),
            "gender": request.form.get("gender"),
            "about": request.form.get("about"),
            "image_url": request.form.get("image_url"),
            "country_id": request.form.get("country_id"),
        }

        try:
            connection = get_connection()
            user = Users(connection)
            results = user.search(filters)
            flash(f"{len(results)} results found.", "success" if results else "warning")
            return render_template(
                "/crud/users/users.html",
                users=results,
                sort_column=None,
                current_order=None,
                next_order=None,
            )
        except Exception as e:
            return f"Error occurred while searching for users: {e}", 500

    return redirect(url_for("users.users"))

@users_bp.route("/users/top_100_users")
@login_required
def top_users():
    try:
        connection = get_connection()
        comment = Users(connection)
        top_users = comment.get_top_users(limit=100)
        
        return render_template(
            "/crud/users/top_100_users.html",
            top_users=top_users
        )
    except Exception as e:
        return f"Error occurred while fetching the top 100 users: {e}", 500