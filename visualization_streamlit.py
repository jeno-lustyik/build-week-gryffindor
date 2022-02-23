import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Title
st.title("Annual Dystopian Book Expo")
st.subheader("An insight into the best Dystopian books and authors")

headers = ['url', 'title', 'author', 'num_ratings', 'num_reviews', 'avg_rating', 'pages', 'publish_date', 'series', 'genres', 'awards', 'places']
df = pd.read_csv(r'D:\Users\lusty\Strive\GitHub\build-week-gryffindor\1000books.csv')

if st.button('Show data'):
    st.dataframe(df)

df1 = df.groupby(['pages'])

st.text(df1)

# fig_hist_pages = px.histogram(df1, x=df1.pages, y=df1.avg_rating)
# st.plotly_chart(fig_hist_pages)