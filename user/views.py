from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from .forms import *
import random, string
from django.contrib import auth, messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime, os
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template import Context

from django.core.files import File


basemed = "/home/ubuntu/mac-07/"



import urllib.request
import urllib.parse
current_year = datetime.datetime.now().year

def sendSMS(apikey, numbers, sender, message):
    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                   'message': message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return (fr)



def base(request):
    return render(request, 'user/base.html')


def customrend(request, temp):
    if request.user.is_authenticated:
        if request.session.get('jrm') == 'jrm':
            team = teamdata.objects.get(teamid=request.session.get('tid'))
            if team.payment1:
                p1 = "Paid"
                p1h = 'btn btn-success btn-icon-w-animt btn-circle '
            else:
                p1 = "Not Paid"
                p1h = 'btn btn-danger btn-icon-w-animt btn-circle'
            if team.payment2:
                p2 = "Paid"
                p2h = 'btn btn-success btn-icon-w-animt btn-circle'
            else:
                p2 = "Not Paid"
                p2h = 'btn btn-danger btn-icon-w-animt btn-circle'
            if team.carnumber == 0:
                carnum = "NA"
            else:
                carnum = team.carnumber

            if team.vtype=="Combustion":
                iselec = False
            else:
                iselec=True
            members = member.objects.filter(teamid=request.session.get('tid'))
            facs = faculty.objects.filter(teamid=request.session.get('tid'))
            act = activitylog.objects.filter(team=request.user).order_by('-entered')
            memnum = member.objects.filter(teamid=request.session.get('tid')).count()
            memnum = int(memnum)
            memper = float(memnum) / 0.3
            tdata = {"tid": team, "p1": p1, "p2": p2, 'cnum': carnum, 'p2h': p2h, 'p1h': p1h, 'tname': team.teamname,
                     'memnum': memnum, 'memper': memper, 'mdata': members, 'fdata': facs, 'log': act,
                     'p1stat': team.payment2,'carnum':team.carnumber,'memlimit':team.memlimit,"pay1":team.payment1,"pay2":team.payment2,"vtype":team.vtype,"iselec":iselec}

            return (request, temp, tdata)
        else:
            return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


def jrmtemp(request):
    for i in range(101, 151):
        num = carnum()
        num.number = i
        num.booked = False
        num.teamid = "NA"
        num.save()
    return HttpResponse("Done")


def carnumber(request):
    (req, temp, tdata) = customrend(request, 'user/carnumbers.html')
    if(tdata['vtype'])=='Combustion':
        tdata['carnums'] = carnum.objects.filter(number__lte=100)
        tdata['iselec']= False
    else:
        car_enum = carnum.objects.filter(number__gt=100)
        tdata['carnums']=car_enum
        # ecarnums=[]
        # for num in car_enum:
        #     ecarnums.append(str(num)[1:])
        # tdata['ecarnums'] = ecarnums
        tdata['iselec'] = True
    num = tdata['cnum']
    if num == "NA":
        tdata['carnumstat'] = False
    else:
        tdata['carnumstat'] = True
    return render(req, temp, tdata)


def confirmcarnum(request):
    (req, temp, tdata) = customrend(request, 'user/carnumbers.html')
    if not tdata['p1stat']:
        return HttpResponseRedirect("/")
    if tdata['carnum'] > 0:
        return HttpResponseRedirect("/")
    num = request.GET['num']
    try:
        numstatus = carnum.objects.get(number=num)
        if numstatus.booked:
            return HttpResponse(
                "<script>alert('Sorry This Number Is Already Booked By Some Other Team.Please Choose Another Number.');window.location.replace('/carnumber/');</script>")
        else:
            numstatus.teamid = request.session.get('tid')
            numstatus.booked = True
            numteam = teamdata.objects.get(teamid=request.session.get('tid'))
            numteam.carnumber = num
            numstatus.save()
            numteam.save()
            return HttpResponse(
                "<script>alert('Car Number Blocked. Click on OK To Check Booking Status.');window.location.replace('/bookingstatus/');</script>")



    except:
        return HttpResponse(
            "<script>alert('Ummm!! Trying To Manipulate The Things.. Its Not That Easy.');window.location.replace('/carnumber/');</script>")


def bookingconf(request):
    team = teamdata.objects.get(teamid=request.session.get('tid'))
    try:
        num = carnum.objects.get(number=team.carnumber)
        num.teamid = request.session.get('tid')
        return HttpResponse("<script>alert('Car Number Booked Succesfully');window.location.replace('/')</script>")
    except:
        return HttpResponse(
            "<script>alert('Booking Failed. Try Again!');window.location.replace('/carnumber/');</script>")


def checkmail(request):
    email = EmailMultiAlternatives(
        'Registration | Mega ATV Championship 2019',
        '',
        'registration@atvchampionship.com',
        ['asilogjrm@gmail.com'],
        ['jrmkvk@gmail.com'],
        reply_to=['mail@autosportsindia.com'],
        headers={'From': ' Mega ATV Championship 2019<registration@atvchampionship.com>'}
    )
    d = {'teamname': 'jrm', 'teamid': "anything", 'password': 'anythong', 'datetime': datetime.datetime.now()}
    htmly = render_to_string('email.html', d)
    email.attach_alternative(htmly, "text/html")
    email.send()
    return HttpResponse("mail sent")


def editprofile(request):
    (req, temp, tdata) = customrend(request, 'user/editprofile.html')
    return render(req, temp, tdata)


def editp(request):
    (req, temp, tdata) = customrend(request, 'user/editprofile.html')
    if request.method == 'POST':
        team = teamdata.objects.get(teamid=request.session.get('tid'))
        team.teamname = request.POST['tname']
        team.tcap = request.POST['cap']
        team.itype = request.POST['itype']
        team.email = request.POST['email']
        team.coach = request.POST['coach']
        team.phn = request.POST['phn']
        team.altphn = request.POST['altphn']
        team.address = request.POST['addrs']
        team.size = request.POST['size']

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage(location=basemed + 'media/profile/')
            filename = request.session.get('tid') + myfile.name
            filename = fs.save(filename, myfile)
            uploaded_file_url = 'profile/' + filename
            team.teamlogo = uploaded_file_url
        except:
            print()

        try:
            team.save()
            activity = activitylog()
            activity.team = request.user
            activity.activitydetails = "Edited Profile"
            activity.save()
            return HttpResponse("<script>alert('Succefully Changed');window.location.replace('/login/')</script>")
        except Exception as e:
            return HttpResponse("<script>alert('Failed');window.location.replace('/login/')</script>")
    else:
        return HttpResponseRedirect('/login/')


def invoicer(request):
    (req, temp, tdata) = customrend(request, 'user/invoicegen.html')

    return render(req, temp, tdata)


def dwninvoice(request):
    phaseg = request.GET['phase']
    try:
        inv = invoice.objects.get(gstdet__teamid=request.session.get('tid'), phase=phaseg)
        p = {}
        gst = "yes"
        print("hi")
        print(inv.gstdet.lname + "gfh")
        if (2==3):
            p['lname'] = inv.gstdet.lname
            p['id'] = inv.invoicenumber
            p['date'] = inv.invoicedate.date()
            p['address'] = inv.gstdet.addrs
            p['state'] = inv.gstdet.state
            p['sc'] = inv.gstdet.sc
            p['phase'] = inv.phase
            p['gstin'] = inv.gstdet.gst
            if (inv.phase == "Phase 1"):
                p['amt'] = 25423.72
                p['tax'] = 4576.28
                p['total'] = 30000
            elif (inv.phase == "Phase 2"):
                p['amt'] = 24576.27
                p['tax'] = 4423.73
                p['total'] = 29000
            print("hhhhh")

        else:
            team = teamdata.objects.get(teamid=inv.gstdet.teamid)
            p['lname'] = team.teamname
            p['id'] = inv.invoicenumber
            p['date'] = inv.invoicedate.date()
            p['address'] = team.address
            p['state'] = "NA"
            p['sc'] = "NA"
            p['gstin'] = "NA"
            if (inv.phase == "Phase 1"):
                p['amt'] = 25423.72
                p['tax'] = 4576.28
                p['total'] = 30000
            elif (inv.phase == "Phase 2"):
                p['amt'] = 24576.27
                p['tax'] = 4423.73
                p['total'] = 29000
                gst = team.teamid
        passon = {'p': p}

        return render(request, 'user/invoice.html', passon)
    except:
        return HttpResponse("<script> alert('Some Error Occured');window.location.assign('user.atvchampionship.com');")


def payinfo(request):
    (req, temp, tdata) = customrend(request, 'user/paymentinfo.html')
    try:
        paym1 = payments.objects.get(teamid=request.session.get('tid'), phase='Phase 1')
        tdata['paym1'] = True
        tdata['paym1time'] = paym1.time
    except:
        tdata['paym1'] = False

    try:
        paym2 = payments.objects.get(teamid=request.session.get('tid'), phase="Phase 2")
        tdata['paym2'] = True
        tdata['paym2time'] = paym2.time
    except:
        tdata['paym2'] = False
    return render(request, 'user/paymentinfo.html', tdata)


def mydb(request):
    import sqlite3
    conn1 = sqlite3.connect('data.sqlite')
    cursor = conn1.execute("SELECT * FROM treg")

    for row in cursor:
        email = row[8]
        password = row[12]
        teamname = row[2]
        itype = row[4]
        iname = row[5]
        irec = row[6]
        tcap = row[7]
        phn = row[9]
        altphn = "NA"
        coach = row[10]
        size = row[11]
        address = row[13]

        newteam = teamdata()
        newteam.email = email
        newteam.address = address
        newteam.altphn = altphn
        newteam.coach = coach
        newteam.iname = iname
        newteam.irec = irec
        newteam.phn = phn
        newteam.itype = itype
        newteam.teamname = teamname
        newteam.tcap = tcap
        newteam.size = size
        newteam.otp = random.randint(1000000, 9999999)
        newteam.active = True
        newteam.fbactive = False
        newteam.payment1 = False
        newteam.payment2 = False
        newteam.teamid = row[1]
        usertable = User()
        usertable.username = row[1]
        usertable.email = email
        usertable.first_name = teamname
        usertable.set_password(password)
        print(password)

        newteam.save()
        usertable.save()
        print("done")

    return HttpResponse("Done")


def simple_upload(request):
    (req, temp, tdata) = customrend(request, 'user/payment.html')
    try:
        paym1 = payments.objects.get(teamid=request.session.get('tid'), phase='Phase 1')
        tdata['paym1'] = True
        tdata['paym1time'] = paym1.time
    except:
        tdata['paym1'] = False

    try:
        paym2 = payments.objects.get(teamid=request.session.get('tid'), phase="Phase 2")
        tdata['paym2'] = True
        tdata['paym2time'] = paym2.time
    except:
        tdata['paym2'] = False
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        phase = request.POST['phase']
        fs = FileSystemStorage(location=basemed + 'media/proofs/')
        filename = request.session.get('tid') + phase + myfile.name
        filename = fs.save(filename, myfile)
        uploaded_file_url = 'proofs/' + filename
        team = teamdata.objects.get(teamid=request.session.get('tid'))
        pr = payments()
        lname = "request.POST['lname']"
        addr = "request.POST['addr']"
        state = "request.POST['state']"
        gst = "NA"
        scode = "NA]"

        gstmodel = gstindetails()
        gstmodel.teamid = request.session.get('tid')
        gstmodel.lname = lname
        gstmodel.addrs = addr
        gstmodel.state = state
        gstmodel.gst = gst
        gstmodel.sc = scode
        try:
            pr.teamid = request.session.get('tid')
            pr.phase = phase
            pr.time = datetime.datetime.now()
            pr.save()
            if phase == "Phase 1":
                team.payment1proof = uploaded_file_url
            else:
                team.payment2proof = uploaded_file_url

            team.save()
            tdata['uploaded_file_url'] = "Request Submitted"
        except:
            tdata['uploaded_file_url'] = "Request Failed"

        try:
            gstmodel.save()
            activity = activitylog()
            activity.team = request.user
            activity.activitydetails = "Submitted Payment Details Of " + str(phase)
            activity.save()
            tdata['gstsave'] = "GST Details Submitted"
        except:
            tdata['gstsave'] = "GST Details Submision Failed"

        return render(req, temp, tdata)

    return render(request, temp, tdata)




def index(request):
    if request.user.is_authenticated:
        try:
            (req, temp, tdata) = customrend(request, 'user/index.html')
            return render(req, temp, tdata)
        except:
            return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')


def editteam(request):
    (req, temp, tdata) = customrend(request, 'user/editteam.html')
    currmem = member.objects.get(id=request.GET.get('member'), teamid=request.session.get('tid'))
    tdata['currmem'] = currmem
    if currmem:
        if request.session.get('tid') == currmem.teamid:
            return render(req, temp, tdata)
        else:
            return HttpResponse("<script>alert('Member Is Not Of Your Team')</script>")
    else:
        return HttpResponse("<script>alert('Member Does Not Exist')</script>")


def editfaculty(request):
    (req, temp, tdata) = customrend(request, 'user/editfaculty.html')
    currmem = faculty.objects.get(id=request.GET.get('member'), teamid=request.session.get('tid'))
    tdata['currmem'] = currmem
    if currmem:
        if request.session.get('tid') == currmem.teamid:
            return render(req, temp, tdata)
        else:
            return HttpResponse("<script>alert('Faculty Is Not Of Your Team')</script>")
    else:
        return HttpResponse("<script>alert('Faculty Does Not Exist')</script>")


def editmem(request):
    (req, temp, tdata) = customrend(request, 'user/addteam.html')
    mem = member.objects.get(id=request.POST['id'], teamid=request.session.get('tid'))
    mem.mname = request.POST['mname']
    mem.email = request.POST['email']
    mem.phn = request.POST['phn']
    mem.age = request.POST['age']
    mem.role = request.POST['role']
    mem.bg = request.POST['bg']
    mem.year = request.POST['year']
    mem.gender = request.POST['gen']

    if mem.gender == "Male":
        mem.profilepic = "members/male.png"
    else:
        mem.profilepic = "members/female.png"
    try:
        myfile = request.FILES['mempic']
        if myfile.size > 2097152:
            return HttpResponse("<script>alert('File More Than 2MB.');window.location.assign('/viewteam/')</script>")

        fs = FileSystemStorage(location=basemed + 'media/members/')
        filename = request.session.get('tid') + str(datetime.date.today()) + myfile.name
        filename = fs.save(filename, myfile)
        uploaded_file_url = 'members/' + filename
        mem.profilepic = uploaded_file_url
    except:
        print()

    try:
        myfile = request.FILES['idproof']
        if myfile.size > 2097152:
            return HttpResponse("<script>alert('File More Than 2MB.');window.location.assign('/viewteam/')</script>")
        fs = FileSystemStorage(location=basemed + 'media/members/')
        filename = request.session.get('tid') + str(datetime.date.today()) + myfile.name
        filename = fs.save(filename, myfile)
        uploaded_file_url = 'members/' + filename
        mem.idproof = uploaded_file_url
    except:
        print()

    try:

        mem.save()
        activity = activitylog()
        activity.team = request.user
        activity.activitydetails = "Edited " + str(mem.mname)
        activity.save()
        return HttpResponse(
            "<script>alert('Member Updated Succesfully.');window.location.assign('/viewteam/')</script>")
    except Exception as e:
        activity = activitylog()
        activity.team = request.user
        activity.activitydetails = "Tried Editing " + str(mem.mname)
        activity.save()
        return HttpResponse("<script>alert('Member Updated Failed.');window.location.assign('/viewteam/')</script>")


def editfac(request):
    (req, temp, tdata) = customrend(request, 'user/addfaculty.html')
    mem = faculty.objects.get(id=request.POST['id'], teamid=request.session.get('tid'))
    mem.mname = request.POST['mname']
    mem.email = request.POST['email']
    mem.phn = request.POST['phn']
    mem.age = request.POST['age']
    mem.role = request.POST['role']
    mem.bg = request.POST['bg']
    mem.gender = request.POST['gen']

    if mem.gender == "Male":
        mem.profilepic = "members/male.png"
    else:
        mem.profilepic = "members/female.png"
    try:
        myfile = request.FILES['mempic']
        if myfile.size > 2097152:
            return HttpResponse("<script>alert('File More Than 2MB.');window.location.assign('/viewteam/')</script>")
        fs = FileSystemStorage(location=basemed + 'media/members/')
        filename = request.session.get('tid') + str(datetime.date.today()) + myfile.name
        filename = fs.save(filename, myfile)
        uploaded_file_url = 'members/' + filename
        mem.profilepic = uploaded_file_url
    except:
        print()

    try:
        myfile = request.FILES['idproof']
        if myfile.size > 2097152:
            return HttpResponse("<script>alert('File More Than 2MB.');window.location.assign('/viewteam/')</script>")
        fs = FileSystemStorage(location=basemed + 'media/members/')
        filename = request.session.get('tid') + str(datetime.date.today()) + myfile.name
        filename = fs.save(filename, myfile)
        uploaded_file_url = 'members/' + filename
        mem.idproof = uploaded_file_url
    except:
        print()

    try:

        mem.save()
        activity = activitylog()
        activity.team = request.user
        activity.activitydetails = "Edited Faculty " + str(mem.mname)
        activity.save()
        return HttpResponse("<script>alert('Updated Succesfully.');window.location.assign('/viewfaculty/')</script>")
    except Exception as e:
        mem.save()
        activity = activitylog()
        activity.team = request.user
        activity.activitydetails = "Tried Editing Faculty " + str(mem.mname)
        activity.save()
        return HttpResponse("<script>alert('Updated Failed.');window.location.assign('/viewfaculty/')</script>")


def deletemem(request):
    (req, temp, tdata) = customrend(request, 'user/editteam.html')
    try:
        memdel = member.objects.get(id=request.GET.get('member'), teamid=request.session.get('tid'))
        if memdel.delete():
            activity = activitylog()
            activity.team = request.user
            activity.activitydetails = "Deleted Member " + str(memdel.mname)
            activity.save()
            return HttpResponse("<script>alert('Deleted');window.location.replace('/viewteam/')</script>")
        else:
            activity = activitylog()
            activity.team = request.user
            activity.activitydetails = "Tried Deleting " + str(memdel.mname)
            activity.save()
            return HttpResponse(
                "<script>alert('Unable To Delete Member,Please Contact Administrator');window.location.replace('/viewteam/')</script>")
    except:
        return HttpResponse(
            "<script>alert('This Member Does not Belong To Your Team');window.location.replace('/viewteam/')</script>")


def deletefac(request):
    (req, temp, tdata) = customrend(request, 'user/editteam.html')
    try:
        memdel = faculty.objects.get(id=request.GET.get('member'), teamid=request.session.get('tid'))
        if memdel.delete():
            activity = activitylog()
            activity.team = request.user
            activity.activitydetails = "Deleted Faculty " + str(memdel.mname)
            activity.save()
            return HttpResponse("<script>alert('Deleted');window.location.replace('/viewteam/')</script>")
        else:
            activity = activitylog()
            activity.team = request.user
            activity.activitydetails = "Tried Deleting Faculty " + str(memdel.mname)
            activity.save()
            return HttpResponse(
                "<script>alert('Unable To Delete Member,Please Contact Administrator');window.location.replace('/viewfaculty/')</script>")
    except:
        return HttpResponse(
            "<script>alert('This Member Does not Belong To Your Team');window.location.replace('/viewfaculty/')</script>")


def viewlor(request):
    try:
        teamd = teamdata.objects.get(teamid=request.session.get('tid'))
        print(teamd)
        print(teamd.teamname)
        if teamd.payment1:
            ref = "Ref: ASI/BBSR/ADMN/" + str(teamd.teamid[:4]) + " /2019"
            passon = {"lordate": datetime.datetime.now().date(), "teamname": teamd.teamname, "collegename": teamd.iname,
                      "address": teamd.address, "refnum": ref}
            return render(request, "user/lor.html", passon)
        else:
            return HttpResponse(
                "<script> alert('Please Pay First Phase To Generate LOR');window.location.assign('http://user.atvchampionship.com');</script>")


    except:
        return HttpResponse(
            "<script> alert('Some Error Occured');window.location.assign('http://user.atvchampionship.com');</script>")


def viewmember(request):
    (req, temp, tdata) = customrend(request, 'user/viewteam.html')
    return render(req, temp, tdata)


def comingsoon(request):
    return HttpResponse(
        "<script>alert('This Feature Will Be Available Soon And Will Be Notified Through Mail');window.location.replace('/login/');</script>");


def viewfaculty(request):
    (req, temp, tdata) = customrend(request, 'user/viewfaculty.html')
    return render(req, temp, tdata)


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
                        return render(request, 'user/login.html', ldata)

                else:
                    activity = activitylog()
                    activity.team = request.user
                    activity.activitydetails = "Wrong Password Login " + str(user2)
                    activity.save()
                    ldata = {'loginmsg': 'Username And Password Did Not Match'}
                    return render(request, 'user/login.html', ldata)
            except:
                activity = activitylog()
                activity.team = request.user
                activity.activitydetails = "Wrong Password Login " + str(user2)
                activity.save()
                ldata = {'loginmsg': 'Username And Password Did Not Match'}
                return render(request, 'user/login.html', ldata)



        except:
            ldata = {'loginmsg': "Username And Password Did Not Match"}
            return render(request, 'user/login.html', ldata)

    else:
        try:
            if request.session['jrm'] == 'jrm':
                return HttpResponseRedirect('../')

        except:
            return render(request, 'user/login.html')


def addteam(request):
    (req, temp, tdata) = customrend(request, 'user/addteam.html')
    if request.method == 'POST':
        if member.objects.filter(teamid=request.session.get('tid')).count() >= tdata['memlimit']:
            tdata['addmsg'] = "Maximum 30 Members Are Allowed"
            return render(req, temp, tdata)
        else:
            mem = member()
            randomk = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(128)])
            mem.teamid = request.session.get('tid')
            mem.mname = request.POST['mname']
            mem.email = request.POST['email']
            mem.phn = request.POST['phn']
            mem.age = request.POST['age']
            mem.role = request.POST['role']
            mem.bg = request.POST['bg']
            mem.year = request.POST['year']
            mem.gender = request.POST['gen']
            last = member.objects.last()
            newid = last.id + 1
            newidstr = str(newid)
            teamidtemp = newidstr.zfill(5)
            mem.memberid = "ASI/" + str(datetime.datetime.now().year) + "/" + teamidtemp

            if mem.gender == "Male":
                mem.profilepic = "members/male.png"
            else:
                mem.profilepic = "members/female.png"
            try:
                myfile = request.FILES['mempic']
                if myfile.size > 2097152:
                    tdata['addmsg'] = "File More Than 2 MB"
                    return render(req, temp, tdata)
                fs = FileSystemStorage(location=basemed + 'media/members/')
                filename = request.session.get('tid') + str(datetime.date.today()) + myfile.name
                filename = fs.save(filename, myfile)
                uploaded_file_url = 'members/' + filename
                mem.profilepic = uploaded_file_url
            except:
                print()

            try:
                myfile = request.FILES['idproof']
                if myfile.size > 2097152:
                    tdata['addmsg'] = "File More Than 2 MB"
                    return render(req, temp, tdata)
                fs = FileSystemStorage(location=basemed + 'media/members/')
                filename = request.session.get('tid') + str(datetime.date.today()) + myfile.name
                filename = fs.save(filename, myfile)
                uploaded_file_url = 'members/' + filename
                mem.idproof = uploaded_file_url
            except:
                print()
            email = EmailMultiAlternatives(
                f'Members | Mega ATV Championship {current_year}',
                '',
                'registration@atvchampionship.com',
                [mem.email],
                [],
                reply_to=['mail@autosportsindia.com'],
                headers={'From': f' Mega ATV Championship {current_year}<registration@atvchampionship.com>'}
            )
            d = {'tname': tdata['tname'], 'mname': mem.mname, 'skey': randomk, 'memid': mem.memberid}
            htmly = render_to_string('useremail.html', d)
            email.attach_alternative(htmly, "text/html")
            randomk = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(128)])
            mem.secret = randomk

            try:
                mem.save()
                activity = activitylog()
                activity.team = request.user
                activity.activitydetails = "Added Member " + str(mem.mname)
                activity.save()
                email.send()
                tdata['addmsg'] = "Member Added Succesfully"
            except Exception as e:
                try:
                    randomk = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(128)])
                    mem.secret = randomk
                    mem.save()
                    activity = activitylog()
                    activity.team = request.user
                    activity.activitydetails = "Added Member " + str(mem.mname)
                    activity.save()
                    email.send()
                    tdata['addmsg'] = "Member Added Succesfully"
                except:
                    activity = activitylog()
                    activity.team = request.user
                    activity.activitydetails = "Tried Adding " + str(mem.mname)
                    activity.save()
                    tdata['addmsg'] = "Member Adding Failed"

    return render(req, temp, tdata)


def addfac(request):
    (req, temp, tdata) = customrend(request, 'user/addfac.html')
    if request.method == 'POST':
        if faculty.objects.filter(teamid=request.session.get('tid')).count() >= 2:
            tdata['addmsg'] = "Maximum 2 Faculty Are Allowed"
            return render(req, temp, tdata)
        else:
            mem = faculty()
            mem.teamid = request.session.get('tid')
            mem.mname = request.POST['mname']
            mem.email = request.POST['email']
            mem.phn = request.POST['phn']
            mem.age = request.POST['age']
            mem.bg = request.POST['bg']
            mem.gender = request.POST['gen']
            if mem.gender == "Male":
                mem.profilepic = "members/male.png"
            else:
                mem.profilepic = "members/female.png"
            try:
                myfile = request.FILES['mempic']
                if myfile.size > 2097152:
                    tdata['addmsg'] = "File More Than 2 MB"
                    return render(req, temp, tdata)
                fs = FileSystemStorage(location=basemed + 'media/members/')
                filename = request.session.get('tid') + str(datetime.date.today()) + myfile.name
                filename = fs.save(filename, myfile)
                uploaded_file_url = 'members/' + filename
                mem.profilepic = uploaded_file_url
            except:
                print()

            try:
                myfile = request.FILES['idproof']
                if myfile.size > 2097152:
                    tdata['addmsg'] = "File More Than 2 MB"
                    return render(req, temp, tdata)
                fs = FileSystemStorage(location=basemed + 'media/members/')
                filename = request.session.get('tid') + str(datetime.date.today()) + myfile.name
                filename = fs.save(filename, myfile)
                uploaded_file_url = 'members/' + filename
                mem.idproof = uploaded_file_url
            except:
                print()

            try:
                mem.save()
                activity = activitylog()
                activity.team = request.user
                activity.activitydetails = "Added Faculty " + str(mem.mname)
                activity.save()
                tdata['addmsg'] = "Added Succesfully"
            except Exception as e:
                activity = activitylog()
                activity.team = request.user
                activity.activitydetails = "Tried Adding Faculty " + str(mem.mname)
                activity.save()
                tdata['addmsg'] = "Adding Failed"

    return render(req, temp, tdata)


def logout(request):
    auth.logout(request)
    messages.success(request, "Member Added")
    return HttpResponseRedirect('/login/')


def portalclosed(request):
    return HttpResponse("<script>alert('Portal Closed.Data Modification is not Allowed Anymore.');window.location.replace('http://user.atvchampionship.com');</script>")

def teamreg(request):
    return HttpResponseRedirect('/registerteam')

import json
import urllib3
import requests
def newreg(request):
    if request.method == 'POST':
        recap = request.POST.get('g-recaptcha-response')
        recapurl = 'https://www.google.com/recaptcha/api/siteverify'
        recapvalues = {
            'secret': '6LcG6SMTAAAAAAlbpd_gz29DKMQvQGTGo82umLrQ',
            'response': recap
        }
        verify_rs = requests.get(recapurl,params=recapvalues)
        verify_rs = verify_rs.json()
        status = verify_rs.get("success", False)
        if not status:
            messages.error(request, "Validate Recapthca")
            return render(request,'user/register.html')


        receivername = request.POST['mname']
        receiverphn = request.POST['phone']
        otp = random.randint(100000, 999999)
        msg = "Dear%20Team,%nYour%20OTP%20For%20Completing%20MAC%20Season-5%20Registration%20is:%20"+str(otp)+"%n%20%nVisit%20:%20https://atvchampionship.com%20for%20more%20details."
        print(msg)
        # otpobj = verifymobile()
        # otpobj.name = receivername
        # otpobj.mobile = receiverphn
        # otpobj.otp = otp
        # otpobj.save()
        # resp = sendSMS('O5zrBuXWaCU-8n8EpziTEQoR4hYoyoAEz523WENLUb', receiverphn, 'MACGOA', msg)
        # resp = json.loads(str(resp,'utf-8'))
        request.session['jrmtp'] = otp
        request.session['phn'] = receiverphn
        if True:
                return HttpResponse("<script>window.location.replace('/verify-otp/')</script>")
        else:
            messages.error(request,"Error Sending Message")
            return render(request,'user/register.html')


    else:
        return render(request,'user/register.html')

def verifyotp(request):
    """if request.method == 'POST':
        print(request.POST['otp'])
        print(request.session['jrmtp'])
        if int(request.POST['otp']) == int(request.session['jrmtp']):
            request.session['verified']=True
            return HttpResponseRedirect('/teamdetails/')
        else:
            messages.error(request,"Incorrect OTP")
            return render(request, 'user/verifyotp.html')
    else:
        return render(request,'user/verifyotp.html')"""
    request.session['verified'] = True
    return HttpResponseRedirect('/teamdetails/')



def teamdetails(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']
        teamname = request.POST['team_name']
        itype = request.POST['payment']
        iname = request.POST['college_name']
        irec = request.POST['recby']
        tcap = request.POST['cap_name']
        phn = request.session['phn']
        altphn = request.POST['phone_number']
        coach = request.POST['coach_name']
        size = request.POST['size']
        address = request.POST['addrs']
        state = request.POST['state']
        city = request.POST['city']
        vtype = request.POST['vtype']
        print(vtype+"---------------------------")


        newteam = teamdata()
        last = teamdata.objects.last()
        newteam.email = email
        newteam.address = address
        newteam.altphn = altphn
        newteam.coach = coach
        newteam.iname = iname
        newteam.irec = irec
        newteam.phn = phn
        newteam.itype = itype
        newteam.teamname = teamname
        newteam.tcap = tcap
        newteam.size = size
        newteam.otp = random.randint(1000000, 9999999)
        newteam.active = True
        newteam.fbactive = False
        newteam.payment1 = False
        newteam.payment2 = False
        newid = last.id+120
        newidstr = str(newid)
        newteam.state = state
        newteam.city = city
        newteam.vtype = vtype
        teamidtemp = newidstr.zfill(4)
        newteam.teamid = "MAC" + teamidtemp
        usertable = User()
        usertable.username = "MAC" + teamidtemp
        usertable.email = email
        usertable.first_name = teamname
        usertable.set_password(password)

        email = EmailMultiAlternatives(
            f'Registration | Mega ATV Championship {current_year}',
            '',
            'registration@atvchampionship.com',
            [email, 'reg@atvchampionship.com','reg@autosportsindia.com'],
            [],
            reply_to=['mail@autosportsindia.com'],
            headers={'From': f' Mega ATV Championship {current_year}<registration@atvchampionship.com>'}
        )
        d = {'teamname': teamname, 'teamid': newteam.teamid, 'password': password,
             'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'otp': newteam.otp}
        htmly = render_to_string('email.html', d)
        email.attach_alternative(htmly, "text/html")
        print("MAILLLLsds")
        email.send()
        try:
            print("Trying MAIL")
            exist = teamdata.objects.get(email=usertable.email)
            messages.error(request, "Email Already Registered")
            return render(request, 'user/regdatainp.html')
        except Exception as e:
            print(e)
            sadata = {'signupmsg': "Email Available For Registration"}

        try:
            try:
                phn = teamdata.objects.get(phn=phn)
                messages.error(request, "Phone Number Already Exists")
                return render(request,'user/regdatainp.html')
            except:
                newteam.save()
                usertable.save()
                try:

                    return HttpResponse(f"<script>alert('Thank You for registering for Mega ATV Championship {current_year}. Please check your mail for details.');window.location.assign('/login/')</script>")
                except:
                    return HttpResponse(
                       f"<script>alert('Thank You for registering for Mega ATV Championship {current_year}. Unable to send mail.Please contact 7978555567.');window.location.assign('/login/')</script>")
        except Exception as e:
            return HttpResponse(
                "<script>alert('Registration Failed, Please Contact 7978555567');window.location.assign('/login/')</script>")

    else:
        try:
            if request.session['verified']:
                return render(request, 'user/regdatainp.html')
        except:
            return HttpResponseRedirect('/registerteam/')
