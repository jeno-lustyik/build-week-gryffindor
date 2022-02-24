import re

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# titles
st.title("Annual Dystopian Book Expo")
st.subheader("An insight into the best Dystopian books and authors")

headers = ['url', 'titles', 'author', 'num_ratings', 'num_reviews', 'avg_rating', 'num_pages', 'publish_date', 'series',
           'genres', 'awards', 'places']
df = pd.read_csv(r'D:\Users\lusty\Strive\GitHub\build-week-gryffindor\preprocessed.csv', header=0)

if st.button('Show data'):
    st.dataframe(df)

book_input = st.text_input('Author\'s name')
df1 = df.loc[df['author'].str.contains(book_input, flags=re.IGNORECASE)]
if len(book_input) > 0:
    st.dataframe(df1)
# num_pages / Ratings relationship

genre_selector = st.selectbox(label='Select a genre', options=df['genres'])
df2 = df.loc[df['num_pages'] != 0]
df2 = df2.loc[df['num_pages'] < df['num_pages'].quantile(q=0.95)]
df2 = df2.loc[df['num_ratings'] < df['num_ratings'].quantile(q=0.95)]

df2 = df2.loc[df['num_pages'] > df['num_pages'].quantile(q=0.05)]
df2 = df2.loc[df['num_ratings'] > df['num_ratings'].quantile(q=0.05)]

fig_pages = make_subplots(cols=2, rows=1)
fig_pages.add_trace(go.Scatter(x=df2['num_pages'], y=df2['minmax_norm_ratings'], mode='markers', name='Pages Scatter'), col=1, row=1)
fig_pages.add_trace(go.Histogram(x=df2['num_pages'], y=df2['minmax_norm_ratings'], histfunc='avg', nbinsx=10, name='Pages Histogram'), col=2, row=1)
fig_pages.update_layout(bargap=0.1)

st.plotly_chart(fig_pages)

#
# fig_scatter = px.scatter(df2, x=df2['num_pages'], y=df2['minmax_norm_ratings'], color=df2['minmax_norm_ratings'])
# st.plotly_chart(fig_scatter)
# fig_hist_ratings = px.histogram(df2, x=df2['num_pages'], y=df2['minmax_norm_ratings'], nbins=10, histfunc='avg')
# fig_hist_ratings.update_layout(bargap=0.1)
# st.plotly_chart(fig_hist_ratings)


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
    x=df5['titles'], y=df5['avg_rating'],
    row=1, col=1)
fig_places.add_scatter(
    x=df6['titles'], y=df6['avg_rating'],
    row=1, col=2)
st.plotly_chart(fig_places)
st.dataframe(df6)
