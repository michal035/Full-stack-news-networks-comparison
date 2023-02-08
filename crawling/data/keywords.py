from getting_credentials import get
import psycopg2
import pandas as pd
from datetime import datetime
import numpy as np
import re
import unicodedata
from unidecode import unidecode


from extra_functions_for_keywords_file import clean_punctuation, get_list_of_unnecessary_words


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




# basically I  want to count words like 'car' and 'cars' as the same keyword 
# This is the one that will actually get used 

def keywords_search_v2(df):

    pd.options.display.max_colwidth = 100
    df_silimary_words = pd.DataFrame(columns= ["word", "number", "original_words"])

    unnecessary_words = get_list_of_unnecessary_words()
    exceptions = pd.read_csv("crawling/data/exceptions_keywords.csv")

    list_of_political_parites = ["pis","psl","205"]


    for i in df[1]:
        i = clean_punctuation(i)

        
        for word in i:
            if word in unnecessary_words:
                pass
            else:
                #exceptions just for the political parites - just the one with shortcuts ig
                if (len(word) == 4 or len(word) == 3)and word[:3] in list_of_political_parites:
                    
                    first_letters = word[:3]
                    if first_letters in  list(df_silimary_words['word']):
                        index = list(df_silimary_words.index[df_silimary_words["word"] == first_letters])[0]
                        df_silimary_words.at[index,"number"] = int(df_silimary_words.iloc[index].number) + 1
                        df_silimary_words.at[index,"original_words"] = f"{str(df_silimary_words.iloc[index].original_words)}, {word}"
                    else:
                        df_silimary_words = pd.concat([df_silimary_words, pd.DataFrame.from_records([{ 'word': first_letters, 'number': 1 , "original_words" : word}])], ignore_index=True)
                
                elif len(word) >= 4:
                    first_letters = word[:4]
                    
                    
                    #filter for known exceptions like "policja" and "polityka"
                    if first_letters in list(exceptions["old"]):
                        index = list(exceptions.index[exceptions["old"]==first_letters])[0]
                        if exceptions.at[index,"extra"] == "Y":
                            first_letters = word[:5]
                        else:
                            first_letters = exceptions.at[index,"new"]
                    

                    if first_letters in  list(df_silimary_words['word']):
                        index = list(df_silimary_words.index[df_silimary_words["word"] == first_letters])[0]
                        df_silimary_words.at[index,"number"] = int(df_silimary_words.iloc[index].number) + 1
                        df_silimary_words.at[index,"original_words"] = f"{str(df_silimary_words.iloc[index].original_words)}, {word}"
                    else:
                        df_silimary_words = pd.concat([df_silimary_words, pd.DataFrame.from_records([{ 'word': first_letters, 'number': 1 , "original_words" : word}])], ignore_index=True)
                        
                else:
                    first_letters = word
                    if first_letters in  list(df_silimary_words['word']):
                        index = list(df_silimary_words.index[df_silimary_words["word"] == first_letters])[0]
                        df_silimary_words.at[index,"number"] = int(df_silimary_words.iloc[index].number) + 1
                        df_silimary_words.at[index,"original_words"] = f"{str(df_silimary_words.iloc[index].original_words)}, {word}"
                    else:
                        df_silimary_words = pd.concat([df_silimary_words, pd.DataFrame.from_records([{ 'word': first_letters, 'number': 1 , "original_words" : word}])], ignore_index=True)
            
    return df_silimary_words


print(keywords_search_v2(df_tvp).sort_values(by=['number'],ascending=False).head(50))



#I guess you could call this 'debug' tool - for my own testing purposes
def look_for_certain_keyword(df, keyword, extra=False):
    
    keyword = keyword.lower() 
    df[1] = df[1].str.lower()
    df[1] = df[1].str.replace(",","")
    df[1] = df[1].str.replace(".","")
    df[1] = df[1].str.replace("'","")
    df[1] = df[1].str.replace('"',"")


    new_df = df.applymap(lambda x: keyword in x.lower() if isinstance(x,str) else False)
    
    number_of_occrencies = len(new_df[new_df[1] == True])

    if extra == True:
    
        a = new_df.index[new_df[1]==True].tolist()

        pd.options.display.max_colwidth = 100
        for i in a:
            print(df.iloc[i])
   
    

    return number_of_occrencies


#print(look_for_certain_keyword(df_tvn, "tvp", True))


#This is just so i could get full df from separate file
def get_full_data_frames():
    return df_tvn, df_tvp



if __name__ != "__main__":
    
    df_tvn = keywords_search_v2(df_tvn).sort_values(by=['number'],ascending=False).head(100)
    df_tvp = keywords_search_v2(df_tvp).sort_values(by=['number'],ascending=False).head(100)

    df_tvn.to_csv("/home/michal/Documents/Python/scraping/test/crawling/data/tvn_key_words.csv")
    df_tvp.to_csv("/home/michal/Documents/Python/scraping/test/crawling/data/tvp_key_words.csv")


