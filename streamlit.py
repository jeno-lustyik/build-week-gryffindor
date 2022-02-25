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
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image

# Title
st.title("Annual Dystopian Book Expo")
st.subheader("An insight into the best Dystopian books and authors")
st.write("Introduction:")
st.write("Our Boss want to make a Dystopian Book Expo in the central mall, He asked us to:")
st.write("1)Find Best 1000 books in this genre:")
st.write("2)Design a user Interaction software to know what books available in the book store.")
st.write("3)Analyze the data and find Insights")
st.write("")


def naga():
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
                st.subheader("Hey Reader! Make use of User-Interaction tool")
                st.write("Click arrow on the leftside")
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
    #st.write(user_df)

    st.write("")
    st.write("Note- Due to miscumminication,Our procurement team buys the book with highest ratings before our analysis")
    st.subheader("Hey Reader, Let check some Suggestions:")
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
            #st.write(aa_df)
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
                # col-6
                with col6:
                    image1 = Image.open(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\img\6-4.71.jpg')
                    st.image(image1, caption = 'Rotter Nation')
                #col-7
                with col7:
                    image1 = Image.open(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\img\7-4.71.jpg')
                    st.image(image1, caption = 'Linehan Saves')
                #col-8
                with col8:
                    image1 = Image.open(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\img\8-4.71.jpg')
                    st.image(image1, caption = 'Mars Base1')
                #col-9
                with col9:
                    image1 = Image.open(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\img\9-4.71.jpg')
                    st.image(image1, caption = 'Arid Lands')
                #col-10
                with col10:
                    image1 = Image.open(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\img\10-4.70.jpg')
                    st.image(image1, caption = 'Maya of the In-between')


            cont_img = book_img_rating()
            #st.write(cont_img)

    cust_sug_df = sug_cust()
    #st.write(cust_sug_df)
naga_df = naga()

def jeno():
    df = pd.read_csv(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\final.csv', header=None)
    book_input = st.text_input('Author\'s name')
    df1 = df.loc[df['author'].str.contains(book_input, flags=re.IGNORECASE)]
    if len(book_input) > 0:
        st.dataframe(df1)

    # minmax norm ratings and publish year

    g = df.groupby('original_publish_year')['minmax_norm_ratings'].mean()
    df5 = pd.DataFrame(g)
    df5.reset_index(inplace=True)
    df5.rename(columns={'original_publish_year': 'original_publish_year2', 'minmax_norm_ratings': 'Ratings minmax mean'}, inplace=True)
    ddf5 = df5[df5['original_publish_year2'] > 0]
    ddf5 = ddf5.loc[ddf5['original_publish_year2'] < ddf5['original_publish_year2'].quantile(q=0.95)]
    ddf5 = ddf5.loc[ddf5['original_publish_year2'] > ddf5['original_publish_year2'].quantile(q=0.05)]
    fig_publish = px.scatter(ddf5, ddf5['original_publish_year2'], ddf5['Ratings minmax mean'])
    st.plotly_chart(fig_publish)

    # no of ratings and actual rating
    h = df[['num_reviews','average_rating_flo']]

    df6 = h.sort_values('average_rating_flo', ascending= False)
    df6 = df6.loc[df6['num_reviews'] < df['num_reviews'].quantile(q=0.95)]
    df6 = df6.loc[df6['num_reviews'] > df['num_reviews'].quantile(q=0.05)]

    df6 = df6.loc[df6['average_rating_flo'] < df['average_rating_flo'].quantile(q=0.95)]
    df6 = df6.loc[df6['average_rating_flo'] > df['average_rating_flo'].quantile(q=0.05)]
    print(df6)

    fig_rating_num = px.scatter(df6, df6['average_rating_flo'], df6['num_reviews'])
    fig_rating_num.update_layout(title='Number of ratings based on actual ratings')

    st.plotly_chart(fig_rating_num)


    #ratings / awards relationship

    i = df[['average_rating_flo', 'awards_len']]

    df7 = i.sort_values('awards_len', ascending=False)
    ddf7 = df7[df7['awards_len'] > 0]

    fig_rating_awa = px.histogram(ddf7, ddf7['awards_len'], ddf7['average_rating_flo'], histfunc='avg', nbins=8)
    fig_rating_awa.update_layout(title='Ratings and number of awards correlation', bargap=0.1)
    st.plotly_chart(fig_rating_awa)
    # plt.ylim(1,5)
    # plt.xlim(1,43)

    df_top50 = df.sort_values(by=['minmax_norm_ratings'])
    df_top50 = df_top50.loc[df_top50['average_rating_flo'] < df['average_rating_flo'].quantile(q=0.95)]
    df_top50 = df_top50.loc[df_top50['num_pages'] > 0]
    df_top50 = df_top50.loc[df_top50['num_ratings'] > 10000]
    df_top50 = df_top50[0:50]
    st.dataframe(df_top50)


    # num_pages / Ratings relationship

    threshold_genres = st.slider('Set a threshold for books in genre:',1, 300)
    ser_genre = df['genre'].dropna()
    unique_genres = set(','.join(ser_genre).split(','))
    unique_genres = sorted(unique_genres)
    # counts = df['genre'].value_counts()
    # res = df[~df['genre'].isin(counts[counts < threshold_genres].index)]
    # st.dataframe(res)
    genre_selector = st.selectbox(label='Select a genre', options=unique_genres)
    df_genre_notna = df.dropna(subset=['genre'])
    df_genre = df_genre_notna.loc[df_genre_notna['genre'].str.contains(genre_selector, flags=re.IGNORECASE)]

    if len(df_genre) >= threshold_genres:
        df2 = df_genre.loc[df_genre['num_pages'] != 0]
        df2 = df2.loc[df['num_pages'] < df['num_pages'].quantile(q=0.95)]
        df2 = df2.loc[df['num_ratings'] < df['num_ratings'].quantile(q=0.95)]

        df2 = df2.loc[df['num_pages'] > df['num_pages'].quantile(q=0.05)]
        df2 = df2.loc[df['num_ratings'] > df['num_ratings'].quantile(q=0.05)]

        fig_pages = make_subplots(cols=2, rows=1)
        fig_pages.add_trace(go.Scatter(x=df2['num_pages'], y=df2['minmax_norm_ratings'], mode='markers', name='Pages Scatter'), col=1, row=1)
        fig_pages.add_trace(go.Histogram(x=df2['num_pages'], y=df2['minmax_norm_ratings'], histfunc='avg', nbinsx=10, name='Pages Histogram'), col=2, row=1)
        fig_pages.update_layout(bargap=0.1)

        st.plotly_chart(fig_pages)
    else:
        st.text('This genre does not have enough books to show the data.')

















