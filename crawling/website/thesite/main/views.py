from django.shortcuts import render
from django.http import JsonResponse, response
from django.http import HttpResponse, HttpResponseRedirect
from .models import tvn, tvp, um
from datetime import datetime
from calendar import monthrange
from django.shortcuts import redirect
from .serializers import TvnSerializer
import json

class merge():

    def __init__(self, a="", b="", c="") -> None:
        self.tvn = a
        self.tvp = b
        self.c = c
    def add_other(self, key, value):
        if key == "tvn":
            self.tvn = value

        else:
            self.tvp = value

    def __repr__(self) -> str:
        return f"tvn = {self.tvn} tvp={self.tvp}"




def adding_stuff_to_merge(tvP, tvN, month=""):
    objs = []

    # whole merge thing needs to be rewritten
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

    if month != "":
        objs.append(merge(a='info_podsumowanie', b=month))
        objs.append(merge('Keyword1 = 0', 'keyword2 = 0', "c"))

    for i in range(d):
        if the_thing == 1:
            obj = merge(a=tvN[i].headline)
            objs.append(obj)
        else:
            obj = merge(b=tvP[i].headline)
            objs.append(obj)

    if month != "":
        for i in range(dd):
            if the_thing == 1:
                objs[i+2].add_other("tvp", tvP[i].headline)
            else:
                objs[i+2].add_other("tvn", tvN[i].headline)

    if month == "":
        for i in range(dd):
            if the_thing == 1:
                objs[i].add_other("tvp", tvP[i].headline)
            else:
                objs[i].add_other("tvn", tvN[i].headline)

    # here

    return objs


def number_of_days_in_month(year=2023, month=2):
    return monthrange(year, month)[1]


def index(response):

    lng = "Eng"

    print(response.method)
    if response.method == 'POST':

        if response.POST.get("btn1"):
            pass
        elif response.POST.get("btn2"):
            lng = "Pol"

    # tvP = tvp.objects.all()
    # tvN = tvn.objects.all()

    t = datetime.now()
    date = t.strftime("%Y-%m-%d")

    tvP = tvp.objects.raw(f"select * from main_tvp where date = '{date}'")
    tvN = tvn.objects.raw(f"select * from main_tvn where date = '{date}'")

    objs = adding_stuff_to_merge(tvP, tvN)
    context = {'hl': objs, "lng": lng, }
    # context = {'tvp': tvP,'tvn': tvN ,"lng":lng, }

    return render(response, "main/index.html", context)


def archive(response, number_of_months=1):

    t = datetime.now()

    date = t.strftime("%Y-%m-%d")


    if response.method == "POST":
        if response.POST.get("btn3"):
            number_of_months = int(number_of_months) + 1
            return redirect(f"/archive/{number_of_months}/")

    
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

    day = t.day
    month = t.month
    year = t.year

    eh = 1

    contex_information = []
    list_of_objs = []

    while eh <= int(number_of_months):

        date = f"{year}-{month}-{int(number_of_days_in_month(year, int(month)))}"
        date2 = f"{year}-{month}-{1}"

        """if month == 1:
            date2 = f"{year-1}-12-{1}"
        else:
            date2 = f"{year}-{month-1}-{1}" """

        tvP = tvp.objects.raw(
            f"select * from main_tvp where date between '{date2}' and '{date}'")
        tvN = tvn.objects.raw(
            f"select * from main_tvn where date between '{date2}' and '{date}'")

        # call function that count amount of keywords

        objs = adding_stuff_to_merge(tvP, tvN, f"{month}/{year}")
        list_of_objs.append(objs)

        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1

        eh += 1

    return render(response, "main/archive.html", {'l': list_of_objs})


def statistics(response):
    return render(response, "main/statistics.html")


def db_test(response):
    """obj = um.objects.all()
    print(obj)
    context = {'obj':obj}
    return render(response, "main/dbtest.html", {"c":context})"""

    t = datetime.now()
    date = t.strftime("%Y-%m-%d")
    u = f"{t.year}-{t.month}-{t.day}"

    p = tvp.objects.raw(f"select * from main_tvp where date = '{u}'")
    context = {'p': p, }
    return render(response, "main/dbtest.html", context)



def api(response, keyword=None ):
    
    
    if keyword.isdigit() == True:
        t = datetime.now()
        date = t.strftime("%Y-%m-%d")
        u = f"{t.year}-{t.month}-{t.day}"

        eh = 1
        day = t.day
        month = t.month
        year = t.year

        list_of_objs = [[],[]]

        while eh <= int(keyword):

            date = f"{year}-{month}-{int(number_of_days_in_month(year, int(month)))}"
            date2 = f"{year}-{month}-{1}"


            tvP = tvp.objects.raw(
                f"select * from main_tvp where date between '{date2}' and '{date}';")
            tvN = tvn.objects.raw(
                f"select * from main_tvn where date between '{date2}' and '{date}';")

           
            p = len(tvP)
            n = len(tvN)

        
            for i in range(p):
                print(tvP[i].headline)
                list_of_objs[0].append(tvP[i].headline)
            for i in range(n):
                list_of_objs[1].append(tvN[i].headline)


            if month == 1:
                year -= 1
                month = 12
            else:
                month -= 1

            eh += 1


        return HttpResponse(json.dumps(list_of_objs, ensure_ascii=False))
        
        #return JsonResponse(list_of_objs, safe=False)
    
    elif  keyword == "keywords":
        pass
    else:
        pass


def index2(response):

    return render(response, "main/index2.html")
