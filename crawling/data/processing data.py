import numpy as np
import pandas as pd

df = pd.read_csv("/home/michal/Documents/Python/scraping/test/crawling/data/headlines3.csv", sep=";")
print(df.axes)

df.sort_values(['link','hour/date',], inplace=True, ascending = [False, True])
df.to_csv("/home/michal/Documents/Python/scraping/test/crawling/data/headlines4.csv", sep=";", mode="w")