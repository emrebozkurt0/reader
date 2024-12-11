from flask import Blueprint, render_template, request, redirect, url_for
from main.classes.comments import Comments
from main.utils.get_data import get_table_data
from main.utils.database import get_connection

comments_bp = Blueprint('comments', __name__)

@comments_bp.route("/comments")
def comments():
    comments = get_table_data("Comments")
    return render_template("/crud/comments/comments.html", comments=comments)

@comments_bp.route("/comments/add", methods=["GET", "POST"])
def add_comment():
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
            comment.add(data)
            return redirect(url_for("comments.comments"))
        except Exception as e:
            return f"Error occurred while adding the comment: {e}", 500
    return render_template("/crud/comments/add_comment.html")
