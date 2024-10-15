from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('',views.index),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('employees/update/<int:id>/', views.employee_update, name='employee_update'),
    path('employees/delete/<int:id>/', views.employee_delete, name='employee_delete'),
    path('employees/leaves/', views.employee_leave_list, name='employee_leave_list'),
    path('employees/<int:id>/add_leave/', views.add_leave, name='add_leave'),
    path('employees/<int:id>/salary/', views.employee_salary_details, name='employee_salary_details'),

]
