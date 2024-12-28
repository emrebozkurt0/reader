from flask import Blueprint, render_template, request, redirect, url_for, session
import mysql.connector
from main.utils.config import db_host, db_user, db_password, db_name
import bcrypt
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    msg_type = ''  
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        try:
            connection = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                auth_plugin='mysql_native_password'
            )
            cursor = connection.cursor(dictionary=True)
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
            
            if user:
                if user['role'] != 1:  
                    msg = 'You do not have permission to log in!'
                    msg_type = 'danger'  
                elif bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    session['loggedin'] = True
                    session['id'] = user['user_id']
                    session['username'] = user['username']
                    session.permanent = True
                    return redirect(url_for('main.admin'))
                else:
                    msg = 'Incorrect username/password!'
                    msg_type = 'danger'  
            else:
                msg = 'User not found!'
                msg_type = 'danger'  
        except mysql.connector.Error as err:
            msg = f"Database error: {err}"
            msg_type = 'danger' 
    return render_template('login.html', msg=msg, msg_type=msg_type)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    msg_type = ''  
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        subscription_id = 1

        if len(password) < 8:
            msg = 'Password must be at least 8 characters long!'
            msg_type = 'danger'  
        elif not re.search(r'[A-Z]', password):
            msg = 'Password must contain at least one uppercase letter!'
            msg_type = 'danger' 
        elif not re.search(r'[a-z]', password):
            msg = 'Password must contain at least one lowercase letter!'
            msg_type = 'danger'  
        elif not re.search(r'\d', password):
            msg = 'Password must contain at least one digit!'
            msg_type = 'danger'  
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            msg = 'Password must contain at least one special character!'
            msg_type = 'danger'  
        else:
            try:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                connection = mysql.connector.connect(
                    host=db_host,
                    user=db_user,
                    password=db_password,
                    database=db_name,
                    auth_plugin='mysql_native_password'
                )
                cursor = connection.cursor(dictionary=True)
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                user = cursor.fetchone()

                if user:
                    msg = 'User already exists!'
                    msg_type = 'danger'  
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    msg = 'Invalid email address!'
                    msg_type = 'danger'  
                elif not re.match(r'[A-Za-z0-9]+', username):
                    msg = 'Username must contain only characters and numbers!'
                    msg_type = 'danger' 
                else:
                    cursor.execute(
                        'INSERT INTO users (name, username, password, email, subscription_id) VALUES (%s, %s, %s, %s, %s)',
                        (name, username, hashed_password, email, subscription_id)
                    )
                    connection.commit()
                    msg = 'You have successfully registered!'
                    msg_type = 'success' 
                    
            except mysql.connector.Error as err:
                msg = f"Database error: {err}"
                msg_type = 'danger'  
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
        msg_type = 'danger'  
    return render_template('register.html', msg=msg, msg_type=msg_type)
