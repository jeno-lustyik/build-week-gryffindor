import re
import os

from matplotlib import container
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import base64
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Title
st.title("Annual Dystopian Book Expo")
st.subheader("An insight into the best Dystopian books and authors")


#headers = ['url', 'title', 'author', 'num_ratings', 'num_reviews', 'avg_rating', 'pages', 'publish_date', 'series', 'genres', 'awards', 'places']
df = pd.read_csv(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\final.csv',header=None)
df.columns = ['url', 'title', 'author', 'num_ratings', 'num_reviews', 'avg_rating', 'pages', 'publish_date', 'series', 'genres', 'awards', 'places']

if st.button('Show data'):
    st.dataframe(df)


def user_interaction():
    st.sidebar.header("Customer Input Interaction")
    book_filters = ['Book & Author', 'Published year', 'page & ratings']
    page = st.sidebar.radio('Filters', book_filters)

    if page == 'Book & Author':
        selected_book = st.sidebar.text_input('Search By Book Name')
        selected_author = st.sidebar.text_input('Search by Author name')
       
        if selected_book != "" and selected_author == "":
            df2 = df.loc[df.title.str.contains(selected_book, flags=re.IGNORECASE)]
            st.dataframe(df2)
        # if book and author name selected.
        elif selected_book != "" and selected_author != "":
            df2 = df.loc[df.title.str.contains(selected_book, flags=re.IGNORECASE) | df.author.str.contains(selected_author, flags=re.IGNORECASE)]
            st.dataframe(df2)
        elif selected_book == "" and selected_author != "":
            df2 = df.loc[df.author.str.contains(selected_author, flags=re.IGNORECASE)]
            st.dataframe(df2)
        else:
            st.subheader("Please search for your required **Book** or favourite **Author**")
    elif page == 'page & ratings':
        selected_pages = st.sidebar.select_slider("Select no.of pages:", options=range(1,1100), value=100)
        st.sidebar.write("ma no.of pages", selected_pages)

        check_star1 = st.sidebar.checkbox("Average Rating- 0 to 1")
        check_star2 = st.sidebar.checkbox("Average Rating- 1 to 2")
        check_star3 = st.sidebar.checkbox("Average Rating- 2 to 3")
        check_star4 = st.sidebar.checkbox("Average Rating- 3 to 4")
        check_star5 = st.sidebar.checkbox("Average Rating- 4 to 5")
        st.sidebar.write("ma no.of pages", selected_pages)
        if selected_pages>=102:
            df2 = df.loc[df.pages <= selected_pages]
            st.dataframe(df2)
        elif check_star1:
            df2 = df.loc[(df.avg_rating >= 0.00) & (df.avg_rating<=0.99)]
            st.dataframe(df2)
        elif check_star2:
            df2 = df.loc[(df.avg_rating >= 1.00) & (df.avg_rating<=1.99)]
            st.dataframe(df2)
        elif check_star3:
            df2 = df.loc[(df.avg_rating >= 2.00) & (df.avg_rating<=2.99)]
            st.dataframe(df2)
        elif check_star4:
            df2 = df.loc[(df.avg_rating >= 3.00) & (df.avg_rating<=3.99)]
            st.dataframe(df2)
        elif check_star5:
            df2 = df.loc[(df.avg_rating >= 4.00) & (df.avg_rating<=4.99)]
            st.dataframe(df2)
        else:
            st.write("Please select a valid page number or required rating")

    else:
        selected_year = st.sidebar.selectbox('Year',reversed(range(1800,2024)), index=0)
        selected_years_range = st.sidebar.select_slider("Select range of years", options=range(1800,2023), value=[int(1800),int(1900)])
        years_range = [int(selected_years_range[0]),int(selected_years_range[1])]
        st.sidebar.write("Selected range of years:", years_range)
        if years_range[0]!= 1800 and years_range[1]!=1900:
            df2 = df.loc[df.publish_date.isin(range(years_range[0],years_range[1]))]
            st.dataframe(df2)
        elif years_range[0]==years_range[1]:
            df2 = df.loc[df.publish_date == years_range[0]]
            st.dataframe(df2)
        else:
            df2 = df.loc[df.publish_date == selected_year]
            st.dataframe(df2)

user_df = user_interaction()
st.write(user_df)

st.write("Suggestions to Customer")
def sug_cust():
    book_sug = ['Authors with most awards', 'Top Rated books']
    page = st.radio('Select one', book_sug)

    if page == 'Authors with most awards':
        def most_award_author():
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
            data = [df1["author"], df1["awards_len"]]
            headers = ["author", "no.of awards"]
            df2= pd.concat(data, axis=1, keys=headers)
            df3= df2.sort_values(by='no.of awards', ascending=False)
            df4 = df3.head(10)
            # bar chart need to be plotted
            author_bar = px.bar(df4, df4['author'],df4['no.of awards'])
            st.plotly_chart(author_bar)
        aa_df = most_award_author()
        st.write(aa_df)
    if page == "Top Rated books":
        def book_img_rating():
            st.write("Top rated books")
            col1,col2,col3,col4,col5,col6,col7,col8,col9,col10=st.columns(10)
            with col1:
                image1 = Image.open(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\img\1-5.0.jpg')
                st.image(image1, caption = 'Breakaway')
            # col-2
            with col2:
                image1 = Image.open(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\img\2-4.83.jpg')
                st.image(image1, caption = 'Earth Flown')
            # col-3
            with col3:
                image1 = Image.open(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\img\3-4.78.jpg')
                st.image(image1, caption = 'Zombie Road 5')
            # col-4
            with col4:
                image1 = Image.open(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\img\4-4.77.jpg')
                st.image(image1, caption = 'Down and Rising')
            # col-5
            with col5:
                image1 = Image.open(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\img\5-5.77.jpg')
                st.image(image1, caption = 'Lost Helix')



        cont_img = book_img_rating()
        st.write(cont_img)

cust_sug_df = sug_cust()
st.write(cust_sug_df)



















