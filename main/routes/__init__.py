from flask import Blueprint, render_template
from .books import books_bp
from .users import users_bp
from .publishers import publishers_bp
from .authors import authors_bp
from .comments import comments_bp

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def admin():
    return render_template("admin.html")

def register_routes(app):
    app.register_blueprint(books_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(publishers_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(main_bp)
