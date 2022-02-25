import pandas as pd

df = pd.read_csv("final.csv", sep = ',' ,names=['url','title','author','num_reviews','num_ratings','avg_stars','num_pages','publishing_year','series','genre','awards','places'])
print(df.dtypes)
def missing_data_checker():
    ####-0
    url_index = df.index[(df['url']=='')].tolist()
    print(f"url : {len(url_index)}")

    ####-1
    title_index = df.index[(df['title']=='Not found')].tolist()
    print(f"title : {len(title_index)}")


    ####-2
    author_index = df.index[(df['author']=='Not found')].tolist()
    print(f"Author : {len(author_index)}")


    ####-3
    reviews_index = df.index[(df['num_reviews']==0)].tolist()
    print(f"reviews : {len(reviews_index)}")


    ####-4
    ratings_index = df.index[(df['num_ratings']==0)].tolist()
    print(f"ratings : {len(ratings_index)}")

    ####-5
    stars_index = df.index[(df['avg_stars']==0)].tolist()
    print(f"stars : {len(stars_index)}")


    ####-6
    pages_index = df.index[(df['num_pages']==0)].tolist()
    print(f"pages : {len(pages_index)}")
    # 27 books have no pages


    ####-7
    year_index = df.index[(df['publishing_year']==0)].tolist()
    print(f"years : {len(year_index)}")

    ###-8
    series_index = df.index[(df['series']=='No series found')].tolist()
    print(f"series : {len(series_index)}")


    ###-9
    genre_index = df.index[(df['genre']=='Not found')].tolist()
    print(f"genre : {len(genre_index)}")


    ###-10
    awards_index = df.index[(df['awards']=='Not found')].tolist()
    print(f"awards: {len(awards_index)}")


    ####-11
    places_index = df.index[(df['places']=='Not found')].tolist()
    print(f"places : {len(places_index)}")

    places_index = df.index[(df['places']== '')].tolist()
    print(f"places : {len(places_index)}")

missing_data_checker()