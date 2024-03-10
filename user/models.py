from django.db import models
import datetime
from django.contrib.auth.models import User
# Create your models here.

class member(models.Model):
    teamid = models.CharField(max_length=7,default="NA")
    mname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phn = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bg = models.CharField(max_length=100)
    year = models.CharField(max_length=4,default="NA")
    gender = models.CharField(max_length=8,default="Unknown")
    profilepic = models.ImageField(upload_to="members/", default="members/male.png")
    idproof = models.ImageField(upload_to="", default="regback..png")
    secret = models.CharField(max_length=128,unique=True)
    memberid = models.CharField(max_length=15,default="NA")


    def __str__(self):
        return self.teamid + "-" + self.mname+"-" +str(self.id)


class faculty(models.Model):
    teamid = models.CharField(max_length=7,default="NA")
    mname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phn = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    bg = models.CharField(max_length=100)
    gender = models.CharField(max_length=8,default="Unknown")
    profilepic = models.ImageField(upload_to="members/", default="members/male.png")
    idproof = models.ImageField(upload_to="", default="regback..png")


    def __str__(self):
        return self.teamid + "-" + self.mname+"-" +str(self.id)


class activitylog(models.Model):
    team = models.ForeignKey(User,on_delete=models.CASCADE)
    activitydetails= models.CharField(max_length=400)
    entered = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.team.username + "-" + self.activitydetails+"-" +str(self.id)


class carnum(models.Model):
    number = models.IntegerField(unique= True)
    booked = models.BooleanField()
    teamid = models.CharField(max_length=7,default="NA")

    def __str__(self):
        return str(self.number) + "-"+ "-" + str(self.teamid)





class gstindetails(models.Model):
    teamid = models.CharField(max_length=7,default="NA")
    lname = models.CharField(max_length=100)
    addrs = models.CharField(max_length=50,default="NA")
    state = models.CharField(max_length=50,default="NA")
    gst = models.CharField(max_length=15,blank=False)
    sc = models.CharField(max_length=2,default="NA")

    class Meta:
        unique_together = ('teamid', 'gst',)

    def __str__(self):
        return self.teamid+"-"+str(self.id)

class payments(models.Model):
    teamid = models.CharField(max_length=7)
    phase = models.CharField(max_length=10)
    time = models.DateTimeField()
    updated = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teamid', 'phase')



    def __str__(self):
        return self.teamid + "-" + self.phase



class invoice(models.Model):
    invoicenumber = models.CharField(max_length=20)
    invoicedate = models.DateTimeField()
    phase = models.CharField(max_length=10,default="NA")
    gstdet = models.ForeignKey(gstindetails, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('gstdet', 'phase')

    def __str__(self):
        return str(self.id)+"-"+str(self.gstdet.teamid)+" - "+str(self.invoicenumber)+" - "+str(self.invoicedate.date())


class verifymobile(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)




class teamdata(models.Model):
    teamid = models.CharField(max_length=7,blank=True)
    teamname = models.CharField(max_length=80,unique= True,blank=True)
    itype = models.CharField(max_length=100)
    iname = models.CharField(max_length=200)
    irec = models.CharField(max_length=100)
    tcap = models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True,default="ASD")
    phn = models.CharField(max_length=13)
    altphn = models.CharField(max_length=13)
    coach = models.CharField(max_length=100)
    size = models.IntegerField(blank=True)
    address = models.CharField(max_length=200)
    otp = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    fblink = models.CharField(max_length=300,blank=True)
    fbactive = models.BooleanField(blank=True)
    payment1 = models.BooleanField(blank=True)
    payment2 = models.BooleanField(blank=True)
    payment1proof = models.ImageField(upload_to='proofs/', blank=True,null=True)
    payment2proof = models.ImageField(upload_to='proofs/', blank=True,null=True)
    carnumber = models.IntegerField(default=0)
    teamlogo = models.ImageField(upload_to='profile/',default='profile/default.png')
    memlimit = models.IntegerField(default=30)
    state = models.CharField(max_length=100,default="NA")
    city = models.CharField(max_length=100,default="NA")
    vtype = models.CharField(max_length=20,default="Combustion")
    rsvp = models.BooleanField(default=False)
    fully_paid = models.BooleanField(default= False)
    balance_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.teamid+"-"+self.teamname+"-"+self.vtype+"--"+str(self.carnumber)+"-"+str(self.fully_paid)+"-"+str(self.balance_amount)+"-"+str(self.rsvp)


