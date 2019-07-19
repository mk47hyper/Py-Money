from pymoney.employees.routes import *


class EmployeeControl:
    def __init__(self, request):
        self.request = request
        self.pay = request.form['pay']
        self.note = request.form['note']

    def add_entry(self, employee_id):
        raise Exception(
            'This function is used to add a database entry, when called by one of the subclasses of EmployeeControl')


class SalaryControl(EmployeeControl):
    def __init__(self, request):
        super().__init__(request)
        self.base_pay = request.form["base_pay"]
        self.days = request.form['days']

    def add_entry(self, employee_id):
        entry = SalaryPayment(salary=self.base_pay, days_worked=self.days,
                              amount=self.pay, employee_id=employee_id, note=self.note)
        db.session.add(entry)
        db.session.commit()
        flash('Payment Authorized!', 'success')


class HourlyControl(EmployeeControl):
    def __init__(self, request):
        super().__init__(request)
        self.h_rate = request.form['hour_rate']
        self.hours = request.form['hours_worked']
        self.o_rate = request.form['overtime_rate']
        self.overtime = request.form['overtime_hours']

    def add_entry(self, employee_id):
        entry = HourlyPayment(h_rate=self.h_rate,
                              h_worked=self.hours,
                              o_rate=self.o_rate,
                              o_hours=self.overtime,
                              amount=self.pay,
                              note=self.note,
                              employee_id=employee_id)
        db.session.add(entry)
        db.session.commit()
        flash('Payment Authorized!', 'success')


class CommissionControl(EmployeeControl):
    def __init__(self, request):
        super().__init__(request)
        self.sales = request.form['sales']
        self.com_rate = request.form['com_rate']

    def add_entry(self, employee_id):
        entry = CommissionPayment(sales=self.sales,
                                  com_rate=self.com_rate,
                                  amount=self.pay,
                                  note=self.note,
                                  employee_id=employee_id)
        db.session.add(entry)
        db.session.commit()
        flash('Payment Authorized!', 'success')


class SalComControl(SalaryControl, CommissionControl):
    def __init__(self, request):
        super().__init__(request)

    def add_entry(self, employee_id):
        entry = SalaryCommissionPayment(salary=self.base_pay,
                                        days_worked=self.days,
                                        sales=self.sales,
                                        com_rate=self.com_rate,
                                        amount=self.pay,
                                        note=self.note,
                                        employee_id=employee_id)
        db.session.add(entry)
        db.session.commit()
        flash('Payment Authorized!', 'success')
