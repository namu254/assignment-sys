from django import forms
from django.forms import ModelForm
from .models import Course
# Form to handle the sign up 
class signUpForm(forms.Form):
	username = forms.CharField(label='Username (Adm Number or Staff Number)')
	email=  forms.EmailField(label='email')
	password = forms.CharField(widget=forms.PasswordInput())

class allcourseForm(forms.Form):
	course = forms.ModelMultipleChoiceField(queryset=Course.objects.all())