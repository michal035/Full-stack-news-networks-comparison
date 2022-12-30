import numpy as np
import pandas as pd



def tvn():
    
    df = pd.read_csv("/home/michal/Documents/Python/scraping/test/crawling/data/headlines3.csv", sep=";")
    df.sort_values(['link','hour/date',], inplace=True, ascending = [False, True])
    
    df.to_csv("/home/michal/Documents/Python/scraping/test/crawling/data/headlines4.csv", sep=";", mode="w")


    df2 = pd.read_csv("/home/michal/Documents/Python/scraping/test/crawling/data/headlines2.csv", sep=";")
    #print(df2.loc[df2["article-headline"].str.contains("TVN24 GO")])
    

    c = len(df2)

    df4 = pd.DataFrame = (df2.loc[df2["article-headline"].str.contains("TVN24 GO")])
    t = list(df4.index)

    df4 = df2.iloc[:t[0]]


    df4.to_csv("/home/michal/Documents/Python/scraping/test/crawling/data/headlines1.csv", sep=";", mode="w")
            





def tvp():
    
    df = pd.read_csv("/home/michal/Documents/Python/scraping/test/crawling/data/headlines5.csv", sep=";")
    
    """df2 = pd.DataFrame({

        'article-headline' : [],
        'hour/date' : []
        })"""
    df2 = pd.DataFrame()

    for i in range(len(df)):
        
        # no idea why there is == like it should be != as far as i am concern, its late in the night tho don't judge me - quite sure it was working just fine before with !=
        if str(df.iloc[i,1]).find(".") == -1:
            
            temp_def = pd.DataFrame({'article-headline' : [df.iloc[i,0]],'hour/date' : [df.iloc[i,1]]})
            df2 = pd.concat([temp_def,df2], ignore_index=True)
            df2.sort_values(['hour/date'], inplace=True)
    
    
    df2 = df2.reset_index(drop=True)
    df2.set_index(['article-headline', 'hour/date'])
    df2.to_csv("/home/michal/Documents/Python/scraping/test/crawling/data/headlines6.csv", sep=";", mode="w")
    

