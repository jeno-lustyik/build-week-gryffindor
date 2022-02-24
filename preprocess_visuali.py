from cmath import nan
import csv
import pandas as pd 
import numpy as np
from bs4 import BeautifulSoup
import html.parser
from time import sleep
import matplotlib.pyplot as plt

#def preprocessing():

df = pd.read_csv(r'C:\Users\omolara\Documents\strive school\build-week-gryffindor\final.csv', header = None)
df.columns = ['url', 'titles','author','num_reviews','num_ratings','avg_rating', 'num_pages','original_publish_year', 'book_series', 'genre', 'awards', 'places']
#print(df)


#df1.loc[df1["awards"] == "Not found", "awards"] = np.nan
# df['awards'] = df['awards'].str.strip(',')
# df['awards'] = df['awards'].str.split(',')  
# df['awards'] = df["awards"].apply(len)

def len_award():
    awards = df['awards'].tolist()
    a = []
    for i in awards:
        if i!='Not found':
            i = str(i)
            i = i.split(',')
            a.append(len(i))

        else:
            a.append(0)
 
    b=df.assign(awards_len = a)
    return b

df1 = len_award()
print(df1.head())
print(df1['awards_len'])


def avg_rating_clean_up():
    avg_ratin = df['avg_rating'].tolist()
    c = []
    for i in avg_ratin:
        if i!='Not found':
            c.append(i)

        else:
            c.append(0)
 
    d = df1.assign(average_rating_flo = c)
    d['average_rating_flo'] = d['average_rating_flo'].astype(float)
    return d

df2 = avg_rating_clean_up()
print(df2)


# # # # #defining a function for the min-max normalization
def min_max_norm():
    minmax_norm = df2.copy()
    minmax_norm
    column = 'average_rating_flo'
    minmax_norm[column] = 1 + (minmax_norm[column] - minmax_norm[column].min())/(minmax_norm[column].max() -  minmax_norm[column].min()) * 9
    e = df2.assign(minmax_norm_ratings = minmax_norm[column])
    return e
df3 = min_max_norm()
print(df3)

# # #finding the mean of avg_ratings column 
average = df3.average_rating_flo.mean()
#print(average)
#defining a function for the mean normalization
def mean_norm():
    mean_normal = df2.copy()
    column = 'average_rating_flo'
    mean_normal[column] = 1 + ( mean_normal[column] - average)/(mean_normal[column].max() - mean_normal[column].min()) * 9
    f = df3.assign(mean_norm_ratings =  mean_normal[column])
    return f
df4= mean_norm()

print(df4)

#group thr group by original published year and get the mean of the min_max_norm_rating

g = df4.groupby('original_publish_year')['minmax_norm_ratings'].mean()
df5 = pd.DataFrame(g)
df5.reset_index(inplace=True)
df5.rename(columns = {'original_publish_year': 'original_publish_year2', 'minmax_norm_ratings': 'Ratings minmax mean'}, inplace = True)
print(df5)


#no of ratings and actual rating
h = df4[['num_ratings', 'num_reviews']]

df6 = h.sort_values('num_reviews', ascending= False)
#print[df6]

#no of award and ratings 

i = df4[['average_rating_flo', 'awards_len']]

df7 = i.sort_values('average_rating_flo', ascending= False)

print(df7)




# # #create a function that  returns the maximum minmax rating 
def author_name(name: str):
    j = df3.loc[df['author'] == name]
    k = j.sort_values('minmax_norm_ratings', ascending= False)
    return k.iloc[0, 0]
print(author_name('Dean F. Wilson'))

# #print(df.groupby('Director name')['Rating'])
# #Visualizationn
# #plotting a graph of the original publish year of books in group against the average of the minmax_norm rating using bar chat 
# plot the number of awards and avg.ratings against title of books and compare if the award given goes in line with the avg.rating 
#plot a scattered graph of ratings to the number of pages, to check if the number of rating is determined by the number of pages 
# use a straight line graph to see if the number of raing and number of review follow a certain pattern
# plt.bar(df5['original_publish_year2'],df5['Ratings minmax mean'])
# plt.legend()
# plt.show()