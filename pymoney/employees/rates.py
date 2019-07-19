class Rate:
    def __init__(self):
        self.base = 0

    def set_base(self, amount):
        self.base = amount

    def get_base(self):
        return self.base



class SalaryR(Rate):
    def __init__(self):
        super().__init__()
        self.base = 55000


class HourlyR(Rate):
    def __init__(self):
        super().__init__()
        self.base = 9.75
        self.over = round((self.base * 1.5), 2)

    def get_over(self):
        return self.over


class SalcomR(SalaryR):
    pass
