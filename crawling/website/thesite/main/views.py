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


def adding_stuff_to_merge(tvP,tvN):
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
        #here needs to be added that blank or so
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
    
    return objs


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



    objs = adding_stuff_to_merge(tvP,tvN)
    context = {'hl': objs,"lng":lng, }
    #context = {'tvp': tvP,'tvn': tvN ,"lng":lng, }

    return render(response, "main/index.html", context )
 

def archive(response, number_of_days=1):
    
    t = datetime.now()
    
    date = t.strftime("%Y-%m-%d")
    
    
    """day = t.day
    month = t.month
    year = t.year


    for i in range(int(number_of_days)):
        date = f"{year}-{month}-{day}"
        tvP = tvp.objects.raw(f"select * from main_tvp where date = '{date}'")
        tvN = tvn.objects.raw(f"select * from main_tvn where date = '{date}'")
        
        
        if day != 1 :
            day -= 1
        else:
            month -=1"""
    # 1 -> 2

    day = t.day
    month = t.month
    year = t.year

    eh = 1
    

    list_of_objs = []
    while  eh <= int(number_of_days):

        date = f"{year}-{month}-{28}" #
        
        #date2 = f"{year}-{month}-{1}"
        if month == 1:
            date2 = f"{year-1}-12-{1}"
        else:
            date2 = f"{year}-{month-1}-{1}" 
        
        print(f"date2 - {date2} date - {date}")
        tvP = tvp.objects.raw(f"select * from main_tvp where date between '{date2}' and '{date}'")
        tvN = tvn.objects.raw(f"select * from main_tvn where date between '{date2}' and '{date}'")


        if month == 1:
            year -= 1
            month = 11
        else:
            month -= 2

        objs = adding_stuff_to_merge(tvP,tvN)
        list_of_objs.append(objs)
        eh +=1
    
    return render(response, "main/archive.html",{'l': list_of_objs} )
    #return render(response, "main/archive.html",{'l':number_of_days} )
 





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

