"""assignment_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin,auth
from django.urls import path, include
from assignment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('lecturer_dashboard', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('select_course', views.select_course, name='select_course'),
    path('student_edit_units', views.student_edit_units, name='student_edit_units'),
    path('student_get_units', views.student_get_units, name='student_get_units'),
    path('lecturer_edit_units', views.lecturer_edit_units, name='lecturer_edit_units'),
    path('lec_get_units/<str:course_code>/<int:year>/<int:semester>', views.lec_get_units, name='lec_get_units'),
    path('lecturer_add_units', views.lecturer_add_units, name='lecturer_add_units'),
    path('lecturer_remove_units', views.lecturer_remove_units, name='lecturer_remove_units'),
    path('give_assignment', views.give_assignment, name='give_assignment'),
]
