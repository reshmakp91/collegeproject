from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('loginpage',views.loginpage,name='loginpage'),
    path('user_login',views.user_login,name='user_login'),
    path('logout',views.logout,name='logout'),
    
    path('adminpanel',views.adminpanel,name='adminpanel'),
    path('addcourse',views.addcourse,name='addcourse'),
    path('add_course',views.add_course,name='add_course'),
    path('addstudent',views.addstudent,name='addstudent'),
    path('add_student',views.add_student,name='add_student'),
    path('viewstudents',views.viewstudents,name='viewstudents'),
    path('editpage/<int:pk>',views.editpage,name='editpage'),
    path('edit_student/<int:pk>',views.edit_student,name='edit_student'),
    path('/<int:pk>',views.delete_student,name='delete_student'),
   
    path('teacherdetails/<int:pk>',views.teacherdetails,name='teacherdetails'),
    path('viewteachers',views.viewteachers,name='viewteachers'),
    path('deleteteacher/<int:pk>',views.deleteteacher,name='deleteteacher'),

    path('register',views.register,name='register'),
    path('register_user',views.register_user,name='register_user'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('viewprofile/<int:pk>',views.viewprofile,name='viewprofile'),
    path('editprofile/<int:pk>',views.editprofile,name='editprofile'),
    path('edit_profile/<int:pk>',views.edit_profile,name='edit_profile'),

    
    
]