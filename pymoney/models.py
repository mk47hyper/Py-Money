from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from pymoney import db, login_manager
from flask_login import UserMixin
from flask import current_app
from sqlalchemy.ext.declarative import declared_attr


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(20), nullable=False)
    last = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    contract = db.Column(db.String(30), nullable=False)


class Payment(db.Model):
    __abstract__ = True
    dt = datetime.utcnow()
    payment_date = db.Column(db.Text, nullable=False,
                             default=dt.strftime("%m/%d/%Y, %H:%M:%S"))
    amount = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text)
    @declared_attr
    def employee_id(cls):
        return db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

    def __repr__(self):
        return f"Payment('{self.payment_date}', '{self.amount}', '{self.note}', '{self.employee_id}')"


class SalaryPayment(Payment):
    __tablename__ = 'salary_payments'
    id = db.Column(db.Integer, primary_key=True)
    salary = db.Column(db.Integer)
    days_worked = db.Column(db.Integer)


class HourlyPayment(Payment):
    __tablename__ = 'hourly_payments'
    id = db.Column(db.Integer, primary_key=True)
    h_rate = db.Column(db.Integer)
    h_worked = db.Column(db.Integer)
    o_rate = db.Column(db.Integer)
    o_hours = db.Column(db.Integer)


class CommissionPayment(Payment):
    __tablename__ = 'commission_payments'
    id = db.Column(db.Integer, primary_key=True)
    sales = db.Column(db.Integer)
    com_rate = db.Column(db.Integer)


class SalaryCommissionPayment(Payment):
    __tablename__ = 'salcom_payments'
    id = db.Column(db.Integer, primary_key=True)
    salary = db.Column(db.Integer)
    days_worked = db.Column(db.Integer)
    sales = db.Column(db.Integer)
    com_rate = db.Column(db.Integer)
