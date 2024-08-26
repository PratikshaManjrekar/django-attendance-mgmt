from django import forms
from .models import Subject

class AttendanceForm(forms.Form):
    date       = forms.DateField(widget=forms.SelectDateWidget)
    time_slot  = forms.ChoiceField(choices=[
        ('09:00-11:00', '09:00-11:00'),
        ('11:00-13:00', '11:00-13:00'),
        ('13:00-15:00', '13:00-15:00'),
        ('15:00-17:00', '15:00-17:00'),
    ])
    subject    = forms.ModelChoiceField(queryset=Subject.objects.all())
    is_present = forms.BooleanField(required=False)
