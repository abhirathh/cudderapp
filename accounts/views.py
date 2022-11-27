import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
import math, random
import datetime
import hashlib
import json
from .models import userApiConfig
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        # password2 = request.POST['password2']
        email = request.POST['email']

        ct = datetime.datetime.now()

        timestamp = str(ct)

        # if password1 != password2:
        #     messages.info(request, "Passwords don't match")
        #     return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email alreay registered')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
            user.save()

            hashCombinations = str(username) + str(timestamp)
            hashApiKey = hashlib.sha256(hashCombinations.encode()).hexdigest()

            print(timestamp)
            userApiConfig.objects.create(username = username,
                                        api_key = str(hashApiKey),
                                        timestamp = timestamp)
            print(timestamp)
            return redirect('login')
    else:
        return render(request, 'accounts/register.html')

### Login ###
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(f'/api/dashboard')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

###Logout###
def logout(request):
    auth.logout(request)
    return redirect('/accounts/login')

### forgotPassword ###
def forgotPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        usermail = request.POST['usermail']

        fetchUserDb = User.objects.filter(username = username, email = usermail)
        print(username)
        print(usermail)

        if fetchUserDb:
            forgotPassMessage('success')
            print('Here')

            return redirect('/')
        else:
            forgotPassMessage('error')
            return redirect('/accounts/login')
    else:
        print('Render')
        return render(request, 'accounts/forgotpass.html')

def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

def resetPasswordRender(request):
    return render(request, 'accounts/resetpassword.html')

def resetPassword(request):
    if request.method == 'POST':
        username = request.POST['username']
        usermail = request.POST['usermail']
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        fetchUserDb = User.objects.filter(username = username, email = usermail)

        if fetchUserDb:
            changePass = User.objects.get(username = username, email = usermail)

            if password1 == password2:
                changePass.set_password(password1)
                changePass.save()
                print('Changed')

                return redirect('/accounts/login')
