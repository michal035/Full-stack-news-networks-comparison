from django.shortcuts import render
from django.http import JsonResponse, response
from django.http import HttpResponse, HttpResponseRedirect
from .models import um


def index(response):

    lng = "Eng"
    print(response.method)
    if response.method == 'POST':
        

        if response.POST.get("btn1"):
            pass
        elif response.POST.get("btn2"):
            lng = "Pol"
        

    return render(response, "main/index.html", {"lng":lng})


def db_test(resposne):
    """obj = um.objects.all()
    print(obj)
    context = {'obj':obj}
    return render(resposne, "main/dbtest.html", {"c":context})"""
    p = um.objects.all()
    context = {'p': p,}
    return render(resposne, "main/dbtest.html", context)

