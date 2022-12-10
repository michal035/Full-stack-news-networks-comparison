import requests 
import threading
from queue import Queue


list_of_working_proxies = []
q = Queue()


with open("/home/michal/Documents/Python/scraping/test/crawling/proxy/raw_list.txt","r") as f:
    p = f.read().split("\n")
    
    for i in p:
        q.put(i)


def t():
    global q
    while not q.empty():
        p = q.get()
        
        try:
            res = requests.get("http://ipinfo.io/json", proxies={"http": p, "https": p})
        except:
            continue
        if res.status_code == 200:
            print(p)


for _ in range(5):
    threading.Thread(target=t).start()


