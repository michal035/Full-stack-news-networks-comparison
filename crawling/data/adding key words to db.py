from  getting_credentials import get
import psycopg2
import pandas as pd 
import keywords



df_tvn = pd.read_csv("crawling/data/tvn_key_words.csv")
df_tvp = pd.read_csv("crawling/data/tvp_key_words.csv")

print(df_tvn[df_tvn["word"]=="polsce"].number)



"""data = get()

conn = psycopg2.connect(
   database=data[2], user=data[0], password=data[1], host='127.0.0.1', port= '5432'
)

conn.autocommit = True


cursor = conn.cursor()"""




