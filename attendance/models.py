from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    
class Student(models.Model):
    user     = models.OneToOneField(User,on_delete=models.CASCADE)
    roll_no  = models.CharField(max_length=10, unique=True)
    name     = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    user       = models.OneToOneField(User,on_delete=models.CASCADE)
    faculty_id = models.CharField(max_length=10, unique=True)
    name       = models.CharField(max_length=100)
    password   = models.CharField(max_length=100)
    subjects   = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student    = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject    = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date       = models.DateField()
    time_slot  = models.CharField(max_length=20)
    is_present = models.BooleanField(default=True)

    class Meta:
        unique_together = ['student', 'subject', 'date', 'time_slot']
