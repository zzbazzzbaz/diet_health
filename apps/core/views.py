from django.shortcuts import render


def home(request):
    """系统首页"""
    return render(request, 'home.html')
