import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

def index(request):
    return render(request, 'index/index.html')

def security(request):
    return render(request, 'security.html')
