from django.shortcuts import render
from django.http import JsonResponse, response
from django.http import HttpResponse, HttpResponseRedirect
from .models import tvn,tvp, um
from datetime import datetime


class merge():

    def __init__(self,a="",b="") -> None:
        self.tvn = a
        self.tvp = b

    
    def add_other(self,key,value):
        if key == "tvn":
            self.tvn = value
            
        else:
            self.tvp = value



    def __repr__(self) -> str:
        return f"tvn = {self.tvn} tvp={self.tvp}"


def index(response):


    lng = "Eng"
   
    print(response.method)
    if response.method == 'POST':
        

        if response.POST.get("btn1"):
            pass
        elif response.POST.get("btn2"):
            lng = "Pol"


    #tvP = tvp.objects.all()
    #tvN = tvn.objects.all()

    t = datetime.now()
    date = t.strftime("%Y-%m-%d")

    tvP = tvp.objects.raw(f"select * from main_tvp where date = '{date}'")
    tvN = tvn.objects.raw(f"select * from main_tvn where date = '{date}'")




    objs = []


    #whole merge thing needs to be rewritten
    d = 0
    dd = 0
    the_thing = 0


    if len(tvP) > len(tvN):
        d = len(tvP)
        dd = len(tvN)
    else:
        d = len(tvN)
        dd = len(tvP)
        the_thing = 1

    for i in range(d):
        if the_thing == 1:
            obj = merge(a=tvN[i].headline)
            objs.append(obj)
        else:
            obj = merge(b=tvP[i].headline)
            objs.append(obj)


    for i in range(dd):
        if the_thing == 1: 
            objs[i].add_other("tvp",tvP[i].headline)
        else:
            objs[i].add_other("tvn",tvN[i].headline)
    


    context = {'hl': objs,"lng":lng, }
    #context = {'tvp': tvP,'tvn': tvN ,"lng":lng, }

    return render(response, "main/index.html", context )
 


def db_test(resposne):
    """obj = um.objects.all()
    print(obj)
    context = {'obj':obj}
    return render(resposne, "main/dbtest.html", {"c":context})"""

    
    t = datetime.now()
    date = t.strftime("%Y-%m-%d")
    u = f"{t.year}-{t.month}-{t.day}"


    p = tvp.objects.raw(f"select * from main_tvp where date = '{u}'")
    context = {'p': p,}
    return render(resposne, "main/dbtest.html", context)

