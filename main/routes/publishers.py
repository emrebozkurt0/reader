from flask import Blueprint, render_template, request, redirect, url_for
from main.classes.publishers import Publishers
from main.utils.get_data import get_table_data
from main.utils.database import get_connection

publishers_bp = Blueprint('publishers', __name__)

@publishers_bp.route("/publishers")
def publishers():
    publishers = get_table_data("Publishers")
    return render_template("/crud/publishers/publishers.html", publishers=publishers)

@publishers_bp.route("/publishers/add", methods=["GET", "POST"])
def add_publisher():
    if request.method == "POST":
        data = {
            "publisher_name": request.form["name"],
        }
        try:
            connection = get_connection()
            publisher = Publishers(connection)
            publisher.add(data)
            return redirect(url_for("publishers.publishers"))
        except Exception as e:
            return f"Error occurred while adding the publisher: {e}", 500
    return render_template("/crud/publishers/add_publisher.html")
