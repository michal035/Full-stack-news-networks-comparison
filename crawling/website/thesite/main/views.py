from django.shortcuts import render
from django.http import JsonResponse, response
from django.http import HttpResponse, HttpResponseRedirect
from .models import tvn, tvp, um
from datetime import datetime
from calendar import monthrange
from django.shortcuts import redirect
from .serializers import TvnSerializer
import psycopg2
import json
from configparser import ConfigParser



config = ConfigParser()
config.read("/home/michal/Documents/Python/scraping/test/crawling/other/config.ini")
config["database"]["password"]


conn = psycopg2.connect(
   database=config["database"]["database_n"], user=config["database"]["user"], password=config["database"]["password"], host='127.0.0.1', port= '5432'
)

conn.autocommit = True
cursor = conn.cursor()



def number_of_days_in_month(year=2023, month=2):
    return monthrange(year, month)[1]


def archive(response, keyword=None):
    
    if response.method == "POST":
        if response.POST.get("thebtN"):
            keyword = int(keyword) + 1
            return redirect(f"/archive/{keyword}/")



    return render(response, "main/archive.html")



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
    
    

    elif  keyword == "key_words":

        data = []
        cursor.execute(f"select * from keywords;")
        conn.commit()
        result = cursor.fetchall()


        #need to add examples of those keywords
        for i in result:
            data.append({
            "headline" : i[0],
            "first_cell" : f"TVN: {i[1]}",
            "second_cell" : f"TVP: {i[2]}",
            },)
        
        return HttpResponse(json.dumps(data, ensure_ascii=False))
    else:
        pass


def index2(response):

    return render(response, "main/index2.html")


def key_words(response):
    return render(response, "main/key_words.html")



