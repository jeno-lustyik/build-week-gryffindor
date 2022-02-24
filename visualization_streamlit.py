import re

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Title
st.title("Annual Dystopian Book Expo")
st.subheader("An insight into the best Dystopian books and authors")

headers = ['url', 'title', 'author', 'num_ratings', 'num_reviews', 'avg_rating', 'pages', 'publish_date', 'series',
           'genres', 'awards', 'places']
df = pd.read_csv(r'D:\Users\lusty\Strive\GitHub\build-week-gryffindor\final.csv', header=None)
df.columns = headers

if st.button('Show data'):
    st.dataframe(df)

book_input = st.text_input('Author\'s name')
df1 = df.loc[df['author'].str.contains(book_input, flags=re.IGNORECASE)]
if len(book_input) > 0:
    st.dataframe(df1)

# Pages / Ratings relationship

df2 = df.loc[df['pages'] != 0]
fig_scatter = px.scatter(df2, x=df2['pages'], y=df2['avg_rating'], color=df2['avg_rating'])
st.plotly_chart(fig_scatter)

# Locations in the book: is a book rated higher if it happens in america?

df3 = df.dropna(axis=0, subset=['places'])
df5 = df3.loc[df3['places'].str.contains('america', flags=re.IGNORECASE)]
df5 = df5.sort_values(by='avg_rating')
# st.plotly_chart(fig_places)
df4 = pd.DataFrame(
    {'americas_rating': df3['avg_rating'].loc[df3['places'].str.contains('america', flags=re.IGNORECASE)],
     'americas_reviews': df3['num_reviews'].loc[df3['places'].str.contains('america', flags=re.IGNORECASE)]
     })
df6 = df3.loc[~df3['places'].str.contains('america', flags=re.IGNORECASE)]
df6 = df6.sort_values(by='avg_rating')

fig_places = make_subplots(rows=1, cols=2)
fig_places.add_scatter(
    x=df5['title'], y=df5['avg_rating'],
    row=1, col=1)
fig_places.add_scatter(
    x=df6['title'], y=df6['avg_rating'],
    row=1, col=2)
st.plotly_chart(fig_places)
st.dataframe(df6)
