import pandas as pd


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


#Those are just unesssary words that would flood the final results - conjunctions etc.
def get_list_of_unnecessary_words():
    df = pd.read_csv('/home/michal/Documents/Python/scraping/test/crawling/data/words.csv', delimiter=',')

    list_of_words = list(df.columns)

    return list_of_words

    