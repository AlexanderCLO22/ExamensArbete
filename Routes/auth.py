from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

authviews = Blueprint('authviews', __name__)

@authviews.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = current_app.mongodb_repository.find_user(username)
        
        if  user:
            if  check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('homeviews.home'))
        else:
            flash("Wrong username or password")
            return redirect(url_for('authviews.login'))
    
    return render_template("login.html", user=current_user)

@authviews.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homeviews.home'))

@authviews.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user = current_app.mongodb_repository.find_user(username)
        
        if user:
            flash("Username already exists", category='error')
            return redirect(url_for('authviews.signup'))
        elif len(username) < 3:
            flash("Username must be at least 3 characters", category='error')
            return redirect(url_for('authviews.signup'))
        elif password1 != password2:
            flash("Passwords don't match")
            return redirect(url_for('authviews.signup'))
        else:
            current_app.mongodb_repository.create_user(username=username, password=generate_password_hash(password1))
            return redirect(url_for('authviews.login'))
    
    return render_template("sign_up.html", user=current_user)