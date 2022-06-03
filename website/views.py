from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import employees
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():


    if request.method == 'POST':
        name_form = request.form.get('name_search')

        if(len(name_form) > 2):
            result = employees.query.filter(employees.name.contains(name_form)).order_by(employees.id).all()
            
            if result:
                flash('Users found!')

            else:
                flash('Users not found', category='error')  

        else:
            flash('Please provide more than 2 characters', category='error')
        
        
    return render_template("search.html", user=current_user)

