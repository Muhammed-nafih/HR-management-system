from django.shortcuts import render, redirect,get_object_or_404
from .models import Employee, Leaves
from datetime import date, datetime

def index(request):
    return render(request,'index.html')

def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})


def employee_add(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        position = request.POST['position']
        salary = request.POST['salary']
        date_joined = request.POST['date_joined']

        Employee.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            position=position,
            salary=salary,
            date_joined=date_joined
        )

        return redirect('employee_list')

    return render(request, 'employee_add.html')


def employee_update(request, id):
    employee = Employee.objects.get(id=id)
    if request.method == 'POST':
        employee.first_name = request.POST['first_name']
        employee.last_name = request.POST['last_name']
        employee.email = request.POST['email']
        employee.position = request.POST['position']
        employee.salary = request.POST['salary']
        employee.date_joined = request.POST['date_joined']
        employee.save()

        return redirect('employee_list')

    return render(request, 'employee_update.html', {'employee': employee})

def employee_delete(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect('employee_list')


def employee_leave_list(request):
    employees = Employee.objects.all()
    current_year = date.today().year
    current_month = date.today().month
    leave_data = []

    for employee in employees:
        annual_leave_taken = Leaves.objects.filter(employee=employee, date__year=current_year).count()
        monthly_leave_taken = Leaves.objects.filter(employee=employee, date__year=current_year,
                                                   date__month=current_month).count()
        annual_leave_balance = 12 - annual_leave_taken
        monthly_leave_balance = 2 - monthly_leave_taken


        leave_data.append({
            'employee': employee,
            'annual_leave_taken': annual_leave_taken,
            'annual_leave_balance': annual_leave_balance,
            'monthly_leave_taken': monthly_leave_taken,
            'monthly_leave_balance': monthly_leave_balance
        })

    return render(request, 'employee_leave_list.html', {'leave_data': leave_data})


def add_leave(request, id):
    employee = Employee.objects.get(id=id)
    if request.method == 'POST':
        leave_date = request.POST['date']
        reason = request.POST['reason']

        leave_date = datetime.strptime(leave_date, "%Y-%m-%d").date()

        current_year = leave_date.year
        current_month = leave_date.month
        monthly_leave_taken = Leaves.objects.filter(employee=employee, date__year=current_year,
                                                   date__month=current_month).count()

        Leaves.objects.create(employee=employee, date=leave_date, reason=reason)

        monthly_leave_taken += 1


        if monthly_leave_taken > 2:
            employee.deductions += 1000
            employee.save()

        return redirect('employee_leave_list')

    return render(request, 'add_leave.html', {'employee': employee})


def employee_salary_details(request, id):
    employee = get_object_or_404(Employee, id=id)
    if request.method == 'POST':

        employee.bonus = float(request.POST.get('bonus', 0))
        employee.deductions = float(request.POST.get('deductions', 0))
        employee.save()
        return redirect('employee_salary_details', id=employee.id)

    net_salary = employee.salary + employee.bonus - employee.deductions
    return render(request, 'employee_salary_details.html', {
        'employee': employee,
        'net_salary': net_salary
    })
