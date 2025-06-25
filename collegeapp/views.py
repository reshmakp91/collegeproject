from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from collegeapp.models import Course,Student,Teacher
import os


def home(request):
    return render(request,'home.html')

def loginpage(request):
    if request.user.is_authenticated:
        messages.info(request,f'You are already logged in as {request.user.username}.')
        return redirect('home')
    return render(request,'login.html')

def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                messages.info(request,f'Hi, You are now logged in as {request.user.username}')
                return redirect('adminpanel')
            else:
                auth.login(request,user)
                messages.info(request,f'Hi {username}, You are now logged in...')
                return redirect('dashboard')

        else:
            messages.info(request,"Invalid Username or Password")
            return redirect('loginpage')
    return render(request,'login.html')


  
def adminpanel(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request,'adminpanel.html')  
    else:
        messages.info(request,"Access denied. Only admin can view this page.")
        return redirect('home') 


@login_required(login_url='loginpage')
def logout(request):
    auth.logout(request)
    messages.info(request,"You are successfully logged out...")
    return redirect('home')

   
def addcourse(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request,'addcourse.html') 
    else:
        messages.info(request,"Only Admin can add courses...")
        return redirect('home') 
    
def add_course(request):
    if request.method=='POST':
        course_name = request.POST['course_name']
        fee = request.POST['course_fee']
        course = Course(course=course_name,Fee=fee)
        course.save()
        messages.info(request,"New Course Added to portal!!")
        return redirect('addcourse')
    return render(request,'addcourse.html')

   
def addstudent(request):
    if request.user.is_authenticated and request.user.is_staff:
        courses = Course.objects.all()
        return render(request,'addstudent.html',{'courses': courses}) 
    else:
        messages.info(request,"Only Admin can add Students...")
        return redirect('home') 


def add_student(request):
    
    if request.method=='POST':
        name=request.POST['student_name']
        addr = request.POST['student_address']
        age = request.POST['student_age']
        jdate = request.POST['student_jdate']
        sel = request.POST['sel']
        sel_course = Course.objects.get(id=sel)
        student = Student(Name=name,Address=addr,Age=age,Joining_Date=jdate,Course_name=sel_course)
        student.save()
        messages.info(request,"New Student added to portal!!")
        return redirect('addstudent')
    return render(request,'addstudent.html')


def viewstudents(request):
    if request.user.is_authenticated and request.user.is_staff:
        students = Student.objects.all()
        return render(request,'viewstudents.html',{'students': students})
    else:
        messages.info(request,"Only Admin can view Students...")
        return redirect('home') 

def register(request):

    courses = Course.objects.all()
    return render(request,'register.html',{'courses':courses})
    
def register_user(request):
    
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        age = request.POST['age']
        contact = request.POST['mobile']
        addr = request.POST['addr']
        district = request.POST['district']
        state = request.POST['state']
        pincode = request.POST['pincode'] 
        pic = request.FILES.get('picture')
        gender = request.POST['gender']
        sel = request.POST['sel']
        course = Course.objects.get(id=sel)
        experience = request.POST['exp']

        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already taken!!")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email ID already registered!!")
                return redirect('register')
            else:
                user = User.objects.create_user(
                    first_name=fname,
                    last_name=lname,
                    email=email,
                    username=username,
                    password=password
                )
                user.save()
                teacher = Teacher(
                    user=user,
                    Course_name=course,
                    Age=age,
                    Contact=contact,
                    Address=addr,
                    District=district,
                    State=state,
                    Pin=pincode,
                    Image = pic,
                    Gender = gender,
                    Experience = experience
                    )
                teacher.save()
        else:
            messages.info(request,"Passwords do not match!!!")
            return redirect('register')
        messages.info(request,'Registration success! You can login now..')
        return redirect('loginpage')
    return render(request,'register.html')


def editpage(request,pk):

    if request.user.is_authenticated and request.user.is_staff:
        student = Student.objects.get(id=pk)
        courses = Course.objects.all()
    else:
        messages.info(request,"Only Admin can edit Students...")
        return redirect('home') 
    
    return render(request,'editpage.html',{'student':student, 'courses':courses})


def edit_student(request,pk):

    student = Student.objects.get(id=pk)
    courses = Course.objects.all()

    if request.method=='POST':
        
        student.Name = request.POST['student_name']
        student.Address = request.POST['student_address']
        student.Age = request.POST['student_age']
        student.Joining_Date = request.POST['student_jdate']
        sel = request.POST['sel']
        sel_course = Course.objects.get(id=sel)
        student.Course_name = sel_course
        student.save()
        messages.info(request,"Student details updated successfully!!")
        return redirect('editpage', pk=student.id)
    return render(request,'editpage.html',{'student':student, 'courses':courses})

def delete_student(request,pk):
    if request.user.is_authenticated and request.user.is_staff:
        student = Student.objects.get(id=pk)
        student.delete()
        messages.info(request,f'Student deleted successfully!!')
        return redirect('viewstudents')
    else:
        messages.info(request,"Only Admin can delete Students...")
        return redirect('home')
    

def dashboard(request):
    if request.user.is_authenticated and not request.user.is_staff:
        teacher = Teacher.objects.get(user=request.user)
        return render(request,'dashboard.html',{'teacher' : teacher})  
    else:
        messages.info(request,"Access denied. Only Teachers can view this page.")
        return redirect('home')

def viewteachers(request):

    if request.user.is_authenticated and request.user.is_staff:
        teachers = Teacher.objects.all()
        return render(request,'viewteachers.html',{'teachers' : teachers}) 
    else:
        messages.info(request,"Only Admin can view teachers...")
        return redirect('home') 

def editteacher(request,pk):

    if request.user.is_authenticated and request.user.is_staff:
        teacher = Teacher.objects.get(id=pk)
        courses = Course.objects.all()
        return render(request,'editteacher.html',{'teacher' : teacher,'courses':courses}) 
    else:
        messages.info(request,"Only Admin can edit teacher...")
        return redirect('home') 
    
def edit_teacher(request,pk):

    teacher = Teacher.objects.get(id=pk)
    courses = Course.objects.all()
    user = User.objects.get(id=teacher.user.id)

    if request.method=='POST':
        
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.email = request.POST['email']
        user.username = request.POST['username']
        teacher.Age = request.POST['age']
        teacher.Contact = request.POST['mobile']
        teacher.Address = request.POST['addr']
        teacher.District = request.POST['district']
        teacher.State = request.POST['state']
        teacher.Pin = request.POST['pincode'] 
        teacher.Gender = request.POST['gender']
        sel = request.POST['sel']
        course = Course.objects.get(id=sel)
        teacher.Course_name=course
        if len(request.FILES)!=0:
            if len(teacher.Image)>0:
                os.remove(teacher.Image.path)
            teacher.Image = request.FILES['picture']
        teacher.Experience = request.POST['exp']
        teacher.save()
        user.save()
        messages.info(request,"Teacher details updated successfully!!")
        return redirect('editteacher', pk=teacher.id)
    return render(request,'editteacher.html',{'teacher':teacher, 'courses':courses})

def teacherdetails(request,pk):

    if request.user.is_authenticated and request.user.is_staff:
        teacher = Teacher.objects.get(id=pk)
        return render(request,'teacherdetails.html',{'teacher':teacher})
    else:
        messages.info(request,"Only Admin can view teacher profile...")
        return redirect('home') 
    
def deleteteacher(request,pk):

    if request.user.is_authenticated and request.user.is_staff:
        teacher = Teacher.objects.get(id=pk)
        user = User.objects.get(id=teacher.user.id)
        teacher.delete()
        user.delete()
        messages.info(request,"Teacher details deleted successfully!!")
        return redirect('viewteachers')
    else:
        messages.info(request,"Only Admin can delete teacher profile...")
        return redirect('home') 
    
def viewprofile(request,pk):

    teacher = Teacher.objects.get(id=pk)
    
    if request.user.is_authenticated and not request.user.is_staff:
        return render(request,'viewprofile.html',{'teacher':teacher})
    else:
        messages.info(request,f"You have to login as {teacher.user.username} to view this profile")
        return redirect('home') 
    
def editprofile(request,pk):
    
    if request.user.is_authenticated and not request.user.is_staff:
        teacher = Teacher.objects.get(id=pk)
        courses = Course.objects.all()
        return render(request,'editprofile.html',{'teacher' : teacher,'courses':courses}) 
    else:
        messages.info(request,f"You have to login as {teacher.user.username} to edit this profile")
        return redirect('home')  
    
    
def edit_profile(request,pk):

    teacher = Teacher.objects.get(id=pk)
    courses = Course.objects.all()
    user = User.objects.get(id=teacher.user.id)

    if request.method=='POST':
        
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.email = request.POST['email']
        user.username = request.POST['username']
        teacher.Age = request.POST['age']
        teacher.Contact = request.POST['mobile']
        teacher.Address = request.POST['addr']
        teacher.District = request.POST['district']
        teacher.State = request.POST['state']
        teacher.Pin = request.POST['pincode'] 
        teacher.Gender = request.POST['gender']
        sel = request.POST['sel']
        course = Course.objects.get(id=sel)
        teacher.Course_name=course
        if len(request.FILES)!=0:
            if len(teacher.Image)>0:
                os.remove(teacher.Image.path)
            teacher.Image = request.FILES['picture']
        teacher.Experience = request.POST['exp']
        teacher.save()
        user.save()
        messages.info(request,"Teacher details updated successfully!!")
        return redirect('editprofile', pk=teacher.id)
    return render(request,'editprofile.html',{'teacher':teacher, 'courses':courses})








