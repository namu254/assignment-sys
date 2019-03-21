from django.contrib import admin
from .models import Student, Lecturer, Unit, Course
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
	list_display = ('adm_no', 'full_name','units','course')
	list_display_links = ('adm_no', 'full_name')

class LecturerAdmin(admin.ModelAdmin):
	list_display = ('staff_no', 'full_name','lec_units')
	list_display_links = ('staff_no', 'full_name')

class CourseAdmin(admin.ModelAdmin):
	list_display = ('course_code', 'course_name')
	list_display_links = ('course_code', 'course_name')

class UnitAdmin(admin.ModelAdmin):
	list_display = ('unit_code', 'unit_name')
	list_display_links = ('unit_code', 'unit_name')

admin.site.register(Student, StudentAdmin)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Unit, UnitAdmin)
