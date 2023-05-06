from multiprocessing import context
from pickle import NONE
import django
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import journeyDetails, Loggedin, contactinfo
from django.core.mail import send_mail
import math
import random
from django_otp.oath import totp
from django_otp.util import random_hex
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import datetime
from datetime import timedelta
from datetime import date
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from dateutil.relativedelta import relativedelta
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import time
from django_otp.oath import TOTP

# Create your views here.
# from django.template import loader


# def index(request):
#     return render(request, 'index.html')
# global m
# global u1

def logout(request):
    
    user_id = request.session.get('username')
    auth.logout(request)
    request.session.flush()
    if user_id:
        request.session['username'] = user_id
    return redirect('Login')


def register(request):
    
    if request.method == 'POST':
        username = request.POST['username']
       
        email = request.POST['email']
      
        password = request.POST['password']
        
        password1 = request.POST['password1']

        if "@gmail.com" in email:
            if password == password1:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already registered')
                    return render(request, 'register.html')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists')
                    return render(request, 'register.html')
                else:
                    request.session['username'] = username
                    request.session['password'] = password
                    request.session['email'] = email
                    m = request.session.get('email')
                    otp_code = random_hex(length=6)
                    request.session['otp_code'] = otp_code

                    htmlgen = '<p>Your OTP is <strong>'+otp_code+'</strong></p>'
                    send_mail('OTP request', otp_code, 'rtritik09@gmail.com',
              [m], fail_silently=False, html_message=htmlgen)
                    # return render(request, 'otp.html')
                    
                    return redirect('otp')
            else:
                messages.info(request, 'Password are not same')
                return render(request, 'register.html')
        else:
            messages.info(request, 'Please register with your IITK email ID')
            return render(request, 'register.html')

    else:

        return render(request, 'register.html')


# u2 = "ritik"
# GLOBAL_VARIABLE = NONE

# r = "devanshs20@iitk.ac.in"


def Login(request):
    global u2
    # global r
    if request.method == 'POST':
        username = request.POST['username']
        u2 = username
        password = request.POST['password']

        user = auth.authenticate(username=u2, password=password)

        if user is not None:
            auth.login(request, user)
            # sv1 = Loggedin(loggedin=username,
            #                time=datetime.now().time(), date=datetime.now().date())
            # sv2 = journeyDetails(username=username)
            # sv1.save()
            # sv2.save()
            # r = searchuser(user.username)
            request.session['username'] = username
            return redirect('dash')
        else:

            messages.info(request, 'Credentials Invalid')
            return redirect('Login')

    else:
        return render(request, 'Login.html')


# def delogin(request,*u2):
#     if request.user.is_authenticated:
#         log = Loggedin.objects.filter(loggedin=u2)
#         log.delete()
#         return redirect('Login')

@login_required
def saver(request):
    if request.method == "POST":
        name = request.POST.get('name')
        hall = request.POST.get('hall')
        date = request.POST.get('date')
        # n = parse_datetime(date)
        # g = n.day
        time = request.POST.get('time')
        # format = '%I:%M%p'
        pr = str(date) + ' ' + str(time)
        format = '%Y-%m-%d %H:%M'  # The format
        comtime = datetime.strptime(pr, format)
        #t = datetime.datetime.strptime(time, format)
        #comtime = datetime.datetime.combine(n, t)
        Blocation = request.POST.get('Blocation')
        Dlocation = request.POST.get('Dlocation')
        cityfrom = request.POST.get('cityfrom')
        cityto = request.POST.get('cityto')
        contact = request.POST.get('phone')
        comment = request.POST.get('comment')
        # username = Loggedin.objects.last()
        # send_journeykey()
        # print(request.user.get_username())
        sv = journeyDetails(id=generateOTP(),username=request.user.get_username(), name=name, hall=hall, date=date,
                            time=time, comtime=comtime, Blocation=Blocation, Dlocation=Dlocation, cityfrom=cityfrom, cityto=cityto, phone=contact, comments=comment)
        sv.save()

        # messages.success(request, 'Data Saved')

        return redirect('dash')
    else:
        return render(request, 'saver.html')


# def searchuser(u2):
#     global d
#     keyuser = User.objects.get(username=u2)
#     keyemail = keyuser.email
#     d = keyemail
#     return d


@login_required
def search(request):
    if request.method == "POST":
        key = request.POST.get('key')
        if not journeyDetails.objects.filter(id=key).exists():
            messages.info(request, "Please Enter correct key")
            return render(request, "search.html")
        data = journeyDetails.objects.get(id=key)
        date = (data.date)
        datet = (data.comtime)
        slocation = data.Blocation
        flocation = data.Dlocation
        #ctime = journeyDetails.objects.values_list( 'comtime', flat=True)
        #dt = datetime.combine(date, time)
        # dt=(data.comtime)
        next_t = datet+(timedelta(hours=+6, minutes=+0, seconds=+0))
        prev_t = datet+(timedelta(hours=-6, minutes=-0, seconds=-0))
        #dateid = (data.dayid)
        #prev = int(dateid)-1
        #next = int(dateid)+1
        # dt = datetime.datetime.strptime(str(date), '%Y-%m-%d')
        # min_dt = (dt - timedelta(hours=24))
        # max_dt = (dt + timedelta(hours=24))
        # info = journeyDetails.objects.filter((Q(dayid=dateid) | Q(dayid=prev) | Q(
        #    dayid=next)) & (Q(comtime=prev_t) & Q(comtime=next_t)))

        info = journeyDetails.objects.filter(comtime__range=(prev_t, next_t))
        if journeyDetails.objects.filter(Q(date=date) & Q(Blocation=slocation) & Q(Dlocation=flocation)).exists():
            return render(request, 'Result.html', {'data': info})
        else:
            messages.info(request, 'No journey for this date')
            return render(request,'dash.html')
    else:
        return render(request, 'search.html')


@login_required
def Result(request):
    return render(request, 'Result.html')


def home(request):
    return render(request, 'home.html')


@login_required
def trips(request):
    # if request.method == "POST":
    # phone = request.POST.get('phone')
    data = journeyDetails.objects.filter(username=request.user.get_username())
    if journeyDetails.objects.filter(username=request.user.get_username()).exists():
        return render(request, 'getid.html', {'data': data})
    else:
        # messages.info(request, 'You have not any trip')
        return redirect('dash')


@login_required
def dash(request):

    return render(request, 'dash.html')


# global no
# no = 0


def otp(request):

    if request.method == "POST":

        otp = request.POST.get('otp')
        otp_code = request.session.get('otp_code')
        totp = TOTP(otp_code.encode())
        totp_token = totp.token()
        u1=request.session.get('username')
        m=request.session.get('email')
        p1=request.session.get('password')
        if otp_code == otp:
            user = User.objects.create_user(
                username=u1, email=m, password=p1)
            user.save()
            # del request.session['u1']
            # del request.session['m']
            # del request.session['p1']
            return redirect('Login')
        else:
            # del request.session['u1']
            # del request.session['m']
            # del request.session['p1']
            return HttpResponse('Invalid OTP')
    else:

        return render(request, 'otp.html')

def generateOTP():
    digits = "abcdefghijklmnopqrstuvwxyz"
    OTP = ""

    for i in range(4):
         OTP += digits[math.floor(random.random() * 10)]

    return OTP


# def send_otp(request):
#     otp_code = random_hex(length=6)
#     request.session['otp_code'] = otp_code

#     htmlgen = '<p>Your OTP is <strong>'+otp_code+'</strong></p>'
#     send_mail('OTP request', otp_code, 'rtritik09@gmail.com',
#               [m], fail_silently=False, html_message=htmlgen)
#     return HttpResponse(otp_code)


# def send_journeykey(request):
#     o = generateOTP()
#     htmlgen = '<p>Hi, Your unique key for just saved journey details is <strong>'+o+'</strong></p>'
#     send_mail('Journey Key request', o, 'rtritik09@gmail.com',
#               [request.user.email], fail_silently=False, html_message=htmlgen)
#     return HttpResponse(o)


# def dates(request, *u2):

#     data = journeyDetails.objects.filter(username=u2)
#     if journeyDetails.objects.filter(username=u2).exists():
#         return render(request, 'dates.html', {'data': data})
#     else:
#         messages.info(request, 'You have not any registered trip')
#         return redirect('dash')

# def home1(request):
#     return render(request, "home1.html")


def contact(request):
    if request.method == "POST":
        name = request.POST['Name']
        email = request.POST['Email']
        subject = request.POST['Subject']
        message = request.POST['Message']
        det = contactinfo(name=name, email=email,
                          subject=subject, message=message)
        det.save()
        messages.info(request, 'We Will Get In Touch With You Soon')
        return render(request, 'home.html')
    else:
        return render(request, 'home.html')
