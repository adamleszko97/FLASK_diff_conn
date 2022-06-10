from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import users
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get("password")

        user = users.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash('Logged in successfully!')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
