from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Course(models.Model):
    course_code = models.CharField(max_length=100, primary_key=True)
    course_name = models.CharField(max_length=100)
    def __str__(self):
        return self.course_name

class Unit(models.Model):
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
    semester_choices = (
        (First, 'First semester'),
        (Second, 'Second semester'),
        (Third, 'Third semester'),
        (Fourth, 'Fourth semester'),
    )
    unit_code = models.CharField(max_length=100, primary_key=True)
    unit_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.CharField(max_length=1,choices=Year_choices,default= First)
    semester = models.CharField(max_length=1,choices=semester_choices,default= First)
    def __str__(self):
        return self.unit_code

class Student(models.Model):
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
    semester_choices = (
        (First, 'First semester'),
        (Second, 'Second semester'),
        (Third, 'Third semester'),
        (Fourth, 'Fourth semester'),
    )
    adm_no = models.CharField(max_length=50, primary_key=True)
    full_name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True) 
    units =  ArrayField(models.CharField(max_length=200), blank=True, null=True)
    year = models.CharField(max_length=1,choices=Year_choices,default=First)
    semester = models.CharField(max_length=1,choices=semester_choices,default=First)
    def __str__(self):
        return self.adm_no

class Lecturer(models.Model):
    staff_no = models.CharField(max_length=50, primary_key=True)
    full_name = models.CharField(max_length=200)
    lec_units =  ArrayField(models.CharField(max_length=200), blank=True, null=True)
    def __str__(self):
        return self.staff_no
