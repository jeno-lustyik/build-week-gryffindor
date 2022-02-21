import requests
from bs4 import BeautifulSoup

page_10_links = [] 

for i in range(1,11):
    url = f"https://www.goodreads.com/list/show/47.Best_Dystopian_and_Post_Apocalyptic_Fiction?page={i}"
    page_10_links.append(url)

#print(page_10_link)
books_links_1000 = []

for i in page_10_links:
    page1 = requests.get(i)
    #print(page1)
    soup1 = BeautifulSoup(page1.content,'html.parser')
    book_link = soup1.find_all('a', class_ = "bookTitle")

    for i in book_link:
        book_href = i.get('href')
        books_links_1000.append(book_href)

print(books_links_1000[4])



#     for i in book_link:
#         book_href = i.href
#         books_links_1000.append(book_href)

# print(books_links_1000)
   


