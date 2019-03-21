from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,HttpRequest,Http404
from .models import Student, Lecturer, Unit, Course
from .forms import signUpForm, allcourseForm
from django.contrib.auth.models import User
# Create your views here.

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
def student_dashboard(request):
  no_course = Student.objects.filter(course__isnull=True)
  if no_course:
    return redirect('select_course')
  return render(request, 'student_dashboard.html')

# Select course
@login_required(login_url='login')
@csrf_protect
def select_course(request):
  if request.method == "POST":
    form = allcourseForm(request.POST)
    if form.is_valid():
      course = form.cleaned_data['course']
      for c in course:
        # get the course intance
        course = Course.objects.get(course_name=c)
        student = Student.objects.get(adm_no=request.user)
        student.course = course
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
def student_edit_units(request):
  # get the course and the units in that course
  student = Student.objects.get(adm_no=request.user)
  student_course = student.course
  student_name = student.full_name
  # Select the units that are in that course
  units = Unit.objects.filter(course=student_course)
  context = {
    'units': units,
    'course_name': student_course,
    'student_name' : student_name
  }
  return render(request, 'student_edit_units.html', context)


# Lecturer dashboard
@login_required(login_url='login')
@csrf_protect
def lecturer_dashboard(request):

  return render(request, 'lecturer_dashboard.html')




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


