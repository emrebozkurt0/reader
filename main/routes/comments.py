from flask import Blueprint, render_template, request, redirect, url_for,flash
from main.classes.comments import Comments
from main.utils.get_data import get_table_data
from main.utils.database import get_connection
from main.utils.decorators import login_required
from datetime import datetime

comments_bp = Blueprint('comments', __name__)

@comments_bp.route("/comments")
@login_required
def comments():
    comments = get_table_data("Comments")
    return render_template("/crud/comments/comments.html", comments=comments)

@comments_bp.route("/comments/add", methods=["GET", "POST"])
@login_required
def add_comment():
    if request.method == "POST":
        data = {
            "user_id": request.form["user_id"],
            "book_id": request.form["book_id"],
            "content": request.form["content"],
            "score": request.form["score"],
            "comment_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:00"),
        }
        try:
            connection = get_connection()
            comment = Comments(connection)
            comment.add(data)
            flash("Comment added successfully.","success")
            return redirect(url_for("comments.comments"))
        except Exception as e:
            return f"Error occurred while adding the comment: {e}", 500
    return render_template("/crud/comments/add_comment.html")

@comments_bp.route("/comments/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_comment(id):
    if request.method == "POST":
        data = {
            "user_id": request.form["user_id"],
            "book_id": request.form["book_id"],
            "content": request.form["comment_text"],
            "score": request.form["score"],
        }
        try:
            connection = get_connection()
            comment = Comments(connection)
            comment.update(id, data)
            flash("Comment updated successfully.","success")
            return redirect(url_for("comments.comments"))
        except Exception as e:
            return f"Error occurred while updating the comment: {e}", 500
    else:
        try:
            connection = get_connection()
            comment = Comments(connection)
            comment_data = comment.get_by_id(id)
            return render_template("/crud/comments/update_comment.html", comment=comment_data)
        except Exception as e:
            return f"Error occurred while fetching the comment data: {e}", 500


@comments_bp.route("/comments/delete/<int:id>", methods=["POST"])
@login_required
def delete_comment(id):
    try:
        connection = get_connection()
        comment = Comments(connection)
        comment.delete(id)
        flash("Comment deleted successfully.","success")
        return redirect(url_for("comments.comments"))
    except Exception as e:
        return f"Error occurred while deleting the comment: {e}", 500

@comments_bp.route("/comments/search", methods=["GET", "POST"])
@login_required
def search_comments():
    if request.method == "POST":
        filters = {
            "comment_id": request.form.get("comment_id"),
            "book_id": request.form.get("book_id"),
            "comment_datetime": request.form.get("comment_datetime"),
            "user_id": request.form.get("user_id"),
            "content": request.form.get("content"),
            "score": request.form.get("score"),
        }

        try:
            connection = get_connection()
            comment = Comments(connection)
            results = comment.search(filters)
            flash(f"{len(results)} results found.", "success" if results else "warning")
            return render_template(
                "/crud/comments/comments.html",
                comments=results,
                sort_column=None,
                current_order=None,
                next_order=None,
            )
        except Exception as e:
            return f"Error occurred while searching for comments: {e}", 500

    return redirect(url_for("comments.comments"))
