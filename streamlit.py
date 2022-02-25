import re
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import base64
import numpy as np

# Title
st.title("Annual Dystopian Book Expo")
st.subheader("An insight into the best Dystopian books and authors")


#headers = ['url', 'title', 'author', 'num_ratings', 'num_reviews', 'avg_rating', 'pages', 'publish_date', 'series', 'genres', 'awards', 'places']
df = pd.read_csv(r'C:\Users\rnr31\Documents\GitHub\build-week-gryffindor\final.csv',header=None)
df.columns = ['url', 'title', 'author', 'num_ratings', 'num_reviews', 'avg_rating', 'pages', 'publish_date', 'series', 'genres', 'awards', 'places']

if st.button('Show data'):
    st.dataframe(df)

# auth_input = st.text_input('Author name')
# df1 = df.loc[df.author.str.contains(auth_input, flags=re.IGNORECASE)]
# st.dataframe(df1)
# fig_scatter = px.scatter(df, x=df.avg_rating, y=df.num_pages, color=df.avg_rating)
# st.plotly_chart(fig_scatter)
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
        # elif selected_pages>=102 and check_star1:
        #     df2 = df.loc[(df.pages <= selected_pages) & (df.avg_rating >= 0.00) & (df.avg_rating<=0.99)]
        #     st.dataframe(df2)
        # elif selected_pages>=102 and check_star2:
        #     df2 = df.loc[(df.pages <= selected_pages) & (df.avg_rating >= 1.00) & (df.avg_rating<=1.99)]
        #     st.dataframe(df2)
        # elif selected_pages>=102 and check_star3:
        #     df2 = df.loc[(df.pages <= selected_pages) & (df.avg_rating >= 2.00) & (df.avg_rating<=2.99)]
        #     st.dataframe(df2)
        # elif selected_pages>=102 and check_star4:
        #     df2 = df.loc[(df.pages <= selected_pages) & (df.avg_rating >= 3.00) & (df.avg_rating<=3.99)]
        #     st.dataframe(df2)
        # elif selected_pages>=102 and check_star5:
        #     df2 = df.loc[(df.pages <= selected_pages) & (df.avg_rating >= 4.00)]
        #     st.dataframe(df2)
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





