from django.shortcuts import render

def homepage(request):
  return render(request, "homepage.html")


def login(request):
  return render(request, "login.html")