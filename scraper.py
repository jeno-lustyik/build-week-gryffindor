from bs4 import BeautifulSoup
import requests

url = 'https://www.goodreads.com/book/show/40961427-1984'
pg = requests.get(url)
soup = BeautifulSoup(pg.content, 'html.parser')


title = soup.find('h1', class_='gr-h1 gr-h1--serif').text
author = soup.find('span', itemprop='name').text
num_reviews = soup.find('meta', itemprop='reviewCount')['content']
num_ratings = soup.find('meta', itemprop='ratingCount')['content']

genre = soup.find_all('a', class_='actionLinkLite bookPageGenreLink')
genres = []
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
print(genres)

awards = soup.find('div', itemprop='awards')
awards = awards.text.replace('\n', '').replace('...more', ', ').replace('...less', '')
print(awards)

box = soup.find('div', id='details')
box_div = box.find_all('div')
setting = []
for i in box_div:
    if i.text == 'Setting':
        set_box = box_div[box_div.index(i) + 1].find_all('a')
        for k in set_box:
            setting.append(k.text.replace(',', ' -'))
setting = ','.join(setting)
print(setting)

publish_date = box.find('nobr', class_='greyText').text.strip()[-5:-1]

print(publish_date)

### Naga
# avg_rating(stars)
book_stars = soup.find('div', id="bookMeta")
star_count = book_stars.find('span', {'itemprop': 'ratingValue'})
stars_value = star_count.text
print(stars_value)

# num_pages
book_pages = soup.find('div', class_ = "row")
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
publish_date = book_publish.find('nobr',class_="greyText").text
print(publish_date)