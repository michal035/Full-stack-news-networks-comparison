import requests 
import threading
from queue import Queue
import pandas as pd
import signal
import sys


def interrupt_handler(signum, frame):
    print("\n")
    print(df)
    print("\n")
    sys.exit()


signal.signal(signal.SIGINT, interrupt_handler)



list_of_working_proxies = []
q = Queue()


with open("/home/michal/Documents/Python/scraping/test/crawling/proxy/raw_list.txt","r") as f:
    p = f.read().split("\n")
    
    for i in p:
        q.put(i)


df = pd.DataFrame({
    'ipaddress_with_port' : [],
    'time' : [],
    'ipaddress' : []


})


def t():
    global q
    global df

    while not q.empty():
        p = q.get()
        
        try:
            res = requests.get("http://ipinfo.io/json", proxies={"http": p, "https": p})
        except:
            continue
        if res.status_code == 200:
            print(p)
            time = res.elapsed
            print(time)
            df2 = pd.DataFrame ({"ipaddress_with_port": [p],'time': [time], 'ipaddress': [(p.split(":")[0])] })
            df = pd.concat([df,df2], ignore_index=True)


for _ in range(5):
    threading.Thread(target=t).start()

