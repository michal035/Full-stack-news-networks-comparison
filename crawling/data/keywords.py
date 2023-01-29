from  getting_credentials import get
import psycopg2
import pandas as pd
from datetime import datetime
import numpy as np
import re
import unicodedata
from unidecode import unidecode


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



#print(look_for_certain_keyword(df_tvp, "ukrain"))


#might need to put this into seprate file yeah
def clean_punctuation(i):
    
    i = i.replace("\xa0"," ")
    

    i = i.replace("'","")
    i = i.replace('"',"")
    i = i.replace(".","")
    i = i.replace(",", "")
    i = i.replace("!", "")
    i = i.replace("?", "")

    i = i .split(" ")

    return i 


# basically I  want to count words like 'car' and 'cars' as the same keyword
def keywords_search_v2(df):
    pd.options.display.max_colwidth = 100
    df_silimary_words = pd.DataFrame(columns= ["word", "number", "original_word"])
    unnecessary = ["[VIDEO]"]
    list_of_political_parites = ["pis","psl","205"]


    for i in df[1]:
        i = clean_punctuation(i)

        
        for word in i:
            if word in unnecessary:
                pass
            else:
                #exceptions just for the political parites - just the one with shortcuts ig
                if (len(word) == 4 or len(word) == 3)and word[:3] in list_of_political_parites:
                    
                    first_letters = word[:3]
                    if first_letters in  list(df_silimary_words['word']):
                        index = list(df_silimary_words.index[df_silimary_words["word"] == first_letters])[0]
                        df_silimary_words.at[index,"number"] = int(df_silimary_words.iloc[index].number) + 1
                        df_silimary_words.at[index,"original_word"] = f"{str(df_silimary_words.iloc[index].original_word)}, {word}"
                    else:
                        df_silimary_words = pd.concat([df_silimary_words, pd.DataFrame.from_records([{ 'word': first_letters, 'number': 1 , "original_word" : word}])], ignore_index=True)
                
                elif len(word) >= 4:
                    first_letters = word[:4]
                    if first_letters in  list(df_silimary_words['word']):
                        index = list(df_silimary_words.index[df_silimary_words["word"] == first_letters])[0]
                        df_silimary_words.at[index,"number"] = int(df_silimary_words.iloc[index].number) + 1
                        df_silimary_words.at[index,"original_word"] = f"{str(df_silimary_words.iloc[index].original_word)}, {word}"
                    else:
                        df_silimary_words = pd.concat([df_silimary_words, pd.DataFrame.from_records([{ 'word': first_letters, 'number': 1 , "original_word" : word}])], ignore_index=True)
                        
                else:
                    #here just needs to be added 
                    pass

            
    return df_silimary_words

print(keywords_search_v2(df_tvn).sort_values(by=['number'],ascending=False).head(50))



def keywords_search(dff):

    df = pd.DataFrame(columns= ["word", "number"])
    df_silimary_words = pd.DataFrame(columns= ["word", "number", "original_indexes"])

    list_of_not_words = ["się","i","są","to","jest","jak","nie","był","w", "na", "z", "się", " ", "do", "o", "po", "przez", "za", "sprawie", "od"
    ,"co", "dla", "tak", "jej", "ma","będzie", "już", "że", "lat", "[wideo]", "ws", "ani", "pod", "go", 'ze']



    for i in dff[1]:

        #i = unicodedata.normalize("NFKD", i)
        #i = unidecode(i)
        #i = i .split(" ")

        i = clean_punctuation(i)

        for word in i:
        
            if word in list_of_not_words:
                pass
            
            else:

                if word in list(df['word']):

                    index = list(df.index[df["word"] == word])[0]
                    df.at[index, "number"] = int(df.iloc[index].number) + 1

                else:
                    df = pd.concat([df, pd.DataFrame.from_records([{ 'word': word, 'number': 1 }])], ignore_index=True)
    
    return df


#top = (keywords_search(df_tvn).sort_values(by=['number'],ascending=False)).head(50)



