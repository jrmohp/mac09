from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *

import random,string
from django.contrib import auth,messages
from  django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime,os
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from user.models import *


from django.core.files import File

basemed = "/home/jrm/website/"


def error_404(request):
    return render("404.html")

def error_500(request):
    return render("500.html")

def base(request):

    return render(request,'asi/base.html')



def customrend(request,temp):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            allt = teamdata.objects.all().filter().order_by('-created_at')
            p1 = teamdata.objects.filter(payment1= True).count()
            p2 = teamdata.objects.filter(payment2= True).count()
            tc = teamdata.objects.filter().count()
            tdata = {'teams': allt, 'p1':p1 , 'p2':p2,'memnum':tc}
            return (request, temp, tdata)
        else:
            return HttpResponseRedirect('/asi/login/')
    else:
        return HttpResponseRedirect('/asi/login/')







def viewenv(request):
    (req, temp, tdata) = customrend(request, 'asi/viewinvdetails.html')
    pid = tdata['pid'] = payments.objects.get(id=request.GET['id'])
    pgstin = tdata['pgstin'] = gstindetails.objects.get(teamid=pid.teamid)
    try:
        tdata['inv'] = invoice.objects.get(gstdet__teamid=pid.teamid)
    except:
        inv= {'invoicenumber':"NA",'invoicedate':"NA",'phase':"NA",'id':"new"}
        tdata['inv'] = inv



    return render(request, temp, tdata)





def index(request):
    if request.user.is_authenticated:
        try:
            (req, temp, tdata) = customrend(request, 'asi/index.html')
        except:
            return HttpResponseRedirect('/asi/login/')



        return render(request, temp, tdata)
    else:
        return HttpResponseRedirect('/asi/login/')





def paymentp(request):
    if request.user.is_authenticated:
            (req, temp, tdata) = customrend(request, 'asi/payments.html')
            paymentobs = payments.objects.all().filter().order_by('-time')
            tdata['payments'] = paymentobs
            return render(request, temp, tdata)






def updatep(request):
    (req, temp, tdata) = customrend(request, 'asi/updatepayment.html')

    if request.method == "POST":
        inv=invoice()
        inv.invoicenumber = request.POST['invno']
        inv.invoicedate = request.POST['invdate']
        inv.phase = request.POST['phase']
        gstid = request.POST['gstin']
        gstob = gstindetails.objects.get(id= gstid)
        inv.gstdet = gstob
        paym = payments.objects.get(id = request.POST['pid'])
        paym.updated = True
        team = teamdata.objects.get(teamid= paym.teamid)
        if(inv.phase == "Phase 1"):
            team.payment1 = True
        elif(inv.phase == "Phase 2"):
            team.payment2 = True
        try:
            inv.save()
            paym.save()
            team.save()
            return HttpResponse("<script>alert('Updated With Invoice');window.location.assign('/asi/payments/');</script>")
        except:
            return HttpResponse("<script>alert('Unable To Update');window.location.assign('/asi/payments/');</script>")




    else:
        pid = tdata['pid'] = payments.objects.get(id=request.GET['id'])
        print(pid.teamid)
        pgstin = tdata['pgstin'] = gstindetails.objects.get(teamid=pid.teamid)

        if (pid.phase == "Phase 1"):
            tdata['proof'] = teamdata.objects.get(teamid=pid.teamid).payment1proof
        else:
            tdata['proof'] = teamdata.objects.get(teamid=pid.teamid).payment2proof







        return render(request, temp, tdata)


def login(request):
    if request.method == 'POST':
        username = request.POST['tid']
        password = request.POST['pwd']

        try:
            user2 = User.objects.get(username=username)
            try:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        auth.login(request, user)
                        request.session['tid'] = username
                        request.session['jrm'] = 'jrm'
                        activity = activitylog()
                        activity.team = user2
                        activity.activitydetails = "Logged In "
                        activity.save()
                        return HttpResponseRedirect('../')
                    else:
                        activity = activitylog()
                        activity.team = request.user
                        activity.activitydetails = "Tried Logging Not Active " + str(user2)
                        activity.save()
                        ldata = {'loginmsg': 'User Not Active'}
                        return render(request, 'asi/login.html', ldata)

                else:
                    activity = activitylog()
                    activity.team = request.user
                    activity.activitydetails = "Wrong Password Login " + str(user2)
                    activity.save()
                    ldata = {'loginmsg': 'Username And Password Did Not Match'}
                    return render(request, 'asi/login.html', ldata)
            except:
                activity = activitylog()
                activity.team = request.user
                activity.activitydetails = "Wrong Password Login " + str(user2)
                activity.save()
                ldata = {'loginmsg': 'Username And Password Did Not Match'}
                return render(request, 'asi/login.html', ldata)



        except:
            ldata = {'loginmsg': "Username And Password Did Not Match"}
            return render(request, 'asi/login.html',ldata)

    else:
        try:
            if request.session['jrm'] == 'jrm':
                return HttpResponseRedirect('../')

        except:
            return render(request, 'asi/login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/asi/login/')
