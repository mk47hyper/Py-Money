from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DateTimeField, IntegerField
from wtforms.validators import DataRequired


class EmployeeForm(FlaskForm):
    first = StringField('First Name', validators=[DataRequired()])
    last = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    contract = SelectField('Contract',
                           choices=[('salary', 'Salaried'), ('hourly', 'Hourly'), ('commission', 'Commission'), ('salcom', 'Salary / Commission')])
    submit = SubmitField('Add Employee')
