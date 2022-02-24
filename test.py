import pandas as pd
import re

df = pd.read_csv("final.csv", sep = ',' ,names=['url','title','author','num_reviews','num_ratings','avg_stars','num_pages','publishing_year','series','genre','awards','places'])
#print(df)
a = df[df['title'].str.contains("1984", flags=re.IGNORECASE)]
print(a)






