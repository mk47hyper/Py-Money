from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required
from pymoney import db
from pymoney.models import Employee, Payment, SalaryPayment, HourlyPayment, CommissionPayment, SalaryCommissionPayment
from pymoney.employees.forms import EmployeeForm
from pymoney.employees.rates import SalaryR, HourlyR, SalcomR
from pymoney.employees.helper import SalaryControl, HourlyControl, CommissionControl, SalComControl

employees = Blueprint('employees', __name__)


@employees.route("/")
@employees.route("/home")
def list_employees():
    employees = Employee.query.order_by(Employee.id)
    return render_template('employee/employees_list.html', title='Employees', employees=employees)


@employees.route("/employee/new", methods=['GET', 'POST'])
@login_required
def new_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        employee = Employee(first=form.first.data,
                            last=form.last.data,
                            email=form.email.data,
                            phone=form.phone.data,
                            address=form.address.data,
                            contract=form.contract.data)
        db.session.add(employee)
        db.session.commit()
        flash('Employee added to the database!', 'success')
        return redirect(url_for('employees.list_employees'))
    return render_template('employee/add_employee.html', title='New Employee', form=form, legend='New Employee')

@employees.route("/employee/<int:employee_id>/update", methods=['GET', 'POST'])
@login_required
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm()
    if form.validate_on_submit():
        employee.first = form.first.data
        employee.last = form.last.data
        employee.email = form.email.data
        employee.phone = form.phone.data
        employee.address = form.address.data
        employee.contract = form.contract.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('employees.employee', employee_id=employee_id))
    elif request.method == 'GET':
         form.first.data = employee.first
         form.last.data = employee.last
         form.email.data = employee.email
         form.phone.data = employee.phone
         form.address.data = employee.address
         form.contract.data = employee.contract
    return render_template('employee/add_employee.html', title='Update Employee',
                           form=form, legend='Update Employee Record')


@employees.route("/employee/<int:employee_id>", methods=['GET', 'POST'])
def employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    fullname = f'{employee.first} {employee.last}'
    rate=0
    over=0
    if employee.contract == 'salary':
        form_template = 'employee/forms/salary_form.html'
        table_template = 'employee/tables/salary.html'
        payments = SalaryPayment.query.filter(SalaryPayment.employee_id == employee_id).all()
        rate = SalaryR().get_base()
        if request.method == "POST":
            form = SalaryControl(request=request)
            form.add_entry(employee_id=employee_id)
            return redirect(url_for('employees.employee', employee_id=employee_id))
    elif employee.contract == 'hourly':
        form_template = 'employee/forms/hourly_form.html'
        table_template = 'employee/tables/hourly.html'
        payments = HourlyPayment.query.filter(HourlyPayment.employee_id == employee_id).all()
        r = HourlyR()
        rate = r.get_base()
        over = r.get_over()
        if request.method == "POST":
            form = HourlyControl(request=request)
            form.add_entry(employee_id=employee_id)
            return redirect(url_for('employees.employee', employee_id=employee_id))
    elif employee.contract == 'commission':
        form_template = 'employee/forms/commission_form.html'
        table_template = 'employee/tables/commission.html'
        payments = CommissionPayment.query.filter(CommissionPayment.employee_id == employee_id).all()
        if request.method == "POST":
            form = CommissionControl(request=request)
            form.add_entry(employee_id=employee_id)
            return redirect(url_for('employees.employee', employee_id=employee_id))
    elif employee.contract == 'salcom':
        form_template = 'employee/forms/salcom_form.html'
        table_template = 'employee/tables/salcom.html'
        payments = SalaryCommissionPayment.query.filter(SalaryCommissionPayment.employee_id == employee_id).all()
        rate = SalcomR().get_base()
        if request.method == "POST":
            form = SalComControl(request=request)
            form.add_entry(employee_id=employee_id)
            return redirect(url_for('employees.employee', employee_id=employee_id))

    return render_template('employee/employee.html',
                           title=fullname,
                           employee=employee,
                           form_template=form_template,
                           table_template=table_template,
                           payments=payments,
                           rate=rate,
                           over=over)
