from ast import IsNot
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import time

filepath = Path('100books.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)

# empty lists for each scraping element that we need for each book.
page_10_links = []
books_links_1000 = []
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
    for i in range(1, 2):
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

        for i in book_link[45:51]:
            book_href = i.get('href')
            books_links_1000.append(book_href)

    # print(books_links_1000[4])
    return books_links_1000


books_links_1000 = book_1000_links()


# print(books_links_1000)



# creating data frame
df = pd.DataFrame(
    {'avg_rating':book_star_rating,
     'book_pages': book_num_pages,
     'publish_year':book_publish_year,
     'book_series':book_series_list})

df.to_csv('100books.csv',index=False)



# Scraper function to scrape and clean required elements from the web.
def book_avg_rating():
    # for 1st 100 books, i was giving range of first 100 books.

    for i in books_links_1000:
        time.sleep(5)
        url = f"https://www.goodreads.com{i}"
        print(url)
        page1 = requests.get(url)
        # print(page1)
        soup1 = BeautifulSoup(page1.content, 'html.parser')

        # avg_rating for each books
        book_stars = soup1.find('span', {'itemprop': 'ratingValue'})
        time.sleep(5)
        if book_stars is not None:
            time.sleep(5)
            book_star_rating.append(book_stars.text.strip())
        else:
            book_star_rating.append('not found')

        time.sleep(5)

        # no.of pages in the book
        pages_count = soup1.find('span', {'itemprop': 'numberOfPages'})
        time.sleep(5)
        if pages_count is not None:
            book_num_pages.append(pages_count.text.strip().split()[0])
        else:
            book_num_pages.append('not found')
        time.sleep(5)

        # Book publishing year
        publish_date = soup1.find('nobr', class_="greyText").text.strip()[-5:-1]

        if publish_date is not None:
            book_publish_year.append(publish_date[-5:-1])
            time.sleep(10)
        else:
            print("not found")

        # Book series-only few books have series and others dont.
        book_series = soup1.find('h2', id="bookSeries")
        time.sleep(5)
        if len(book_series.contents) > 1:
            time.sleep(5)
            a = book_series.a.text.strip()
            book_series_list.append(a[1:(len(a) - 1)])
        else:
            book_series_list.append('No series Found')
        time.sleep(5)

        df = pd.DataFrame(
            {'avg_rating':book_star_rating,
             'book_pages': book_num_pages,
             'publish_year':book_publish_year,
             'book_series':book_series_list})

    return book_star_rating


def book_details():
    for url in books_links_1000:
        # Useragent and requesting the page
        headers = {'User-Agent': 'Chrome/98.0.4758.102'}
        pg = requests.get(f"https://www.goodreads.com{url}", headers=headers)
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
                if len(genres_dump) <= 1 and i not in genres_dump:
                    genres_dump.append(f'{i.text}, ')
                elif len(genres_dump) == 2 and i not in genres_dump:
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

        df = pd.DataFrame(
            {'title': titles,
             'author': authors,
             'num_reviews': num_ratings,
             'num_ratings': num_reviews,
             'avg_rating': book_star_rating,
             'num_pages': book_num_pages,
             'original_publish_year': book_publish_year,
             'book_series': book_series_list,
             'genre': genres,
             'awards': awards,
             'places': settings})

        print(df)
        df.to_csv('100books.csv', mode='w', index=False, header=False)


book_details()
