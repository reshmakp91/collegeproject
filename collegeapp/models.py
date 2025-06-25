from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    
    course = models.CharField(max_length=255,null=True)
    Fee = models.IntegerField(null=True)

    def __str__(self):
        return self.course
    
class Student(models.Model):
    
    Name = models.CharField(max_length=255,null=True)
    Address = models.TextField(null=True)
    Age = models.IntegerField(null=True)
    Joining_Date = models.DateField(null=True)
    Course_name = models.ForeignKey(Course, on_delete = models.CASCADE,null=True)

    def __str__(self):
        return self.Name
    
class Teacher(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE,null=True)
    Course_name = models.ForeignKey(Course, on_delete = models.CASCADE,null=True)
    Age = models.IntegerField(null=True)
    Contact = models.CharField(max_length=255,null=True)
    Address = models.TextField(null=True)
    District = models.CharField(max_length=255,null=True)
    State = models.CharField(max_length=255,null=True)
    Pin = models.IntegerField(null=True)
    Gender = models.CharField(max_length=255,null=True)
    Experience = models.IntegerField(null=True)
    Image = models.ImageField(upload_to="images/",null=True)

    def __str__(self):
        return self.user.first_name