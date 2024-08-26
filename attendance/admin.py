from django.contrib import admin
from .models import *

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Subject)
admin.site.register(Attendance)