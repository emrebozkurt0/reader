from flask import render_template, request
from app import app

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")