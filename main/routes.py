from flask import render_template, request
from app import app

@app.route('/')
def get_users():
    return render_template("home.html")
