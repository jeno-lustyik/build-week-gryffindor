import re

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Title
st.title("Annual Dystopian Book Expo")
st.subheader("An insight into the best Dystopian books and authors")

headers = ['url', 'title', 'author', 'num_ratings', 'num_reviews', 'avg_rating', 'pages', 'publish_date', 'series', 'genres', 'awards', 'places']
df = pd.read_csv(r'D:\Users\lusty\Strive\GitHub\build-week-gryffindor\preprocessed.csv')

df.to_csv()

if st.button('Show data'):
    st.dataframe(df)

auth_input = st.text_input('Author name')
column = df['author']
df1 = df.loc[df.author.str.contains(auth_input, flags=re.IGNORECASE)]
if len(auth_input) > 0 is not None:
    st.dataframe(df1)
# fig_scatter = px.scatter(df, x=df.avg_rating, y=df.num_pages, color=df.avg_rating)
# st.plotly_chart(fig_scatter)