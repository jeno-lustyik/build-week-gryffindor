
from ast import IsNot
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import time

# update the recent csv file

df = pd.read_csv("final.csv", sep = ',' ,names=['url','title','author','num_reviews','num_ratings','avg_stars','num_pages','publishing_year','series','genre','awards','places'])
#print(df)

## Each sepearate function created for each column, because we dont need to scrape all the columns. 
# so the user can use a function that designed to scrape particular values in the colum
# all calling_functions are comented, please uncomment required missing column function
# facing problems with missing_places()function 

# getting index of all not found titles values in the df
title_index = df.index[(df['title']=='Not found')].tolist()
print(len(title_index))
def missing_titles():
    for i in title_index:
        url = f"{df.iat[i,0]}"
        pg = requests.get(url)
        soup = BeautifulSoup(pg.content, 'html.parser')
        time.sleep(10)
        if soup.find('h1', class_='gr-h1 gr-h1--serif') is not None:
            df.at[i,'title'] = soup.find('h1', class_='gr-h1 gr-h1--serif').text.strip()
            df.to_csv('100books.csv', mode='w', index=False, header=False)
        else:
            df.at[i,'title'] = 'Not found'
            df.to_csv('100books.csv', mode='w', index=False, header=False)
#missing_titles()
print("title cleaning is succesful")

# # missed author names.

author_index = df.index[(df['author']=='Not found')].tolist()
print(len(author_index))
def missing_authors():
    for i in author_index:
        url = f"{df.iat[i,0]}"
        pg = requests.get(url)
        soup = BeautifulSoup(pg.content, 'html.parser')
        time.sleep(10)
        if soup.find('span', itemprop='name') is not None:
            time.sleep(15)
            df.at[i,'author'] = soup.find('span', itemprop='name').text.strip()
            df.to_csv('100books.csv', mode='w', index=False, header=False)
        else:
            df.at[i,'author'] = 'Not found'
            df.to_csv('100books.csv', mode='w', index=False, header=False)
#missing_authors()
    
print("author cleaning is sucessful")

# # missed num_revies.

reviews_index = df.index[(df['num_reviews']==0)].tolist()
print(len(reviews_index))

def missing_reviews():
    for i in reviews_index:
        url = f"{df.iat[i,0]}"
        pg = requests.get(url)
        soup = BeautifulSoup(pg.content, 'html.parser')
        time.sleep(10)
        if soup.find('meta', itemprop='reviewCount') is not None:
            time.sleep(15)
            df.at[i,'num_reviews'] = soup.find('meta', itemprop='reviewCount')['content']
            df.to_csv('100books.csv', mode='w', index=False, header=False)
        else:
            df.at[i,'num_reviews'] = 0
            df.to_csv('100books.csv', mode='w', index=False, header=False)
#missing_reviews()

print("reviews cleaning is sucessful")

# # missed num_ratings.

ratings_index = df.index[(df['num_ratings']==0)].tolist()
print(len(ratings_index))

def missing_ratings():
    for i in ratings_index:
        url = f"{df.iat[i,0]}"
        pg = requests.get(url)
        soup = BeautifulSoup(pg.content, 'html.parser')
        time.sleep(10)
        if soup.find('meta', itemprop='ratingCount') is not None:
            time.sleep(15)
            df.at[i,'num_ratings'] = soup.find('meta', itemprop='ratingCount')['content']
            df.to_csv('100books.csv', mode='w', index=False, header=False)
        else:
            df.at[i,'num_ratings'] = 0
            df.to_csv('100books.csv', mode='w', index=False, header=False)
#missing_ratings()       

print("ratings part is sucessful")

# missed avg_stars.

stars_index = df.index[(df['avg_stars']==0)].tolist()
print(stars_index)

def missing_stars():
    for i in stars_index:
        url = f"{df.iat[i,0]}"
        pg = requests.get(url)
        soup = BeautifulSoup(pg.content, 'html.parser')
        time.sleep(5)
        if soup.find('span', {'itemprop': 'ratingValue'}) is not None:
            time.sleep(5)
            df.at[i,'avg_stars'] = soup.find('span', {'itemprop': 'ratingValue'}).text.strip()
            df.to_csv('100books.csv', mode='w', index=False, header=False)
        else:
            df.at[i,'avg_stars'] = 0
            df.to_csv('100books.csv', mode='w', index=False, header=False)
        
#missing_stars()
print("stars rating part is sucessful")

# missed num_pages.

pages_index = df.index[(df['num_pages']==0)].tolist()
print(len(pages_index))
print(pages_index)
def missing_pages():
    for i in pages_index:
        url = f"{df.iat[i,0]}"
        print(url)
        pg = requests.get(url)
        soup = BeautifulSoup(pg.content, 'html.parser')
        b = soup.find('span', {'itemprop': 'numberOfPages'})
        print(b.text)
        time.sleep(15)
        if soup.find('span', {'itemprop': 'numberOfPages'}) is not None:
            time.sleep(15)
            a = soup.find('span', {'itemprop': 'numberOfPages'}).text.strip().split()[0]
            print(a)
            df.at[i,'num_pages'] = a
            df.to_csv('100books.csv', mode='w', index=False, header=False)
            print(f"succesful{i}")
        else:
            df.at[i,'num_pages'] = 0
            df.to_csv('100books.csv', mode='w', index=False, header=False)
            print(f"fail{i}")
#missing_pages()

print("pages part is sucessful")

#missed published_years.

year_index = df.index[(df['publishing_year']==0)].tolist()
print(len(year_index))
print(year_index)

def missing_years():
    for i in year_index[2:]:
        url = f"{df.iat[i,0]}"
        print(i)
        print(url)
        pg = requests.get(url)
        soup = BeautifulSoup(pg.content, 'html.parser')
        a = soup.find('div', id="details")
        time.sleep(2)
        if a is not None:
            time.sleep(2)
            b = soup.find_all('div',class_= 'row')
            if b is not None:
                if len(b)!=0 and len(b)>=1:
                    c=b[1].text.split()
                    for k in c:
                        if k.isdigit() and len(k)==4:
                            print(k)
                            df.at[i,'publishing_year'] = k
                            df.to_csv('years_cleaned.csv', mode='w', index=False, header=False)
                            print(f"sucess{i}")
                else:
                    df.at[i,'publishing_year'] = 0
                    df.to_csv('years_cleaned.csv', mode='w', index=False, header=False)
                    print(f"fail{i}")
                
            else:
                df.at[i,'publishing_year'] = 0
                df.to_csv('years_cleaned.csv', mode='w', index=False, header=False)
                print(f"fail{i}")            
        else:
            df.at[i,'publishing_year'] = 0
            df.to_csv('years_cleaned.csv', mode='w', index=False, header=False)
            print(f"fail{i}")
#missing_years()
print("years was sucessful")


###-missing series
series_index = df.index[(df['series']=='No series found')].tolist()
print(len(series_index))
print(series_index)

def missing_series():
    for i in series_index:
        url = f"{df.iat[i,0]}"
        pg = requests.get(url)
        soup = BeautifulSoup(pg.content, 'html.parser')
        time.sleep(15)
        if soup.find('h2', id="bookSeries") is not None:
            time.sleep(15)
            a = soup.find('h2', id="bookSeries").text.strip()
            df.at[i,'series'] = a[1:(len(a) - 1)]
            df.to_csv('100books.csv', mode='w', index=False, header=False)
            print(f"sucess{i}")
        else:
            df.at[i,'series'] = 'No series found'
            df.to_csv('100books.csv', mode='w', index=False, header=False)
            print(f"fail{i}")
#missing_series()
print("series was sucessful")



# ###- genre
genre_index = df.index[(df['genre']=='Not found')].tolist()
print(len(genre_index))

def missing_genre():
    for i in genre_index:
        url = f"{df.iat[i,0]}"
        pg = requests.get(url)
        soup = BeautifulSoup(pg.content, 'html.parser')
        time.sleep(15)
        if soup.find_all('a', class_='actionLinkLite bookPageGenreLink') is not None:
            genre = soup.find_all('a', class_='actionLinkLite bookPageGenreLink')
            genres_dump = []
            for i in genre:
                if len(genres_dump) <= 1 and f'{i.text}, ' not in genres_dump:
                    genres_dump.append(f'{i.text}, ')
                elif len(genres_dump) == 2 and f'{i.text}, ' not in genres_dump:
                    genres_dump.append(i.text)
                    df.at[i,'genre'] = ''.join(genres_dump)
                    df.to_csv('100books.csv', mode='w', index=False, header=False)
                    break
                else:
                    continue
            else:
                df.at[i,'genre'] = 'Not found'
                df.to_csv('100books.csv', mode='w', index=False, header=False)
#missing_genre()
print("genre was sucessful")

# # missed awards.

awards_index = df.index[(df['awards']=='Not found')].tolist()
print(len(awards_index))
def missing_awards():
    for i in awards_index:
        url = f"{df.iat[i,0]}"
        print(url)
        pg = requests.get(url)
        soup = BeautifulSoup(pg.content, 'html.parser')
        time.sleep(2)
        if soup.find('div', itemprop='awards') is not None:
            time.sleep(2)
            award = soup.find('div', itemprop='awards')
            awards_list = award.text.replace('\n', '').replace('...more', ', ').replace('...less', '')
            df.at[i,'awards'] = awards_list
            df.to_csv('100books.csv', mode='w', index=False, header=False)
            print(f"sucess{i}")
        else:
            df.at[i,'awards'] = 'Not found'
            df.to_csv('100books.csv', mode='w', index=False, header=False)
            print(f"fail{i}")
#missing_awards()
print("awards completed")

# places missing
place_index = df.index[(df['places']=='Not found')].tolist()
print(len(place_index))
print(place_index)

def missing_places():
    for i in place_index:
        url = f"{df.iat[i,0]}"
        print(url)
        pg = requests.get(url)
        soup = BeautifulSoup(pg.content, 'html.parser')
        time.sleep(2)
        if soup.find('div', id='details') is not None:
            box = soup.find('div', id='details')
            box_div = box.find_all('div')
            setting = []
            for k in box_div:
                if k.text == 'Setting':
                    set_box = box_div[box_div.index(k) + 1].find_all('a')
                    for j in set_box:
                        setting.append(j.text)
                setting = ','.join(setting)
                df.at[i,'places'] = setting
                df.to_csv('100books.csv', mode='w', index=False, header=False)
                print(f"sucess{i}")
        else:
            df.at[i,'places'] = 'Not found'
            df.to_csv('100books.csv', mode='w', index=False, header=False)
            print(f"fail{i}")
#missing_places()
print("places was done")








       