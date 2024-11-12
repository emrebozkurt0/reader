from flask import render_template, request
from .models import fetch_data, insert_data, execute_query_from_file
from ..app import app

@app.route('/')
def get_users():
    return "First view"
