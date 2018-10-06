from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import logout,authenticate,login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from app.models import *
from django.core.paginator import Paginator

import requests
from bs4 import BeautifulSoup
import re


user_permissions = [

'Can add session',
'Can change session',
'Can delete session',
'Can add actions',
'Can change actions',
'Can delete actions',
'Can add check lists',
'Can change check lists',
'Can delete check lists',
]




def error_page(request,err):
    return render(request,'error.html',context={"err":err})


def home(request):
    return render(request, 'home.html')



def about(request):
    return render(request,'about.html')

def login_user(request):
    if request.method == 'GET':
        return render(request,'login.html')

    elif request.method == 'POST':
        user = authenticate(username=request.POST['user_login'], password=request.POST['user_password'])
        if user:
            login(request, user)
            return listofcases(request)
        else:
            return error_page(request,"invalid password or login")
    else:
        return error_page(request,"invalid method")

def logout_user(request):
    logout(request)
    return render(request,'after_logout.html',{'username':request.user.username})

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')

    elif request.method == 'POST' and not request.user.is_authenticated:
        _login = request.POST['user_login']
        email = request.POST['user_email']
        password = request.POST['user_password']
        password_retype = request.POST['user_password_retype']
        if password != password_retype:
            return error_page(request,'recheck passwords')

        #TODO: validate post data
        user = User(username=_login,first_name=_login,email=email,password=password)
        user.set_password(password) # without hash algorithm (raw)
        if not user:
            return error_page(request,'invalid data')

        user.save()

        for perm in user_permissions:
            user.user_permissions.add(Permission.objects.get(name=perm))
        user.save()
        
        login(request,user)
        authenticate(request,username=_login,password=password)
        return HttpResponseRedirect('/listofcases/')
    
def createchecklist(request):
    
    if request.method == 'POST':
        author = User.objects.get(username=request.user)
        actions = request.POST.getlist('action')
        proj_name = request.POST['project_name']
        checklist_name = request.POST['checklist_name']
        print(request.POST)


        #

        checklist = CheckLists.objects.create( name=checklist_name,project_name=proj_name,author=author )
        checklist.save()

        #

        for a in actions:
            action = Actions.objects.create(name=a,project=checklist,notes='')
            action.save()

        #

        return HttpResponseRedirect('/listofcases/')
    elif request.method == 'GET':
        return render(request,'createchecklist.html')

def listofcases(request):
    cases_by_user_active = CheckLists.objects.filter(is_active=True,is_visible=True).order_by('-add')
    cases_by_user_complete = CheckLists.objects.filter(is_active=False,is_visible=True).order_by('-add')

    return render(request,'listofcases.html',{"cases_active":cases_by_user_active,"cases_complete":cases_by_user_complete})


def checklist(request,id):

    checklist = CheckLists.objects.get(pk=id)
    actions = Actions.objects.filter(project=checklist)
    return render(request,'checklist.html',{'checklist':checklist,'actions':actions})
    # if checklist.author == request.user:
    #     return render(request,'checklist.html',{'checklist':checklist,'actions':actions})
    # else:
    #     return error_page(request,'invalid checklist')

def toggle_status(request,id):
    c = CheckLists.objects.get(pk = id)
    if c.is_active:
        c.is_active = False
        # remove actions infos :


    else:
        c.is_active = True
        c.touched   = False
        actions = Actions.objects.filter(project=c)
        for a in actions:
            a.is_active = False
            a.notes = ''
            a.save()

    c.save()

    return listofcases(request)


def toggle_action(request,action_id,checklist_id):
    a = Actions.objects.get(pk=action_id)

    if a.status == False:
        a.status = True
    else:
        a.status = False

    c = CheckLists.objects.get(pk=checklist_id)
    c.touched = True
    c.save()
    a.save()
    return HttpResponseRedirect('/checklist/{}'.format(checklist_id))

def finish_checklist(request,checklist_id):
    c = CheckLists.objects.get(pk = checklist_id)
    

    # actions = Actions.objects.filter(project=c)
    # for a in actions:
    #     a.touched = False
    #     a.notes = ''
    #     a.save()

    c.is_active = False
    c.save()
    return listofcases(request)


def add_note(request):

    # checklist id
    # action id
    # note

    note = request.POST['note']
    checklist_id = request.POST['checklist_id']
    action_id = request.POST['action_id']

    print(note,checklist_id,action_id)

    selected_checklist = CheckLists.objects.get(pk=int(checklist_id))
    selected_action = Actions.objects.get(pk=int(action_id))

    selected_action.notes = note
    selected_action.save()

    return HttpResponseRedirect("/checklist/"+checklist_id)

    #return HttpResponse("ok")
def remove_checklist(request,checklist_id):

    c = CheckLists.objects.get(pk=checklist_id)
    c.is_visible = False
    c.is_active = False
    c.save()

    return HttpResponseRedirect("/listofcases/")