from flask import Flask

app = Flask(__name__, template_folder="./main/templates", static_folder="./main/static", static_url_path="/static")

from main.routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
