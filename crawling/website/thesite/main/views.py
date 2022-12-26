from django.shortcuts import render
from django.http import JsonResponse, response
from django.http import HttpResponse, HttpResponseRedirect


def index(response):
    #return  HttpResponse("<h1>Hello </h1>")
    return render(response, "main/index.html", {})
