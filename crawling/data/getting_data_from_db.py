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


def look_for_certain_keyword(df, keyword):
    keyword = keyword.lower()
    new_df = df.applymap(lambda x: keyword in x.lower() if isinstance(x,str) else False)
    print(len(df[1]==keyword))


    return new_df

print(look_for_certain_keyword(df_tvp, "tvn"))


