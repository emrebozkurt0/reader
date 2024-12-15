from flask import Flask, session
from main.routes import register_routes
import os
from datetime import timedelta

app = Flask(__name__, template_folder="./main/templates", static_folder="./main/static", static_url_path="/static")

app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'fallback-key-for-development')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

@app.before_request
def refresh_session():
    if 'loggedin' in session:
        session.permanent = True

register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
