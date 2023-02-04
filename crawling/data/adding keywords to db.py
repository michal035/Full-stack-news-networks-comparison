from  getting_credentials import get
import psycopg2
import pandas as pd 
import keywords
from keywords import get_full_data_frames


df_tvn = pd.read_csv("crawling/data/tvn_key_words.csv")
df_tvp = pd.read_csv("crawling/data/tvp_key_words.csv")


df = pd.read_csv('crawling/data/chosen_key_words.csv', delimiter=',')
list_of_words = list(df.columns)


full_df_of_key_words = get_full_data_frames()


#getting pure keyword
def getting_pure_word(df):

   the_words_o = ((df["original_word"][df["word"] == i].to_string(index=False)).replace(" ","")).split(",")  
   the_words_o.pop()

   the_words = [y for y in the_words_o if y[-1] == "a"]
   
   if len(the_words) == 0:
      lengths = [len(x) for x in the_words_o]
      the_word = the_words_o[lengths.index(min(lengths))]
   else:
      lengths = [len(x) for x in the_words]
      the_word = the_words[lengths.index(min(lengths))]

   return the_word

      

for i in list_of_words:
   if i in df_tvp["word"].values and i in df_tvn["word"].values:
      
      tvn = list(df_tvn["number"][df_tvn["word"] == i])[0]
      tvp = list(df_tvp["number"][df_tvp["word"] == i])[0]
      
      the_word = getting_pure_word(df_tvp)



      print(f"{the_word}  TVN: {tvn}   TVP: {tvp}")

   else:
      if i in df_tvn["word"].values:

         df = full_df_of_key_words[1]

         try:
            tvp = list(df["number"][df["word"]==i])[0]
         except:
            tvp = "<2"
         

         the_word = getting_pure_word(df_tvn)

         tvn = list(df_tvn["number"][df_tvn["word"] == i])[0]


         print(f"{the_word}  TVN: {tvn}   TVP: {tvp}")

            
      elif i in df_tvp["word"].values:

         df = full_df_of_key_words[0]

         try:
            tvn = list(df["number"][df["word"]==i])[0]
         except:
            tvn = "<2"
         

         the_word = getting_pure_word(df_tvp)

         tvp = list(df_tvp["number"][df_tvp["word"] == i])[0]


         print(f"{the_word}  TVN: {tvn}   TVP: {tvp}")
      

      else:
         #such occurence would need to be logged ig
         print(i)
      










"""data = get()

conn = psycopg2.connect(
   database=data[2], user=data[0], password=data[1], host='127.0.0.1', port= '5432'
)

conn.autocommit = True


cursor = conn.cursor()"""




