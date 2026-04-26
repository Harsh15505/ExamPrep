from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student
from .forms import StudentForm


def student_list(request):
    """List all students + search by course"""
    query = request.GET.get('course', '')
    if query:
        students = Student.objects.filter(course__icontains=query)
        # __icontains = case-insensitive SQL: WHERE course ILIKE '%query%'
    else:
        students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students, 'query': query})


def add_student(request):
    """Create a new student"""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()                             # INSERT INTO students_student ...
            messages.success(request, 'Student added successfully!')
            return redirect('student-list')         # POST-Redirect-GET pattern
    else:
        form = StudentForm()
    return render(request, 'students/form.html', {'form': form, 'title': 'Add Student', 'btn': 'Add'})


def edit_student(request, pk):
    """Update an existing student"""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)  # instance= → UPDATE not INSERT
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated!')
            return redirect('student-list')
    else:
        form = StudentForm(instance=student)                # pre-fill form with existing data
    return render(request, 'students/form.html', {'form': form, 'title': 'Edit Student', 'btn': 'Update'})


def delete_student(request, pk):
    """Delete a student (POST only)"""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()                            # DELETE FROM students_student WHERE id=pk
        messages.success(request, f'"{student.name}" deleted.')
        return redirect('student-list')
    return render(request, 'students/confirm_delete.html', {'student': student})
