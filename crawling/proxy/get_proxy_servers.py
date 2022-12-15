import requests 
import threading
from queue import Queue
import pandas as pd
import signal
import sys
import numpy as np


def interrupt_handler(signum, frame):
    
    print("\n")
    print(df)
    print("\n")
    
    np.savetxt(r"crawling/proxy/working_proxies.txt", df.values, fmt='%s')
    df.to_csv(r'crawling/proxy/working_proxies.csv', header=None, index=None, sep=' ', mode='w')
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
            res = requests.get("http://ipinfo.io/json", proxies={"http": p, "https": p}, timeout=3)
        except:
            continue
            
        if res.status_code == 200:
            time = str(res.elapsed)[-9:]

            ipaddress = (p.split(":")[0])
            
            print(f"ip: {p}  time: {time}")
            df2 = pd.DataFrame ({"ipaddress_with_port": [p],'time': [time], 'ipaddress': [ipaddress] })
            df = pd.concat([df,df2], ignore_index=True)
          
                
for _ in range(6):
    threading.Thread(target=t).start()

