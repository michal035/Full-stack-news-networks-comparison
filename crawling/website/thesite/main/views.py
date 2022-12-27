from django.shortcuts import render
from django.http import JsonResponse, response
from django.http import HttpResponse, HttpResponseRedirect

def index(response):
    #return  HttpResponse("<h1>Hello </h1>")

    print(response.method)
    if response.method == 'POST':
        
        lng = "Eng"

        if response.POST.get("btn1"):
            pass
        elif response.POST.get("btn2"):
            lng = "Pol"
        



    return render(response, "main/index.html", {"lng":lng})
