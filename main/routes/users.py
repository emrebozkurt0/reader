from flask import Blueprint, render_template, request, redirect, url_for
from main.utils.users import Users
from main.utils.get_data import get_table_data
import mysql.connector
from ..config import db_host, db_user, db_password

users_bp = Blueprint('users', __name__)

@users_bp.route("/users")
def users():
    users = get_table_data("Users")
    subscriptions = get_table_data("Subscriptions")
    return render_template("/crud/users/users.html", users=users, subscriptions=subscriptions)

@users_bp.route("/users/add", methods=["GET", "POST"])
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
            return redirect(url_for("users.users"))
        except Exception as e:
            return f"Error occurred while adding the user: {e}", 500
    return render_template("/crud/users/add_user.html")
