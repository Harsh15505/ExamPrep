from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student-list'),
    path('add/', views.add_student, name='add-student'),
    path('<int:pk>/edit/', views.edit_student, name='edit-student'),
    path('<int:pk>/delete/', views.delete_student, name='delete-student'),
]

# Project-level urls.py should include:
# path('students/', include('students.urls')),
