import pandas as pd
from bs4 import BeautifulSoup
import requests

titles = []
authors = []
num_reviews = []
num_ratings = []
genres = []
awards = []
settings = []


headers = {'User-Agent': 'Mozzila/5.0'}
url = 'https://www.goodreads.com/book/show/40961427-1984'
pg = requests.get(url, headers=headers)
soup = BeautifulSoup(pg.content, 'html.parser')

if soup.find('h1', class_='gr-h1 gr-h1--serif') is not None:
    titles.append(soup.find('h1', class_='gr-h1 gr-h1--serif').text)
else:
    titles.append('')
if soup.find('span', itemprop='name') is not None:
    authors.append(soup.find('span', itemprop='name').text)
else:
    authors.append('')
if soup.find('meta', itemprop='reviewCount') is not None:
    num_reviews.append(soup.find('meta', itemprop='reviewCount')['content'])
else:
    num_reviews.append(0)
if soup.find('meta', itemprop='ratingCount') is not None:
    num_ratings.append(soup.find('meta', itemprop='ratingCount')['content'])
else:
    num_ratings.append(0)

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
    genres.append('')

if soup.find('div', itemprop='awards') is not None:
    award = soup.find('div', itemprop='awards')
    award = award.text.replace('\n', '').replace('...more', ', ').replace('...less', '')
    awards.append(award)
else:
    awards.append('')

if soup.find('div', id='details') is not None:
    box = soup.find('div', id='details')
    box_div = box.find_all('div')
    setting = []
    t = 0
    for i in box_div:
        if i.text == 'Setting':
            t = 1
            set_box = box_div[box_div.index(i) + 1].find_all('a')
            for k in set_box:
                setting.append(k.text.replace(',', ' -'))
    setting = ','.join(setting)
    settings.append(setting)
else:
    settings.append([''])

# if box.find('nobr', class_='greyText') is not None:
#     publish_date = box.find('nobr', class_='greyText').text.strip()[-5:-1]



### Naga
# avg_rating(stars)
book_stars = soup.find('div', id="bookMeta")
star_count = book_stars.find('span', {'itemprop': 'ratingValue'})
stars_value = star_count.text
print(stars_value)

# num_pages
book_pages = soup.find('div', class_="row")
pages_count = book_pages.find('span', {'itemprop': 'numberOfPages'})
pages_value = pages_count.text
print(pages_value)

# series
book_series = soup.find('div', id="bookDataBox")
series_count = book_series.a.text
print(series_count)
# note that some books does not have series- use if condition in that case

# Book_year
book_publish = soup.find('div', id='details')
publish_date = book_publish.find('nobr', class_="greyText").text
print(publish_date)
