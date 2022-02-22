from ast import IsNot
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import time

filepath = Path('100books.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  

page_10_links = [] 
books_links_1000 = []

# we need to scrape 1000 books, Each webpage has 100 books, so we need 10 webpages
def initial_links():
    
    for i in range(1,11):
        url = f"https://www.goodreads.com/list/show/47.Best_Dystopian_and_Post_Apocalyptic_Fiction?page={i}"
        page_10_links.append(url)
    #print(page_10_link)
    return page_10_links
page_10_links=initial_links()
#print(page_10_links)

    # The information of the book we need is inside the book link for each book, So, we need 1000 links 
    # for each book.
    
def book_1000_links():
    for i in page_10_links:
        page1 = requests.get(i)
        #print(page1)
        soup1 = BeautifulSoup(page1.content,'html.parser')
        book_link = soup1.find_all('a', class_ = "bookTitle")

        for i in book_link[0:60]:
            book_href = i.get('href')
            books_links_1000.append(book_href)

    #print(books_links_1000[4])
    return books_links_1000
books_links_1000 = book_1000_links()
#print(books_links_1000)

#empty lists for each scraping element that we need for each book.
book_star_rating = []
book_num_pages = []
book_publish_year = []
book_series_list =[]

# Scraper function to scrape and clean required elements from the web.
def book_avg_rating():

    # for 1st 100 books, i was giving range of first 100 books. 

    for i in books_links_1000[0:50]:
        time.sleep(5)
        url = f"https://www.goodreads.com{i}"
        print(url)
        page1 = requests.get(url)
        #print(page1)
        soup1 = BeautifulSoup(page1.content,'html.parser')

        #avg_rating for each books
        book_stars = soup1.find('span', {'itemprop': 'ratingValue'})
        time.sleep(5)
        if book_stars is not None:
            book_star_rating.append(book_stars.text.strip())
        else:
            book_star_rating.append('not found')

        time.sleep(5)


        #no.of pages in the book
        pages_count = soup1.find('span', {'itemprop': 'numberOfPages'})
        time.sleep(5)
        if pages_count is not None:
            book_num_pages.append(pages_count.text.strip().split()[0])
        else:
            book_num_pages.append('not found')
        time.sleep(5)

        #Book publishing year
        publish_date = soup1.find('nobr',class_="greyText").text.strip()[-5:-1]
       
        
        if publish_date is not None:
            print(publish_date)
        else:
            print("not found")
          
        # Book series-only few books have series and others dont.
        book_series = soup1.find('h2', id="bookSeries")
        time.sleep(5)
        if len(book_series.contents)>1:
            time.sleep(5)
            a = book_series.a.text.strip()
            book_series_list.append(a[1:(len(a)-1)])
        else:
            book_series_list.append('No series Found')
        time.sleep(5)

        print(book_series_list)

    return book_star_rating
book_avg_rating()

df = pd.DataFrame(
    {'avg_rating':book_star_rating,
     'book_pages': book_num_pages,
     'publish_year':book_publish_year,
     'book_series':book_series_list})

df.to_csv('100books.csv',index=False)

#print(len(book_star_rating))
#print(len(book_num_pages))
# print(len(book_publish_year))
# print(len(book_series_list))
# print(book_series_list)

        





   


