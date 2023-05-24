from getting_credentials import get
import psycopg2
import pandas as pd 


data = get()

conn = psycopg2.connect(
   database=data[2], user=data[0], password=data[1], host='127.0.0.1', port= '5432'
)


conn.autocommit = True
cursor = conn.cursor()


def tvn():
    global cursor


    df = pd.read_csv("/home/michal/Documents/Python/rest/csv/tvn.csv", sep=",")


    for i, value in df.iterrows():
        
        cursor.execute(f"INSERT INTO main_tvn(headline, date) VALUES ('{df.iloc[i][1]}','{df.iloc[i][2]}')")

    conn.commit()


def tvp():
    global cursor


    df = pd.read_csv("/home/michal/Documents/Python/rest/csv/tvp.csv", sep=",")

    

    for i, value in df.iterrows():
  
        cursor.execute(f"INSERT INTO main_tvp(headline, date, hour) VALUES ('{df.iloc[i][1]}','{df.iloc[i][2]}','{df.iloc[i][3]}')")

    conn.commit()




tvn()
tvp()
print("done")

conn.close()