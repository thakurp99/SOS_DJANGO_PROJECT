from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.sessions.models import Session
from .Ctl.HomeCtl import HomeCtl
from .Ctl.BaseCtl import BaseCtl
from .Ctl.WelcomeCtl import WelcomeCtl
from .Ctl.LoginCtl import LoginCtl
from .Ctl.RegistrationCtl import RegistrationCtl
from .Ctl.ForgotPasswordCtl import ForgotPasswordCtl
from .Ctl.ChangePasswordCtl import ChangePasswordCtl
from .Ctl.MyProfileCtl import MyProfileCtl
from .Ctl.UserCtl import UserCtl
from .Ctl.UserListCtl import UserListCtl
from .Ctl.CollegeCtl import CollegeCtl
from .Ctl.CollegeListCtl import CollegeListCtl
from .Ctl.CourseCtl import CourseCtl
from .Ctl.CourseListCtl import CourseListCtl
from .Ctl.MarksheetCtl import MarksheetCtl
from .Ctl.MarksheetListCtl import MarksheetListCtl
from .Ctl.MarksheetMeritListCtl import MarksheetMeritListCtl
from .Ctl.RoleCtl import RoleCtl
from .Ctl.RoleListCtl import RoleListCtl
from .Ctl.StudentCtl import StudentCtl
from .Ctl.StudentListCtl import StudentListCtl
from .Ctl.SubjectCtl import SubjectCtl
from .Ctl.SubjectListCtl import SubjectListCtl
from .Ctl.AddFacultyCtl import AddFacultyCtl
from .Ctl.AddFacultyListCtl import AddFacultyListCtl
from .Ctl.TimeTableCtl import TimeTableCtl
from .Ctl.TimeTableListCtl import TimeTableListCtl


# Create your views here.

def action(request, page, action=""):
    ctlName = page + "Ctl()"
    ctlObj = eval(ctlName)
    return ctlObj.execute(request,{"id" : 0})


@csrf_exempt
def actionId(request, page ="", operation="", id=0):
    path = request.META.get('PATH_INFO')
    print('ppppppppppppp',path)
    if request.session.get('user') is not None and page !="":
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = None
        res = ctlObj.execute(request, {"id":id})
    elif page == "Registration":
        ctlName = "Registration" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {'id':id})
    elif page == "Home":
        ctlName = "Home" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})
    elif page == "ForgotPassword":
        ctlName = "ForgotPassword" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request,{"id":id})
    elif page == "Login":
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        request.session['msg'] = None
        print("mmmmmm___(view actionID)_____mmmmmmm",request.session.get('msg'))
        res = ctlObj.execute(request,{"id":id })

    else:
        cltName = "Login" + "Ctl()"
        ctlObj = eval(cltName)
        request.session['msg'] = "Your Session has been Expired, Please Login again"
        res = ctlObj.execute(request,{"id":id,"path":path})
    return res

@csrf_exempt
def auth(request, page="", operation="",id=0):
    global res
    if page == "Logout":
        Session.objects.all().delete()
        request.session['user'] = None
        out = "LOGOUT SUCCESSFULL"
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id":id, "operation":operation, "out":out})
    elif page == "ForgotPassword":
        ctlName = "ForgotPassword" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request,{"id":id, "operation":operation })
    return res


def index(request):
    res = render(request, 'project.html')
    return res

def GET(self):
    return HttpResponse("Hello Guys")
