from django.contrib import admin
from .models import Student, Lecturer, Unit, Course, Assignment, Submission
# Register your models here.

class StudentAdmin(admin.ModelAdmin):
	list_display = ('adm_no', 'full_name','units','course', 'year', 'semester')
	list_display_links = ('adm_no', 'full_name')

class LecturerAdmin(admin.ModelAdmin):
	list_display = ('staff_no', 'full_name','lec_units')
	list_display_links = ('staff_no', 'full_name')

class CourseAdmin(admin.ModelAdmin):
	list_display = ('course_code', 'course_name')
	list_display_links = ('course_code', 'course_name')

class UnitAdmin(admin.ModelAdmin):
	list_display = ('unit_code', 'unit_name', 'year','semester','course')
	list_display_links = ('unit_code', 'unit_name')
class AssignAdmin(admin.ModelAdmin):
	list_display = ('assign_id', 'staff_no', 'unit_code','date_created','due_date','assign_text','assign_file')
	list_display_links = ('unit_code', 'assign_file')

class SubmissionAdmin(admin.ModelAdmin):
	list_display = ('assign_id', 'adm_no','assign_file','date_submitted')
	list_display_links = ('assign_id', 'adm_no')

admin.site.register(Student, StudentAdmin)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Assignment,AssignAdmin)
admin.site.register(Submission,SubmissionAdmin)
