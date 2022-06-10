from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from .models import employees
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    result=[]
    page = request.args.get('page', 1, type=int)

    if request.method == 'POST':
        name_form = request.form.get('name_search')

        if request.form.get('Search') == 'Search':
            name_form = request.form.get('name_search')

            if(len(name_form) > 2):
                result = employees.query.filter(employees.first_name.contains(name_form)).order_by(employees.id).paginate(page=page, per_page=20)
            
                if result:
                    flash('Users found!')

                else:
                    flash('Users not found', category='error')  

            else:
                flash('Please provide more than 2 characters', category='error')

        elif request.form.get('Search All') == 'Search All':
            flash('All employees listed')
            result = employees.query.order_by(employees.last_name.asc()).paginate(page=page, per_page=20)
    
    return render_template("search.html", user=current_user, rows=result)


@views.route('/add_employee', methods=['GET', 'POST'])
@login_required
def add_employee():

    # department_list = employees.query.with_entities(employees.department).distinct()
    # formated_deptlist = []

    raw_data = employees.query.with_entities(employees.department).distinct()
    department_list = [item[0] for item in raw_data]

    if request.method == 'POST':
        name_add = request.form.get('add_name')
        lastname_add = request.form.get('add_lastname')
        phonenumber_add = request.form.get('add_phonenumber')
        department_add = request.form.get('add_department')

        if(len(name_add) <= 2):
            flash("First name has to be at lest 2 characters long")

        elif (len(lastname_add) <=2 ):
            flash("Last name has to be at lest 2 characters long")
        
        elif (len(phonenumber_add) <= 6):
            flash("Phone has to be at lest 6 characters long")
        
        elif department_add == None:
           flash("Please choose Department", category='error')

        else:
            new_employee = employees(first_name=name_add, last_name=lastname_add, phone_number=phonenumber_add, department=department_add)
            db.session.add(new_employee)
            db.session.commit()
            flash('Employee Added!', category='success')

    return render_template("add_employee.html", dept_list=department_list,  user=current_user)

@views.route('/delete-employee', methods=['POST'])
def delete_employee():

    employee = json.loads(request.data)
    employeeId = employee['employeeId']
    employee = employees.query.filter_by(id=employeeId)
    if employee:
        employee.delete()
        db.session.commit()
        flash('Employee Deleted')
        return jsonify({})
    else:
        flash('user does not exist', category='error')
