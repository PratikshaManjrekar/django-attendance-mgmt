from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import AttendanceForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.db import IntegrityError

def welcome_view(request):
    return render(request, 'welcome.html')


def login_redirect(request, user_type):
    if user_type == 'student':
        return redirect('student_login')
    elif user_type == 'faculty':
        return redirect('faculty_login')
    else:
        return redirect('welcome')


def student_dashboard(request, student_id):
    if not request.session.get('student_id') or int(request.session.get('student_id'))!=student_id:
        return redirect('student_login')
    student             = get_object_or_404(Student, id=student_id)
    selected_subject_id = request.GET.get('subject')
    if selected_subject_id:
        attendance_records = Attendance.objects.filter(student=student, subject_id=selected_subject_id)
    else:
        attendance_records = Attendance.objects.filter(student=student)
    subjects = student.subjects.all()
    context  = {
        'student': student,
        'subjects': subjects,
        'attendance_records': attendance_records
    }
    return render(request, 'student_dashboard.html', context)


def student_login(request):
    if request.method == "POST":
        roll_no  = request.POST.get('roll_no')
        password = request.POST.get('password')
        print("trying to log in")
        try:
            student = authenticate(request, username=roll_no, password=password)
            if student is not None:
                print("logged in")
                login(request, student)
                request.session['student_id'] = roll_no
                return redirect('student_dashboard', student_id=roll_no)
            else:
                messages.error(request, 'Invalid password')
        except Student.DoesNotExist:
            messages.error(request, 'Student not found')
    return render(request, 'student_login.html')


def faculty_login(request):
    if request.method == "POST":
        faculty_id = request.POST.get('faculty_id')
        password   = request.POST.get('password')
        # print('Trying to log in...')
        try:
            faculty = Faculty.objects.get(faculty_id=faculty_id)
            user    = authenticate(request, username=faculty.user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse(('faculty_dashboard'), args=[faculty.id]))
            else:
                return render(request, 'faculty_login.html',{'error':'Invalid password'})
        except Faculty.DoesNotExist:
            return render(request, 'faculty_login.html',{'error':'Faculty ID does not exist'})
    return render(request,'faculty_login.html')


def faculty_dashboard(request, faculty_id):
    if not request.user.is_authenticated:
        return redirect('faculty_login')
    faculty  = Faculty.objects.get(id=faculty_id)
    subjects = faculty.subjects.all()
    students = Student.objects.all()
    if request.method == 'POST':
        date       = request.POST.get('date')
        time_slot  = request.POST.get('time_slot')
        subject_id = request.POST.get('subject')
        subject    = Subject.objects.get(id=subject_id)

        for student_id in request.POST:
            if student_id.startswith('present_'):
                student    = Student.objects.get(id=student_id.split('_')[1])
                is_present = request.POST.get(student_id) == 'on'
                try:
                    attendance_record, created = Attendance.objects.get_or_create(
                        student   = student,
                        subject   = subject,
                        date      = date,
                        time_slot = time_slot,
                        defaults  = {'is_present': is_present}
                    )
                    if not created:
                        attendance_record.is_present = is_present
                        attendance_record.save()
                except IntegrityError:
                    continue

        return redirect('view_attendance', faculty_id=faculty_id)
    
    return render(request, 'faculty_dashboard.html', {
        'faculty' : faculty,
        'subjects': subjects,
        'students': students,
        'form'    : AttendanceForm()
    })
    

def view_attendance(request, faculty_id):
    if not request.user.is_authenticated:
        return redirect('faculty_login')
    try:
        faculty            = Faculty.objects.get(id=faculty_id)
        subjects           = faculty.subjects.all()
        students           = Student.objects.filter(subjects__in=subjects).distinct()
        attendance_records = Attendance.objects.filter(
            student__in    = students,
            subject__in    = subjects
        ).select_related('student', 'subject')
    except Faculty.DoesNotExist:
        return redirect('faculty_login')
    return render(request, 'view_attendance.html', {
        'faculty'           : faculty,
        'attendance_records': attendance_records,
    })


def logout_view(request):
    auth_logout(request)
    return redirect('welcome')
