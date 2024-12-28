from flask import Blueprint, render_template, request, redirect, url_for
from main.classes.publishers import Publishers
from main.utils.get_data import get_table_data
from main.utils.database import get_connection
from main.utils.decorators import login_required

publishers_bp = Blueprint("publishers", __name__)


@publishers_bp.route("/publishers")
@login_required
def publishers():
    sort_column = request.args.get("sort", default=None)
    current_order = request.args.get("order", default="asc")
    next_order = (
        "desc"
        if current_order == "asc"
        else ("unsorted" if current_order == "desc" else "asc")
    )
    try:
        connection = get_connection()
        if sort_column and current_order != "unsorted":
            publishers = get_table_data(
                "Publishers", sort_column=f"{sort_column} {current_order.upper()}"
            )
        else:
            publishers = get_table_data("Publishers")

        return render_template(
            "/crud/publishers/publishers.html",
            publishers=publishers,
            sort_column=sort_column,
            current_order=current_order,
            next_order=next_order,
        )
    except Exception as e:
        return f"Error occurred while fetching the publishers: {e}", 500


@publishers_bp.route("/publishers/add", methods=["GET", "POST"])
@login_required
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


@publishers_bp.route("/publishers/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_publisher(id):
    if request.method == "POST":
        data = {
            "publisher_name": request.form["name"],
        }
        try:
            connection = get_connection()
            publisher = Publishers(connection)
            publisher.update(data, id)
            return redirect(url_for("publishers.publishers"))
        except Exception as e:
            return f"Error occurred while updating the publisher: {e}", 500
    else:
        try:
            connection = get_connection()
            publisher = Publishers(connection)
            publisher_data = publisher.get_by_id(id)
            return render_template(
                "/crud/publishers/update_publisher.html", publisher=publisher_data
            )
        except Exception as e:
            return f"Error occurred while fetching the publisher data: {e}", 500


@publishers_bp.route("/publishers/delete/<int:id>", methods=["POST"])
@login_required
def delete_publisher(id):
    try:
        connection = get_connection()
        publisher = Publishers(connection)
        publisher.delete(id)
        return redirect(url_for("publishers.publishers"))
    except Exception as e:
        return f"Error occurred while deleting the publisher: {e}", 500
