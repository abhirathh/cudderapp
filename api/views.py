import hashlib
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
import datetime
import json
from accounts.models import userApiConfig
from django.views.decorators.csrf import csrf_exempt
import secrets

def dashboard(request):
    user_api_data = list(userApiConfig.objects.values().filter(username = request.user.username))
    return render(request, 'dashboard.html', {'user_api_data': user_api_data})

@csrf_exempt
def newApiKey(request):
    if request.method == 'POST':
        name = request.POST['appname']
        print(name)
        loop_breaker = True

        while loop_breaker:

            api_key = secrets.token_hex(10)

            if not userApiConfig.objects.filter(api_key = str(api_key)):
                loop_breaker = False

                ct = datetime.datetime.now()

                timestamp = str(ct)

                userApiConfig.objects.create(username = request.user.username, name = str(name), api_key = str(api_key), timestamp = str(timestamp))

                return redirect('/api/dashboard')
