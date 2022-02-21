import requests
from bs4 import BeautifulSoup

url = "https://www.goodreads.com/book/show/2767052-the-hunger-games"

page1 = requests.get(url)
#print(page1)
soup1 = BeautifulSoup(page1.content,'html.parser')

# avg_rating(stars)
book_stars = soup1.find('div', id="bookMeta")
star_count = book_stars.find('span', {'itemprop': 'ratingValue'})
stars_value = star_count.text
print(stars_value)

# rating_books
book_rating = soup1.find('div', id="bookMeta")
rating_count = book_rating.find('meta', {'itemprop': 'ratingCount'})
rating_value = rating_count.text
print(rating_value)

# review_counts
book_reviews = soup1.find('div', id="bookMeta")
reviews_count = book_reviews.find('meta', {'itemprop': 'reviewCount'})
reviews_value = reviews_count.text
#print(reviews_value)

# num_pages
book_pages = soup1.find('div', class_ = "row")
pages_count = book_pages.find('span', {'itemprop': 'numberOfPages'})
pages_value = pages_count.text
print(pages_value)


# series
book_series = soup1.find('div', id="bookDataBox")
series_count = book_series.a.text
print(series_count)
# note that some books does not have series- use if condition in that case

# Book_year
# req_list = []
#book_publish = soup1.find('div', id='details')
# publish_year = soup1.find_all('div', class_="row")
# get_value = publish_year.find_all('nbor')
# print(get_value)
# for i in publish_year:
#     req_values = i.text.strip()
#     req_list.append(req_values)
#print(req_list[1])
#print(publish_year)
# year_value = publish_year.text
# print(publish_year)
