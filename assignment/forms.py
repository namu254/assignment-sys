from django import forms
from django.forms import ModelForm, TextInput
from .models import Course, Assignment, Submission
from django.utils.translation import gettext_lazy as _
# Form to handle the sign up 
class signUpForm(forms.Form):
	username = forms.CharField(label='Username (Adm Number or Staff Number)')
	email=  forms.EmailField(label='email')
	password = forms.CharField(widget=forms.PasswordInput())

class allcourseForm(forms.Form):
	First = '1'
	Second = '2'
	Third = '3'
	Fourth = '4'
	Year_choices = (
        (First, 'First Year'),
        (Second, 'Second Year'),
        (Third, 'Third Year'),
        (Fourth, 'Fourth Year'),
    )
	Semester_choices = (
        (First, 'First Semester'),
        (Second, 'Second Semester'),
        (Third, 'Third Semester'),
        (Fourth, 'Fourth Semester'),
    )
	course = forms.ModelChoiceField(queryset=Course.objects.all())
	year = forms.ChoiceField(choices=Year_choices)
	semester = forms.ChoiceField(choices=Semester_choices)


class unitFilterForm(forms.Form):
	First = '1'
	Second = '2'
	Third = '3'
	Fourth = '4'
	Year_choices = (
        (First, 'First Year'),
        (Second, 'Second Year'),
        (Third, 'Third Year'),
        (Fourth, 'Fourth Year'),
    )
	Semester_choices = (
        (First, 'First Semester'),
        (Second, 'Second Semester'),
        (Third, 'Third Semester'),
        (Fourth, 'Fourth Semester'),
    )
	course = forms.ModelChoiceField(queryset=Course.objects.all())
	year = forms.ChoiceField(choices=Year_choices)
	semester = forms.ChoiceField(choices=Semester_choices)

class assignmentForm(ModelForm):
	class Meta:
		model = Assignment
		fields = ['unit_code', 'due_date', 'assign_text', 'assign_file']
		widgets = {
            'due_date': TextInput(attrs={'id': 'datepicker'}),
			'unit_code': TextInput(attrs={'readonly': 'readonly','placeholder':'Select the unit code on your left.'}),
        }

class submissionForm(ModelForm):
	class Meta:
		model = Submission
		fields = ['assign_file',]