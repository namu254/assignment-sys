from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,HttpRequest,Http404
from .models import Student, Lecturer, Unit, Course, Assignment, Submission,Material
from .forms import signUpForm, updateprofileForm, unitFilterForm, assignmentForm, submissionForm, materialForm
from django.contrib.auth.models import User
import datetime
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
# Create your views here.

# test function to redirect users
def student_redirect(user):
  return Student.objects.filter(adm_no=user).exists()

def lecturer_redirect(user):
  return Lecturer.objects.filter(staff_no=user).exists()




# landing page
def landing(request):

  return render(request, 'landing_page.html')

# Index page redirect
@login_required(login_url='login')
@csrf_protect
def index(request):
  user = request.user
  is_student = Student.objects.filter(adm_no=user).exists()
  is_lecturer = Lecturer.objects.filter(staff_no=user).exists()
  if is_student:
    print("hello student")
    return redirect('student_dashboard')
  elif is_lecturer:
    print("hello lecturer")
    return redirect('lecturer_dashboard')
  else:
    raise Http404("That page does not exist!")
  return render(request, 'index.html')

# Student dashboard
@login_required(login_url='login')
@csrf_protect
@user_passes_test(student_redirect,login_url='/')
def student_dashboard(request):
  # check if the student has selected a course
  no_course = Student.objects.filter(course__isnull=True,adm_no=request.user)
  # check if there are no units selected
  no_units = Student.objects.get(adm_no=request.user)
  if no_course:
    return redirect('select_course')
  elif len(no_units.units) == 0:
    print("hello")
    return redirect('student_edit_units')
  
  # get the student details
  student_details = Student.objects.filter(adm_no=request.user)
  context = {
    'student_details': student_details,
    
  }
  return render(request, 'student_dashboard.html',context)

# Select course
@login_required(login_url='login')
@csrf_protect
@user_passes_test(student_redirect,login_url='/')
def select_course(request):
  student = Student.objects.get(adm_no=request.user)
  if request.method == "POST":
    form = updateprofileForm(request.POST, instance=student)
    if form.is_valid():
      student = Student.objects.get(adm_no=request.user)
      # reset the units to empty
      updates = form.save(commit=False)
      updates.units = []
      updates.save()
      messages.success(request, 'Profile updated successfully')
      return redirect('select_course')
    else:
       messages.error(request, 'Error updating profile')
       return redirect('select_course')
  
  form = updateprofileForm(instance=student)
  context = {
    'form': form
  }
  return render(request, 'select_course.html', context)


# Edit units
@login_required(login_url='login')
@csrf_protect
@user_passes_test(student_redirect,login_url='/')
def student_edit_units(request):
  if request.method == "POST":
    		# get the json from the ajax
    changes = request.POST.getlist('data[]')
    student_units = Student.objects.get(adm_no=request.user)
    student_units.units = changes
    student_units.save()
    changes_saved = True
    print(changes)
    data = {
      "changes_saved": changes_saved
    }
    return JsonResponse(data)
  # get the course and the units in that course
  student = Student.objects.get(adm_no=request.user)
  student_course = student.course
  student_name = student.full_name
  student_year = student.year
  student_semester = student.semester
  # Select the units that are in that course
  units = Unit.objects.filter(course=student_course, year=student_year, semester=student_semester)
  context = {
    'units': units,
    'course_name': student_course,
    'student_name' : student_name
  }
  return render(request, 'student_edit_units.html', context)



# get the student units
@login_required(login_url='login')
@csrf_protect
@user_passes_test(student_redirect,login_url='/')
def student_get_units(request):
  data = list()
  student_units = Student.objects.values_list('units', flat=True).filter(adm_no= request.user)
  for i in student_units:
    data = list(i)
	# data = serializers.serialize('json',user_interests)
  return JsonResponse(data, safe=False)

# get the units in a array
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def lec_get_units(request, course_code, year, semester):
  # course instance
  course = Course.objects.get(course_code=course_code)
  units = {}
  all_units = Unit.objects.filter(course=course,year=year,semester=semester)
  if all_units.exists():
    for unit in all_units:
      units[str(unit.unit_code)] = {
        'unit_code': unit.unit_code,
        'unit_name': unit.unit_name,
        'year': unit.year,
        'semester': unit.semester,
      }
    return JsonResponse(units)
  else:
    data = {
      'no_units': True
    }
    return JsonResponse(data)

# Edit lecturer teaching units
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def lecturer_edit_units(request):
  lecturer_details = Lecturer.objects.filter(staff_no=request.user)
  form = unitFilterForm()
  context = {
    'form' : form,
    'lecturer_details' : lecturer_details
  }
  return render(request, 'lecturer_edit_units.html',context)

# view to selected units to the lectures database 
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def lecturer_add_units(request):
  if request.method == "POST":
    course_code = request.POST.get('course_code')
    lec_current_units = Lecturer.objects.get(staff_no=request.user)
    if course_code in lec_current_units.lec_units:
      response_data = {
        'saved': False
        }
      return JsonResponse(response_data)
    else:
      lec_current_units.lec_units.append(course_code)
      lec_current_units.save()
      lec_units_after_update = Lecturer.objects.get(staff_no=request.user)
      response_data = {
              'saved': True,
              'lec_units': lec_units_after_update.lec_units 
            }
      return JsonResponse(response_data)

# remove unit from the lec model
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def lecturer_remove_units(request):
  if request.method == "POST":
    course_code = request.POST.get('course_code')
    lec_current_units = Lecturer.objects.get(staff_no=request.user)
    lec_current_units.lec_units.remove(course_code)
    lec_current_units.save()
    lec_units_after_update = Lecturer.objects.get(staff_no=request.user)
    response_data = {
            'removed': True,
            'lec_units': lec_units_after_update.lec_units 
          }
    return JsonResponse(response_data)


# Lecturer dashboard
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def lecturer_dashboard(request):
  no_units = Lecturer.objects.get(staff_no=request.user)
  if len(no_units.lec_units) == 0:
    return redirect('lecturer_edit_units')
  else:
    # lecturer details
    lecturer_details = Lecturer.objects.filter(staff_no=request.user)
    context = {
      'lecturer_details': lecturer_details,
      
    }
  return render(request, 'lecturer_dashboard.html', context)


# allow the lecturer to give assignments to students 
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def give_assignment(request):
  # Lecture instance
  staff_no = Lecturer.objects.get(staff_no=request.user)
  if request.method == "POST":
    form = assignmentForm(request.POST, request.FILES)
    if form.is_valid():
      assign = form.save(commit=False)
      assign.staff_no = staff_no
      assign.save()
      messages.success(request, 'Assignment submitted successfully')
      return redirect('give_assignment')
    else:
       messages.error(request, 'Error submitting assignment')
       return redirect('give_assignment')
  else:
    form = assignmentForm()
  # lecturer units
  lecturer_details = Lecturer.objects.filter(staff_no=request.user)
  
  context = {
		'form': form,
    'lecturer_details': lecturer_details,
	  }
  return render(request, 'give_assignment.html', context)


# allow the lecturer to give reading materials to students to students 
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def give_materials(request):
    # Lecture instance
  staff_no = Lecturer.objects.get(staff_no=request.user)
  if request.method == "POST":
    form = materialForm(request.POST, request.FILES)
    if form.is_valid():
      material = form.save(commit=False)
      material.staff_no = staff_no
      material.save()
      messages.success(request, 'You have successfully given your students reading materials')
      return redirect('give_materials')
    else:
       messages.error(request, 'Error submitting')
       return redirect('give_materials')
  else:
    form = materialForm()
  # lecturer units
  lecturer_details = Lecturer.objects.filter(staff_no=request.user)
  
  context = {
		'form': form,
    'lecturer_details': lecturer_details,
	  }
  return render(request, 'give_materials.html', context)


# view lecturers assignments
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def lec_view_assignments(request):
  # get the lec instance
  lec = Lecturer.objects.get(staff_no=request.user)
  # all the assign under the logined lec
  assignments = Assignment.objects.filter(staff_no=lec)
  # lecturer units
  lecturer_details = Lecturer.objects.filter(staff_no=request.user)
  context = {
    'lecturer_details': lecturer_details,
    'assignments':assignments,
  }

  return render(request,'lec_view_assignments.html', context)

# view lecturers reading materials
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def lec_view_materials(request):
  # get the lec instance
  lec = Lecturer.objects.get(staff_no=request.user)
  # all the reading materials under the logined lec
  materials = Material.objects.filter(staff_no=lec)
  context = {
    'materials':materials,
  }
  return render(request,'lec_view_materials.html', context)

# view lecturers assignments by filtering the unit code
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def lec_view_assign_by_unit_code(request, unit_code):
  # get the lec instance
  lec = Lecturer.objects.get(staff_no=request.user)
  # all the assign under the logined lec
  assignments = Assignment.objects.filter(staff_no=lec,unit_code=unit_code)
  # lecturer units
  lecturer_details = Lecturer.objects.filter(staff_no=request.user)
  context = {
    'lecturer_details': lecturer_details,
    'assignments':assignments,
  }

  return render(request,'lec_view_assign_by_unit_code.html', context)




# the view to help edit units
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def lec_edit_assign(request, assign_id):
  if request.method == "POST":
    # get the assignment instances
    assignment = Assignment.objects.get(assign_id=assign_id)
    # populated field
    form = assignmentForm(request.POST, request.FILES, instance=assignment)
    if form.is_valid():
      assign = form.save(commit=False)
      assign.save()
      return redirect('lec_view_assignments')
  else:
    # get the assignment instances
    assignment = Assignment.objects.get(assign_id=assign_id)
    # populated field
    form = assignmentForm(instance=assignment)
  # lecturer units
  lecturer_details = Lecturer.objects.filter(staff_no=request.user)
  context = {
    'form':form,
    'lecturer_details': lecturer_details,
    'assign_id':assign_id,
  }
  return render(request,'lec_edit_assign.html', context)


# Api for deleting assignments
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def lec_del_assign(request,assign_id):
  # Lecture instance
  staff_no = Lecturer.objects.get(staff_no=request.user)
  assign_to_del = Assignment.objects.get(assign_id=assign_id,staff_no=staff_no)
  assign_to_del.delete()
  response = {
    'deleted':True,
  }
  return JsonResponse(response)


# Lectures details of the assignments and also the submitted assignments
@login_required(login_url='login')
@csrf_protect
@user_passes_test(lecturer_redirect,login_url='/')
def lec_assign_details(request, assign_id):
  # Lecture instance
  staff_no = Lecturer.objects.get(staff_no=request.user)
  # get that assignment detail
  details = Assignment.objects.get(staff_no=staff_no, assign_id=assign_id)
  # get the assignments submissions 
  submissions = Submission.objects.filter(assign_id=details)
  # check if the due date has passed
  context = {
    'assignment_details':details,
    'submissions':submissions
  }
  return render(request,'lec_assign_details.html', context)


# view for showing the students assignments
@login_required(login_url='login')
@csrf_protect
@user_passes_test(student_redirect,login_url='/')
def student_view_assignments(request):
  # get the student details 
  student_details = Student.objects.filter(adm_no=request.user)
  assignment_list = {}
  # get the student units
  units = Student.objects.get(adm_no=request.user)
  # loop through the student units
  for unit in units.units:
    # get the assignments for the currents units add them in a object
    assignments = Assignment.objects.filter(unit_code=unit)
    for assignment in assignments:
      assignment_list[assignment.assign_id] = assignment
  
  context = {
    'assignment_list': assignment_list,
    'student_details':student_details
  }
  return render(request, 'student_view_assignments.html', context)




# view for showing the students reading materials
@login_required(login_url='login')
@csrf_protect
@user_passes_test(student_redirect,login_url='/')
def student_view_materials(request):
  # get the student details 
  student_details = Student.objects.filter(adm_no=request.user)
  materials_list = {}
  # get the student units
  units = Student.objects.get(adm_no=request.user)
  # loop through the student units
  for unit in units.units:
    # get the reading materials for the currents units add them in a object
    materials = Material.objects.filter(unit_code=unit)
    for material in materials:
      materials_list[material.unit_code] = material
  
  context = {
    'materials_list': materials_list,
    'student_details':student_details
  }
  return render(request, 'student_view_materials.html', context)



# view for submiting the students assignments
@login_required(login_url='login')
@csrf_protect
@user_passes_test(student_redirect,login_url='/')
def student_submit_assignment(request, assign_id):
  # get the asignments details
  assignment_details = Assignment.objects.filter(assign_id=assign_id)
  # assignment instance
  assignment = Assignment.objects.get(assign_id=assign_id)
  # check if the due date is passed
  if assignment.due_date < datetime.date.today():
    due_date_passed = True
  else:
    due_date_passed = False
  # student instance
  student = Student.objects.get(adm_no=request.user)
  if request.method == "POST":
    try:
      # submission instance
      submission = Submission.objects.get(assign_id=assignment)
      # populate the fields/on update
      form = submissionForm(request.POST, request.FILES, instance=submission)
      submitted = True
    except Submission.DoesNotExist:
      form = submissionForm(request.POST, request.FILES)
      submitted = False
    if form.is_valid:
      assign = form.save(commit=False)
      assign.assign_id = assignment
      assign.adm_no = student
      assign.save()
      messages.success(request, 'Assignement submitted successfully')
      return HttpResponseRedirect(reverse('student_submit_assignment', args=[assign_id]))
    else:
       messages.error(request, 'Error submiting assignment')
       return HttpResponseRedirect(reverse('student_submit_assignment', args=[assign_id]))
  else:
    try:
      # submission instance
      submission = Submission.objects.get(assign_id=assignment)
      submitted = True
      # populate the fields
      form = submissionForm(instance=submission)
    except Submission.DoesNotExist:
      form = submissionForm()
      submitted = False

  context = {
    'assignment_details': assignment_details,
    'form':form,
    'assign_id':assign_id,
    'submitted':submitted,
    'due_date_passed': due_date_passed,
  }
  
  return render(request, 'student_submit_assignment.html', context)



# view for finding a lecturer
@login_required(login_url='login')
@csrf_protect
@user_passes_test(student_redirect,login_url='/')
def find_lecturer(request):
  lecturers_list = {}
  if request.method == "POST":
    # get the q
    query_tag = request.POST.get('q')
    # perform the query for the lecturers
    try:
      # complex query
      lecturers = Lecturer.objects.filter(
        Q(lec_units__overlap=[query_tag]) | Q(full_name__icontains=query_tag)
      )
      for lecturer in lecturers:
        lecturers_list[lecturer.staff_no] = {
          'name' : lecturer.full_name,
          'units': lecturer.lec_units
        }
      return JsonResponse(lecturers_list)
    except Lecturer.DoesNotExist:
      pass
  return render(request, 'find_lecturer.html')

# view for signing new users
def sign_up(request):
    if request.method == "POST":
      #Get the sign_up form data from the request
      username = request.POST.get('username')
      email = request.POST.get('email')
      password = request.POST.get('password')
      # Database queries for User/Student/Lecturer
      check_student = Student.objects.filter(adm_no=username).exists()
      check_lecturer = Lecturer.objects.filter(staff_no=username).exists()
      check_username = User.objects.filter(username=username).exists()
      # Chek if the username is in the Student or lecturer database
      if check_lecturer or check_student:
        # Check if the username has an account already
        if check_username:
          response_data = {
            'user_exists': True
          }
          return JsonResponse(response_data)
        else:
          user = User.objects.create_user(username,email,password)
          user.save()
          response_data = {
            'created': True
          }
          return JsonResponse(response_data)
      else:
          response_data = {
          'not_created': True
          }
          return JsonResponse(response_data)
    form = signUpForm()
    context = {
		  'form': form,
	  }
    return render(request, 'registration/signup.html', context)


