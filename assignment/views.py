from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,HttpRequest,Http404
from .models import Student, Lecturer, Unit, Course
from .forms import signUpForm, allcourseForm, unitFilterForm
from django.contrib.auth.models import User
# Create your views here.

# test function to redirect users
def student_redirect(user):
  return Student.objects.filter(adm_no=user).exists()

def lecturer_redirect(user):
  return Lecturer.objects.filter(staff_no=user).exists()


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
  if no_course:
    return redirect('select_course')
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
  if request.method == "POST":
    form = allcourseForm(request.POST)
    if form.is_valid():
      course = form.cleaned_data['course']
      year = form.cleaned_data['year']
      # get the course intance
      course = Course.objects.get(course_name=course)
      student = Student.objects.get(adm_no=request.user)
      # reset the units to empty
      student.units = []
      student.course = course
      student.year = year
      student.save()
      return redirect('student_edit_units')
  form = allcourseForm()
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

  return render(request, 'give_assignment.html')




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


