import pandas as pd
import re

df = pd.read_csv("final.csv", sep = ',' ,names=['url','title','author','num_reviews','num_ratings','avg_stars','num_pages','publishing_year','series','genre','awards','places'])
# #print(df)
# a = df[df['title'].str.contains("1984", flags=re.IGNORECASE)]
# print(a)

### filtering data-frame

print(df.dtypes)

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


        #     selected_author = st.sidebar.text_input('Search by Author name')
#selected_year = st.sidebar.text_input(str('Year'))
#     selected_rating = st.sidebar.select_slider("Select rating/ range of rating", options=[1,2,3,4,5], value=[float(1.0),float(5.0)])
    


#     book_name = df.loc[df.title.str.contains(selected_book, flags=re.IGNORECASE)]
#     #st.dataframe(book_name)

#     df1 = df.loc[df.author.str.contains(selected_author, flags=re.IGNORECASE)]
#     #st.dataframe(df1)

#     st.subheader("Based on User preferences.")
#     #df2 = df.loc[df.publish_date == selected_year]
# # if nothing is selcted-full dataframe - works
#     #if selected_year==2023:
#         #st.dataframe(df)
#     # if only book name is selected
#     if selected_book != "":
#         df2 = df.loc[df.title.str.contains(selected_book, flags=re.IGNORECASE)]
#         st.dataframe(df2)
    
#     # if book and author name selected.
#     elif selected_book != "" and selected_author != "":
#         df2 = df.loc[df.title.str.contains(selected_book, flags=re.IGNORECASE) | df.author.str.contains(selected_author, flags=re.IGNORECASE)]
#         st.dataframe(df2)
#     # if year , book & author is selected
#     elif selected_author != "" and selected_book != "" and selected_year!=2023:
#         df2 = df.loc[df.publish_date == selected_year]
#         df3 = df2.loc[df2.author.str.contains(selected_author, flags=re.IGNORECASE) | df2.title.str.contains(selected_book, flags=re.IGNORECASE)]
#         st.dataframe(df3)
#     # if year and book is selected
#     elif selected_book!= "" and selected_author == "" and selected_year!=2023:
#         df2 = df.loc[df.publish_date == selected_year]
#         df3 = df2.loc[df2.title.str.contains(selected_book, flags=re.IGNORECASE)]
#         st.dataframe(df3)
#     # if only year is selected
#     else:
#         df2 = df.loc[df.publish_date == selected_year]
#         st.dataframe(df2)





