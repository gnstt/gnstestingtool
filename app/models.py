from django.db import models
from django.contrib.auth.models import User

class CheckLists(models.Model):
    touched = models.BooleanField(default=False)
    name = models.CharField(max_length=300,default='untitled checklist')
    project_name = models.CharField(max_length=300,default='untitled project')
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    add = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=1500,null=True,blank=True)



class Actions(models.Model):
    name = models.CharField(max_length=300,default='untitled action')
    project = models.ForeignKey(CheckLists,on_delete=models.CASCADE)
    notes = models.TextField(max_length=1500,null=True,blank=True)
    date_start = models.DateTimeField(auto_now_add=True)
    date_end   = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    status = models.BooleanField(default=True)
    attach = models.FileField(upload_to='attach',blank=True)




    