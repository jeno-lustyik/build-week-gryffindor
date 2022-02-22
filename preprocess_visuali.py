import csv
import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup
import html.parser
from time import sleep
import matplotlib.pyplot as plt

df_1 = pd.read_csv(r'C:\Users\omolara\Documents\strive school\strive-exercise\build-week-gryffindor\100books-1to50.csv', header = None)
df_2 = pd.read_csv(r'C:\Users\omolara\Documents\strive school\strive-exercise\build-week-gryffindor\100books_51-100.csv', header = None)
df_1.columns = [' titles','author','num_reviews','num_ratings','avg_rating', 'num_pages','original_publish_year', 'book_series', 'genre', 'awards', 'places']
df_2.columns = [' titles','author','num_reviews','num_ratings','avg_rating', 'num_pages','original_publish_year', 'book_series', 'genre', 'awards', 'places']
data = pd.concat([df_1, df_2], axis = 0)
data.to_csv('datagy.csv', index = False)

df = pd.DataFrame(data)
# #df.columns = [' titles','author','num_reviews','num_ratings','avg_rating', 'num_pages','original_publish_year', 'book_series', 'genre', 'awards', 'places']
# print(df)


df['awards'] = df['awards'].apply(len)
# print(df.head())
# # # #defining a function for the min-max normalization
def min_max_norm():
    minmax_norm = df.copy()
    column = 'avg_rating'
    minmax_norm[column] = 1 + (minmax_norm[column] - minmax_norm[column].min())/(minmax_norm[column].max() -  minmax_norm[column].min()) * 9
    a = df.assign(minmax_norm_ratings = minmax_norm[column])
    return a
df2 = min_max_norm()
print(df2)

#finding the mean of avg_ratings column 
average = df2.avg_rating.mean()
#print(average)
#defining a function for the mean normalization
def mean_norm():
    mean_normal = df2.copy()
    column = 'avg_rating'
    mean_normal[column] = 1 + ( mean_normal[column] - average)/(mean_normal[column].max() - mean_normal[column].min()) * 9
    b = df2.assign(mean_norm_ratings =  mean_normal[column])
    return b
df3 = mean_norm()

print(df3)

# #grouping books by original publish year
c = df2.copy()
d = c.groupby('original_publish_year')['minmax_norm_ratings'].mean()
df4 = pd.DataFrame(d)
df4.reset_index(inplace=True)
df4.rename(columns = {'original_publish_year': 'original_publish_year', 'minmax_norm_ratings': 'Ratings minmax mean'}, inplace = True)
print(df4)


# #create a function that  returns the maximum minmax rating 
def author_name(name: str):
    e = df3.loc[df['author'] == name]
    f = e.sort_values('minmax_norm_ratings', ascending= False)
    return f.iloc[0, 0]
print(author_name('Dean F. Wilson'))

#print(df.groupby('Director name')['Rating'])
#Visualizationn
#plotting a graph of the original publish year of books in group against the average of the minmax_norm rating using bar chat 

plt.bar(df4['original_publish_year'], df4['Ratings minmax mean'])
plt.legend()
plt.show()