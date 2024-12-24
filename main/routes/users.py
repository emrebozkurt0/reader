from flask import Blueprint, render_template, request, redirect, url_for
from main.classes.users import Users
from main.utils.get_data import get_table_data
from main.utils.database import get_connection
from main.utils.decorators import login_required

users_bp = Blueprint('users', __name__)

@users_bp.route("/users")
@login_required
def users():
    users = get_table_data("Users")
    subscriptions = get_table_data("Subscriptions")
    return render_template("/crud/users/users.html", users=users, subscriptions=subscriptions)

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
        }
        try:
            connection = get_connection()
            user = Users(connection)
            user.add(data)
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
        }
        try:
            connection = get_connection()
            user = Users(connection)
            user.update(data, id)
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
        return redirect(url_for("users.users"))
    except Exception as e:
        return f"Error occurred while deleting the user: {e}", 500
