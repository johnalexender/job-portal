from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'email', 'resume']