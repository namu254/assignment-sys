from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Course(models.Model):
    course_code = models.CharField(max_length=100, primary_key=True)
    course_name = models.CharField(max_length=100)
    def __str__(self):
        return self.course_name

class Unit(models.Model):
    unit_code = models.CharField(max_length=100, primary_key=True)
    unit_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE) 
    def __str__(self):
        return self.unit_code


class Student(models.Model):
    adm_no = models.CharField(max_length=50, primary_key=True)
    full_name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True) 
    units =  ArrayField(models.CharField(max_length=200), blank=True, null=True)
    def __str__(self):
        return self.adm_no

class Lecturer(models.Model):
    staff_no = models.CharField(max_length=50, primary_key=True)
    full_name = models.CharField(max_length=200)
    lec_units =  ArrayField(models.CharField(max_length=200), blank=True, null=True)
    def __str__(self):
        return self.staff_no

