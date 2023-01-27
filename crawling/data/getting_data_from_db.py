from  getting_credentials import get
import psycopg2
import pandas as pd
from datetime import datetime
import numpy as np


data = get()

conn = psycopg2.connect(
   database=data[2], user=data[0], password=data[1], host='127.0.0.1', port= '5432'
)

conn.autocommit = True
cursor = conn.cursor()

cursor.execute("select * from main_tvn;")
result_tvn = cursor.fetchall()

conn.commit()

cursor.execute("select * from main_tvp;")
result_tvp = cursor.fetchall()

conn.commit()



df_tvn = pd.DataFrame(result_tvn)
df_tvn = df_tvn.drop(columns=[0,2,3,4])

df_tvp = pd.DataFrame(result_tvp)
df_tvp = df_tvp.drop(columns=[0,2,3,4])

df_tvn[1] = df_tvn[1].str.lower()
df_tvp[1] = df_tvp[1].str.lower()



def look_for_certain_keyword(df, keyword, extra=False):
    keyword = keyword.lower()
    new_df = df.applymap(lambda x: keyword in x.lower() if isinstance(x,str) else False)
    
    number_of_occrencies = len(new_df[new_df[1] == True])

    if extra == True:
    
        a = new_df.index[new_df[1]==True].tolist()

        pd.options.display.max_colwidth = 100
        for i in a:
            print(df.iloc[i])
   
    

    return number_of_occrencies



print(look_for_certain_keyword(df_tvp, "pol"))


#might need to improve it / automate
def advanced_search(df, keyword_base, test=False):
    look_for_certain_keyword(df, keyword_base, True)
    


def keywords_search(df):
    dict_of_words = {}
    for i in df[1]:
        print(i)

keywords_search(df_tvn)