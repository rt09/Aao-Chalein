from multiprocessing import context
from pickle import NONE
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import journeyDetails
from django.core.mail import send_mail
import math
import random
from django.conf import settings
from django.core.mail import EmailMessage, get_connection

# Create your views here.
# from django.template import loader


# def index(request):
#     return render(request, 'index.html')
# global m
# global u1


def register(request):
    global m
    global u1
    if request.method == 'POST':
        username = request.POST['username']
        u1 = username
        email = request.POST['email']
        m = email
        password = request.POST['password']
        password1 = request.POST['password1']

        if "@iitk.ac.in" in email:
            if password == password1:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already registered')
                    return redirect('register')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username=username, email=email, password=password)
                    user.save()
                    send_otp()
                    return redirect('otp')

            else:
                messages.info(request, 'Password are not same')
                return redirect('register')
        else:
            messages.info(request, 'please register with your IITK email ID')
            return redirect('register')

    else:

        return render(request, 'register.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dash')
        else:

            messages.info(request, 'Credentials Invalid')
            return redirect('Login')

    else:
        return render(request, 'Login.html')


def save(request):
    if request.method == "POST":
        name = request.POST.get('name')
        hall = request.POST.get('hall')
        date = request.POST.get('date')
        time = request.POST.get('time')
        Blocation = request.POST.get('Blocation')
        Dlocation = request.POST.get('Dlocation')
        phone = request.POST.get('phone')
        sv = journeyDetails(name=name, hall=hall, date=date,
                            time=time, Blocation=Blocation, Dlocation=Dlocation, phone=phone)
        sv.save()
        messages.success(request, 'Data Saved')
        return redirect('search')
    else:
        return render(request, 'save.html')


def search(request):
    if request.method == "POST":
        date = request.POST.get('date')

        data = journeyDetails.objects.filter(date=date)
        if journeyDetails.objects.filter(date=date).exists():
            return render(request, 'Result.html', {'data': data})
        else:
            messages.info(request, 'No journey for this date')
            return redirect('search')
    else:
        return render(request, 'search.html')


def Result(request):
    return render(request, 'Result.html')


def home(request):
    return render(request, 'home.html')


def trips(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        data = journeyDetails.objects.filter(phone=phone)
        if journeyDetails.objects.filter(phone=phone).exists():
            return render(request, 'Result.html', {'data': data})
        else:
            messages.info(request, 'You have not any trip')
            return redirect('trips')
    else:
        return render(request, 'trips.html')


def dash(request):

    return render(request, 'dash.html')


# global no
# no = 0


def otp(request):

    if request.method == "POST":

        otp = request.POST.get('otp')
        if(int(otp) == int(c)):
            return redirect('Login')
        else:
            u = User.objects.filter(username=u1)
            u.delete()
            return HttpResponse('Invalid OTP')
    else:

        return render(request, 'otp.html')


def generateOTP():
    digits = "0123456789"
    OTP = ""
    global c

    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]

    c = OTP

    return OTP


def send_otp():
    o = generateOTP()
    htmlgen = '<p>Your OTP is <strong>'+o+'</strong></p>'
    send_mail('OTP request', o, 'rtritik09@gmail.com',
              [m], fail_silently=False, html_message=htmlgen)
    return HttpResponse(o)


# def home1(request):
#     return render(request, "home1.html")
