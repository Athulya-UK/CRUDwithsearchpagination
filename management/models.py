from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    joindate=models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=40)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    
    mobile = models.CharField(max_length=40,null=True)
    joindate=models.DateField(auto_now_add=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name

class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='school')
    message=models.CharField(max_length=500)

class Subject(models.Model):
    instructor = models.ForeignKey(User,on_delete=models.CASCADE)
    subect_id=models.CharField(max_length=100,unique=True)
    subject_name=models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    level=models.CharField(max_length=100)
    testlink=models.URLField(max_length=200,null=True,blank=True)
    subject_browser=models.CharField(max_length=2000)
    price=models.IntegerField(default=0)
    subject_image=models.ImageField(upload_to='sub_img/%Y/%m/%d')

    def __str__(self):
        return self.subject_name