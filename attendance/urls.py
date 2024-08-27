from django.urls import path
from . import views

urlpatterns = [
    path('',                                    views.welcome_view,      name='welcome'),
    path('login/student/',                      views.student_login,     name='student_login'),
    path('login/faculty/',                      views.faculty_login,     name='faculty_login'),
    path('dashboard/student/<int:student_id>/', views.student_dashboard, name='student_dashboard'),
    path('login/<str:user_type>/',              views.login_redirect,    name='login_redirect'),
    path('attendance/view/<int:faculty_id>',    views.view_attendance,   name='view_attendance'),
    path('dashboard/faculty/<int:faculty_id>/', views.faculty_dashboard, name='faculty_dashboard'),
    path('logout/',                             views.logout_view,       name='logout'),
    path('faculty/<int:faculty_id>/options/',   views.faculty_options,   name='faculty_options'),
]
