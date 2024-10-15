from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.CharField(max_length=100,null=True)
    date_joined = models.DateField(default=0)
    annual_leave_balance = models.IntegerField(default=12)
    monthly_leave_balance = models.IntegerField(default=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def net_salary(self):
        return self.salary + self.bonus - self.deductions

class Leaves(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f'Leave for {self.employee.first_name} {self.employee.last_name} on {self.date}'


