from  getting_credentials import get
import psycopg2
import pandas as pd
from datetime import datetime


data = get()

conn = psycopg2.connect(
   database=data[2], user=data[0], password=data[1], host='127.0.0.1', port= '5432'
)

conn.autocommit = True


cursor = conn.cursor()

def tvn():
    global cursor

    t = datetime.now()
    u = f"{t.year}-{t.month}-{t.day}"

    df = pd.read_csv("/home/michal/Documents/Python/scraping/test/crawling/data/headlines1.csv", sep=";")
    for i in df["article-headline"]:   
        
        i = i.replace("'","")
        cursor.execute(f"select * from main_tvn where headline = '{i}' and date = '{u}'")
        result = cursor.fetchone()
        
        if result is None:
            cursor.execute(f"INSERT INTO main_tvn(headline, date) VALUES ('{i}','{u}')")

    conn.commit()


def tvp():
    global cursor

    t = datetime.now()
    u = f"{t.year}-{t.month}-{t.day}"

    df = pd.read_csv("/home/michal/Documents/Python/scraping/test/crawling/data/headlines6.csv", sep=";")

    for i in range(len(df)):
        
        i = i.replace("'","")
        cursor.execute(f"select * from main_tvp where headline = '{df.iloc[i][1]}' and date = '{u}'")
        result = cursor.fetchone()
        
        if result is None:
            cursor.execute(f"INSERT INTO main_tvp(headline, date, hour) VALUES ('{df.iloc[i][1]}','{u}','{df.iloc[i][2]}')")

    conn.commit()


def test_query():
    global cursor

    cursor.execute(f"select * from main_tvn where headline = 'Pożar Aautokaru wiozącego turystów z Węgier' and date = '2023-01-02';")
    
    result = cursor.fetchone()
    print(result)
    print(type(result))
    if result is None:
        print('yh')
    



tvn()
tvp()
print("done")

conn.close()