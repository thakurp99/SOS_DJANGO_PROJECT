from calendar import day_abbr
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from service.utility.DataValidator import DataValidator
from service.models import User
from service.service.ChangePasswordService import ChangePasswordService
from service.service.EmailService import EmailService
from service.service.EmailMessege import EmailMessege
from service.service.UserService import UserService

class ChangePasswordCtl(BaseCtl):

    # Populate From from Http request

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm['id']
        self.form['newPassword'] = requestForm['newPassword']
        self.form['oldPassword'] = requestForm['oldPassword']
        self.form['confirmPassword'] = requestForm['confirmPassword']

    # Populate Form from model

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['newPassword'] = obj.newPassword
        self.form['oldPassword'] = obj.oldPassword
        self.form['confirmPassword'] = obj.confirmPassword

    # Convert Form into module
    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.newPassword = self.form['newPassword']
        obj.oldPassword = self.form['oldPassword']
        obj.confirmPassword = self.form['confirmPassword']
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']
        if (DataValidator.isNull(self.form['oldPassword'])):
            inputError['oldPassword'] = "Old Password Can Not Be Null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['newPassword'])):
            inputError['newPassword'] = "New Password Can Not Be Null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['confirmPassword'])):
            inputError['confirmPassword'] = "Confirm Password Can Not Be Null"
            self.form['error'] = True
        return self.form['error']

    #Display Change Password Page
    def display(self, request, params={}):
        if (params['id'] > 0):
            r = self.get_service().get(params['id'])
            self.model_to_form(r)
        res = render(request, self.get_template(), {'form':self.form})
        return res

    # Submit Change Password Page
    def submit(self, request, params={}):
        user = request.session.get('user',None)
        print('--------------->>>>>>>>>>>>',user)
        q = User.objects.filter(login_id = user.login_id, password = self.form['oldPassword'])
        if q.count() > 0:
            if self.form['confirmPassword'] == self.form['newPassword']:
                emsg = EmailMessege()
                emsg.to = [user.login_id]
                emsg.subject = "Change Password"
                mailResponse = EmailService.send(emsg,'changePassword',user)
                print("------------>>>>>>>>>>>",mailResponse)
                if mailResponse == 1:
                    convertUser = self.convert(user, user.id, self.form['newPassword'],self.form['confirmPassword'])
                    UserService().save(convertUser)

                    self.form['error'] = False
                    self.form[',messege'] = "YOUR PASSWORD HAS BEEN CHANGED SUCCESSFULLY , PLEASE CHECK YOUR MAIL"
                    res = render(request, self.get_template(), {'form':self.form})
                else:
                    self.form['error'] = True
                    self.form['messege'] = "Please Check Your Internet Connection"
                    res = render(request,self.get_template(),{'form':self.form})

            else:
                self.form['error'] = True
                self.form['messege'] = "Confirm Password Are Not Matched"
                res = render(request, self.get_template(), {'form': self.form})

        else:
            self.form['error'] = True
            self.form['messege'] = "Old Password is wrong"
            res = render(request, self.get_template(), {'form':self.form})
        return res

    def convert(self,u , uid, upass, ucpwd):
        u.id = uid
        u.password = upass
        u.confirmpassword = ucpwd
        return u

    def get_template(self):
        return "ChangePassword.html"

    def get_service(self):
        return ChangePasswordService()






