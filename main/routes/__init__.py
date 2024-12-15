from flask import Blueprint, render_template
from main.routes.books import books_bp
from main.routes.users import users_bp
from main.routes.publishers import publishers_bp
from main.routes.authors import authors_bp
from main.routes.comments import comments_bp
from main.routes.auth import auth_bp
from main.utils.decorators import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@login_required
def admin():
    return render_template("admin.html")

def register_routes(app):
    app.register_blueprint(books_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(publishers_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
