from ast import IsNot
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import time
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import html.parser
from cmath import nan
import csv

filepath = Path('100books.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)

# empty lists for each scraping element that we need for each book.
page_10_links = []
books_links_1000 = []
book_url = []
titles = []
authors = []
num_reviews = []
num_ratings = []
genres = []
awards = []
settings = []
book_star_rating = []
book_num_pages = []
book_publish_year = []
book_series_list = []


# we need to scrape 1000 books, Each webpage has 100 books, so we need 10 webpages
def initial_links():
    for i in range(9, 11):
        url = f"https://www.goodreads.com/list/show/47.Best_Dystopian_and_Post_Apocalyptic_Fiction?page={i}"
        page_10_links.append(url)
    # print(page_10_link)
    return page_10_links


page_10_links = initial_links()


# print(page_10_links)

# The information of the book we need is inside the book link for each book, So, we need 1000 links
# for each book.

def book_1000_links():
    for i in page_10_links:
        page1 = requests.get(i)
        # print(page1)
        soup1 = BeautifulSoup(page1.content, 'html.parser')
        book_link = soup1.find_all('a', class_="bookTitle")

        for i in book_link:
            book_href = i.get('href')
            books_links_1000.append(book_href)

    # print(books_links_1000[4])
    return books_links_1000


books_links_1000 = book_1000_links()


# print(books_links_1000)


# Scrapper function to scrape each and every req element  from the web

def scraper():
    for url in books_links_1000:
        # Useragent and requesting the page
        headers = {'User-Agent': 'Chrome/98.0.4758.102'}
        book_link = f"https://www.goodreads.com{url}"
        book_url.append(book_link)
        pg = requests.get(book_link, headers=headers)
        time.sleep(10)
        soup = BeautifulSoup(pg.content, 'html.parser')
        time.sleep(10)

        # Titles
        if soup.find('h1', class_='gr-h1 gr-h1--serif') is not None:
            titles.append(soup.find('h1', class_='gr-h1 gr-h1--serif').text.strip())
        else:
            titles.append('Not found')

        # Authors
        if soup.find('span', itemprop='name') is not None:
            authors.append(soup.find('span', itemprop='name').text.strip())
        else:
            authors.append('Not found')

        # Num_reviews
        if soup.find('meta', itemprop='reviewCount') is not None:
            num_reviews.append(soup.find('meta', itemprop='reviewCount')['content'])
        else:
            num_reviews.append(0)
        # Num_ratings
        if soup.find('meta', itemprop='ratingCount') is not None:
            num_ratings.append(soup.find('meta', itemprop='ratingCount')['content'])
        else:
            num_ratings.append(0)

        # Genres
        if soup.find_all('a', class_='actionLinkLite bookPageGenreLink') is not None:
            genre = soup.find_all('a', class_='actionLinkLite bookPageGenreLink')
            genres_dump = []
            for i in genre:
                if len(genres_dump) <= 1 and f'{i.text}, ' not in genres_dump:
                    genres_dump.append(f'{i.text}, ')
                elif len(genres_dump) == 2 and f'{i.text}, ' not in genres_dump:
                    genres_dump.append(i.text)
                    genres.append(''.join(genres_dump))
                    break
                else:
                    continue
        else:
            genres.append('Not found')

        # Awards
        if soup.find('div', itemprop='awards') is not None:
            award = soup.find('div', itemprop='awards')
            award = award.text.replace('\n', '').replace('...more', ', ').replace('...less', '')
            awards.append(award)
        else:
            awards.append('Not found')

        # Places
        if soup.find('div', id='details') is not None:
            box = soup.find('div', id='details')
            box_div = box.find_all('div')
            setting = []
            for i in box_div:
                if i.text == 'Setting':
                    set_box = box_div[box_div.index(i) + 1].find_all('a')
                    for k in set_box:
                        setting.append(k.text.replace(',', ' -'))
            setting = ','.join(setting)
            settings.append(setting)
        else:
            settings.append('Not found')

        # avg_rating for each book
        if soup.find('span', {'itemprop': 'ratingValue'}) is not None:
            book_stars = soup.find('span', {'itemprop': 'ratingValue'})
            book_star_rating.append(book_stars.text.strip())
        else:
            book_star_rating.append('Not found')

        # no.of pages in the book
        if soup.find('span', {'itemprop': 'numberOfPages'}) is not None:
            pages_count = soup.find('span', {'itemprop': 'numberOfPages'})
            book_num_pages.append(pages_count.text.strip().split()[0])
        else:
            book_num_pages.append('Not found')

        # Book publishing year
        if soup.find('nobr', class_="greyText") is not None:
            publish_date = soup.find('nobr', class_="greyText").text.strip()[-5:-1]
            book_publish_year.append(publish_date)
        else:
            book_publish_year.append('Not found')

        # Book series-only few books have series and others dont.
        if soup.find('h2', id="bookSeries") is not None:
            book_series = soup.find('h2', id="bookSeries")
            a = book_series.text.strip()
            book_series_list.append(a[1:(len(a) - 1)])
        else:
            book_series_list.append('No series found')

        a = {'link': book_url,
             'title': titles,
             'author': authors,
             'num_reviews': num_ratings,
             'num_ratings': num_reviews,
             'avg_rating': book_star_rating,
             'num_pages': book_num_pages,
             'original_publish_year': book_publish_year,
             'book_series': book_series_list,
             'genre': genres,
             'awards': awards,
             'places': settings}
        df = pd.DataFrame.from_dict(a, orient='index')
        df = df.transpose()
        # print(df)
        df.to_csv('100books.csv', mode='w', index=False, header=False)


scraper()


################################################################################################################
## missing data checker function
## please un comment the calling function when you required this.
## It gives the no.of missing/nan values in the csv
## Please update the path of new csv file.


def missing_data_checker():
    df = pd.read_csv("final.csv", sep=',',
                     names=['url', 'title', 'author', 'num_reviews', 'num_ratings', 'avg_stars', 'num_pages',
                            'publishing_year', 'series', 'genre', 'awards', 'places'])
    # print(df.dtypes)
    ####-0
    url_index = df.index[(df['url'] == '')].tolist()
    print(f"url : {len(url_index)}")

    ####-1
    title_index = df.index[(df['title'] == 'Not found')].tolist()
    print(f"title : {len(title_index)}")

    ####-2
    author_index = df.index[(df['author'] == 'Not found')].tolist()
    print(f"Author : {len(author_index)}")

    ####-3
    reviews_index = df.index[(df['num_reviews'] == 0)].tolist()
    print(f"reviews : {len(reviews_index)}")

    ####-4
    ratings_index = df.index[(df['num_ratings'] == 0)].tolist()
    print(f"ratings : {len(ratings_index)}")

    ####-5
    stars_index = df.index[(df['avg_stars'] == 0)].tolist()
    print(f"stars : {len(stars_index)}")

    ####-6
    pages_index = df.index[(df['num_pages'] == 0)].tolist()
    print(f"pages : {len(pages_index)}")
    # 27 books have no pages

    ####-7
    year_index = df.index[(df['publishing_year'] == 0)].tolist()
    print(f"years : {len(year_index)}")

    ###-8
    series_index = df.index[(df['series'] == 'No series found')].tolist()
    print(f"series : {len(series_index)}")

    ###-9
    genre_index = df.index[(df['genre'] == 'Not found')].tolist()
    print(f"genre : {len(genre_index)}")

    ###-10
    awards_index = df.index[(df['awards'] == 'Not found')].tolist()
    print(f"awards: {len(awards_index)}")

    ####-11
    places_index = df.index[(df['places'] == 'Not found')].tolist()
    print(f"places : {len(places_index)}")

    places_index = df.index[(df['places'] == '')].tolist()
    print(f"places : {len(places_index)}")


# missing_data_checker()

#########################################################################################################
#########################################################################################################
## function for scraping missing values.
## Each sepearate function created for each column, because we dont need to scrape all the columns.
# so the user can use a function that designed to scrape particular values in the colum
# all calling_functions are comented, please uncomment required missing column function
# facing problems with missing_places()function

# getting index of all not found titles values in the df
def scrape_missing_data():
    df = pd.read_csv("final.csv", sep=',',
                     names=['url', 'title', 'author', 'num_reviews', 'num_ratings', 'avg_stars', 'num_pages',
                            'publishing_year', 'series', 'genre', 'awards', 'places'])

    title_index = df.index[(df['title'] == 'Not found')].tolist()
    print(len(title_index))

    def missing_titles():
        for i in title_index:
            url = f"{df.iat[i, 0]}"
            pg = requests.get(url)
            soup = BeautifulSoup(pg.content, 'html.parser')
            time.sleep(10)
            if soup.find('h1', class_='gr-h1 gr-h1--serif') is not None:
                df.at[i, 'title'] = soup.find('h1', class_='gr-h1 gr-h1--serif').text.strip()
                df.to_csv('100books.csv', mode='w', index=False, header=False)
            else:
                df.at[i, 'title'] = 'Not found'
                df.to_csv('100books.csv', mode='w', index=False, header=False)

    # missing_titles()
    print("title cleaning is succesful")

    # # missed author names.

    author_index = df.index[(df['author'] == 'Not found')].tolist()
    print(len(author_index))

    def missing_authors():
        for i in author_index:
            url = f"{df.iat[i, 0]}"
            pg = requests.get(url)
            soup = BeautifulSoup(pg.content, 'html.parser')
            time.sleep(10)
            if soup.find('span', itemprop='name') is not None:
                time.sleep(15)
                df.at[i, 'author'] = soup.find('span', itemprop='name').text.strip()
                df.to_csv('100books.csv', mode='w', index=False, header=False)
            else:
                df.at[i, 'author'] = 'Not found'
                df.to_csv('100books.csv', mode='w', index=False, header=False)

    # missing_authors()

    print("author cleaning is sucessful")

    # # missed num_revies.

    reviews_index = df.index[(df['num_reviews'] == 0)].tolist()
    print(len(reviews_index))

    def missing_reviews():
        for i in reviews_index:
            url = f"{df.iat[i, 0]}"
            pg = requests.get(url)
            soup = BeautifulSoup(pg.content, 'html.parser')
            time.sleep(10)
            if soup.find('meta', itemprop='reviewCount') is not None:
                time.sleep(15)
                df.at[i, 'num_reviews'] = soup.find('meta', itemprop='reviewCount')['content']
                df.to_csv('100books.csv', mode='w', index=False, header=False)
            else:
                df.at[i, 'num_reviews'] = 0
                df.to_csv('100books.csv', mode='w', index=False, header=False)

    # missing_reviews()

    print("reviews cleaning is sucessful")

    # # missed num_ratings.

    ratings_index = df.index[(df['num_ratings'] == 0)].tolist()
    print(len(ratings_index))

    def missing_ratings():
        for i in ratings_index:
            url = f"{df.iat[i, 0]}"
            pg = requests.get(url)
            soup = BeautifulSoup(pg.content, 'html.parser')
            time.sleep(10)
            if soup.find('meta', itemprop='ratingCount') is not None:
                time.sleep(15)
                df.at[i, 'num_ratings'] = soup.find('meta', itemprop='ratingCount')['content']
                df.to_csv('100books.csv', mode='w', index=False, header=False)
            else:
                df.at[i, 'num_ratings'] = 0
                df.to_csv('100books.csv', mode='w', index=False, header=False)

    # missing_ratings()

    print("ratings part is sucessful")

    # missed avg_stars.

    stars_index = df.index[(df['avg_stars'] == 0)].tolist()
    print(stars_index)

    def missing_stars():
        for i in stars_index:
            url = f"{df.iat[i, 0]}"
            pg = requests.get(url)
            soup = BeautifulSoup(pg.content, 'html.parser')
            time.sleep(5)
            if soup.find('span', {'itemprop': 'ratingValue'}) is not None:
                time.sleep(5)
                df.at[i, 'avg_stars'] = soup.find('span', {'itemprop': 'ratingValue'}).text.strip()
                df.to_csv('100books.csv', mode='w', index=False, header=False)
            else:
                df.at[i, 'avg_stars'] = 0
                df.to_csv('100books.csv', mode='w', index=False, header=False)

    # missing_stars()
    print("stars rating part is sucessful")

    # missed num_pages.

    pages_index = df.index[(df['num_pages'] == 0)].tolist()
    print(len(pages_index))
    print(pages_index)

    def missing_pages():
        for i in pages_index:
            url = f"{df.iat[i, 0]}"
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
                df.at[i, 'num_pages'] = a
                df.to_csv('100books.csv', mode='w', index=False, header=False)
                print(f"succesful{i}")
            else:
                df.at[i, 'num_pages'] = 0
                df.to_csv('100books.csv', mode='w', index=False, header=False)
                print(f"fail{i}")

    # missing_pages()

    print("pages part is sucessful")

    # missed published_years.

    year_index = df.index[(df['publishing_year'] == 0)].tolist()
    print(len(year_index))
    print(year_index)

    def missing_years():
        for i in year_index[2:]:
            url = f"{df.iat[i, 0]}"
            print(i)
            print(url)
            pg = requests.get(url)
            soup = BeautifulSoup(pg.content, 'html.parser')
            a = soup.find('div', id="details")
            time.sleep(2)
            if a is not None:
                time.sleep(2)
                b = soup.find_all('div', class_='row')
                if b is not None:
                    if len(b) != 0 and len(b) >= 1:
                        c = b[1].text.split()
                        for k in c:
                            if k.isdigit() and len(k) == 4:
                                print(k)
                                df.at[i, 'publishing_year'] = k
                                df.to_csv('years_cleaned.csv', mode='w', index=False, header=False)
                                print(f"sucess{i}")
                    else:
                        df.at[i, 'publishing_year'] = 0
                        df.to_csv('years_cleaned.csv', mode='w', index=False, header=False)
                        print(f"fail{i}")

                else:
                    df.at[i, 'publishing_year'] = 0
                    df.to_csv('years_cleaned.csv', mode='w', index=False, header=False)
                    print(f"fail{i}")
            else:
                df.at[i, 'publishing_year'] = 0
                df.to_csv('years_cleaned.csv', mode='w', index=False, header=False)
                print(f"fail{i}")

    # missing_years()
    print("years was sucessful")

    ###-missing series
    series_index = df.index[(df['series'] == 'No series found')].tolist()
    print(len(series_index))
    print(series_index)

    def missing_series():
        for i in series_index:
            url = f"{df.iat[i, 0]}"
            pg = requests.get(url)
            soup = BeautifulSoup(pg.content, 'html.parser')
            time.sleep(15)
            if soup.find('h2', id="bookSeries") is not None:
                time.sleep(15)
                a = soup.find('h2', id="bookSeries").text.strip()
                df.at[i, 'series'] = a[1:(len(a) - 1)]
                df.to_csv('100books.csv', mode='w', index=False, header=False)
                print(f"sucess{i}")
            else:
                df.at[i, 'series'] = 'No series found'
                df.to_csv('100books.csv', mode='w', index=False, header=False)
                print(f"fail{i}")

    # missing_series()
    print("series was sucessful")

    # ###- genre
    genre_index = df.index[(df['genre'] == 'Not found')].tolist()
    print(len(genre_index))

    def missing_genre():
        for i in genre_index:
            url = f"{df.iat[i, 0]}"
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
                        df.at[i, 'genre'] = ''.join(genres_dump)
                        df.to_csv('100books.csv', mode='w', index=False, header=False)
                        break
                    else:
                        continue
                else:
                    df.at[i, 'genre'] = 'Not found'
                    df.to_csv('100books.csv', mode='w', index=False, header=False)

    # missing_genre()
    print("genre was sucessful")

    # # missed awards.

    awards_index = df.index[(df['awards'] == 'Not found')].tolist()
    print(len(awards_index))

    def missing_awards():
        for i in awards_index:
            url = f"{df.iat[i, 0]}"
            print(url)
            pg = requests.get(url)
            soup = BeautifulSoup(pg.content, 'html.parser')
            time.sleep(2)
            if soup.find('div', itemprop='awards') is not None:
                time.sleep(2)
                award = soup.find('div', itemprop='awards')
                awards_list = award.text.replace('\n', '').replace('...more', ', ').replace('...less', '')
                df.at[i, 'awards'] = awards_list
                df.to_csv('100books.csv', mode='w', index=False, header=False)
                print(f"sucess{i}")
            else:
                df.at[i, 'awards'] = 'Not found'
                df.to_csv('100books.csv', mode='w', index=False, header=False)
                print(f"fail{i}")

    # missing_awards()
    print("awards completed")

    # places missing
    place_index = df.index[(df['places'] == 'Not found')].tolist()
    print(len(place_index))
    print(place_index)

    def missing_places():
        for i in place_index:
            url = f"{df.iat[i, 0]}"
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
                    df.at[i, 'places'] = setting
                    df.to_csv('100books.csv', mode='w', index=False, header=False)
                    print(f"sucess{i}")
            else:
                df.at[i, 'places'] = 'Not found'
                df.to_csv('100books.csv', mode='w', index=False, header=False)
                print(f"fail{i}")

    # missing_places()
    print("places was done")


# scrape_missing_data()

#############################################################################################################
#############################################################################################################
#############################################################################################################
def preprocessing():
    df = pd.read_csv(r'C:\Users\omolara\Documents\strive school\build-week-gryffindor\final.csv', header=None)
    df.columns = ['url', 'titles', 'author', 'num_reviews', 'num_ratings', 'avg_rating', 'num_pages',
                  'original_publish_year', 'book_series', 'genre', 'awards', 'places']

    def len_award():
        awards = df['awards'].tolist()
        a = []
        for i in awards:
            if i != 'Not found':
                i = str(i)
                i = i.split(',')
                a.append(len(i))

            else:
                a.append(0)

        b = df.assign(awards_len=a)
        return b

    df1 = len_award()

    def avg_rating_clean_up():
        avg_ratin = df['avg_rating'].tolist()
        c = []
        for i in avg_ratin:
            if i != 'Not found':
                c.append(i)

            else:
                c.append(0)

        d = df1.assign(average_rating_flo=c)
        d['average_rating_flo'] = d['average_rating_flo'].astype(float)
        return d

    df2 = avg_rating_clean_up()

    # print(df2)

    # # # # #defining a function for the min-max normalization
    def min_max_norm():
        minmax_norm = df2.copy()
        minmax_norm
        column = 'average_rating_flo'
        minmax_norm[column] = 1 + (minmax_norm[column] - minmax_norm[column].min()) / (
                    minmax_norm[column].max() - minmax_norm[column].min()) * 9
        e = df2.assign(minmax_norm_ratings=minmax_norm[column])
        return e

    df3 = min_max_norm()
    # print(df3)

    # # #finding the mean of avg_ratings column
    average = df3.average_rating_flo.mean()

    # print(average)
    # defining a function for the mean normalization
    def mean_norm():
        mean_normal = df2.copy()
        column = 'average_rating_flo'
        mean_normal[column] = 1 + (mean_normal[column] - average) / (
                    mean_normal[column].max() - mean_normal[column].min()) * 9
        f = df3.assign(mean_norm_ratings=mean_normal[column])
        return f

    df4 = mean_norm()

    # print(df4)

    # Visualization

    # group thr group by original published year and get the mean of the min_max_norm_rating

    g = df4.groupby('original_publish_year')['minmax_norm_ratings'].mean()
    df5 = pd.DataFrame(g)
    df5.reset_index(inplace=True)
    df5.rename(
        columns={'original_publish_year': 'original_publish_year2', 'minmax_norm_ratings': 'Ratings minmax mean'},
        inplace=True)
    # print(df5)
    ddf5 = df5[df5['original_publish_year2'] > 0]

    print(ddf5)

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.scatter(ddf5['original_publish_year2'], ddf5['Ratings minmax mean'], color='darkred', s=25, alpha=0.5,
                cmap='spectral');
    plt.xlim(1500, 2100, )
    plt.ylim(0.5, 10)
    plt.xlabel('Publish year of books')
    plt.ylabel('Minmax Ratings')
    plt.title('Books by original publshed year and mean of the Minmax  normalization ratings')
    plt.colorbar();
    plt.legend()

    # no of ratings and actual rating
    h = df4[['num_reviews', 'average_rating_flo']]

    df6 = h.sort_values('average_rating_flo', ascending=False)
    print(df6)

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.scatter(df6['average_rating_flo'], df6['num_reviews'], color='darkred', s=25)
    plt.xlabel('average_rating_flo')
    plt.ylabel('num_reviews')
    plt.title('Number of rating and Actual rating of the book ')
    plt.legend()
    # Can this be used to make the decision to read a book or not?

    # no of award and ratings

    i = df4[['average_rating_flo', 'awards_len']]

    df7 = i.sort_values('awards_len', ascending=False)
    ddf7 = df7[df7['awards_len'] > 0]

    print(ddf7)

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.bar(ddf7['awards_len'], ddf7['average_rating_flo'], color='darkred')
    # plt.ylim(1,5)
    # plt.xlim(1,43)
    plt.xlabel('num of award ')
    plt.ylabel('average rating')
    plt.title('number of award and average rating')
    plt.legend()

    # num of rating , average_rating

    j = df4[['average_rating_flo', 'num_ratings']]

    df8 = j.sort_values('num_ratings', ascending=False)
    print(df8)

    ##num of rating , no_of _pages

    j = df4[['num_pages', 'num_ratings']]

    df8 = j.sort_values('num_ratings', ascending=False)
    print(df8)

    # # #create a function that  returns the maximum minmax rating
    def author_name(name: str):
        k = df3.loc[df['author'] == name]
        l = k.sort_values('minmax_norm_ratings', ascending=False)
        return k.iloc[0, 0]

    print(author_name('Dean F. Wilson'))

    # plt a graph of


preprocessing()