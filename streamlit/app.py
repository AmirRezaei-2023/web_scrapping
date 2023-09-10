import streamlit as st
import pandas as pd
"# 📊 Part_One : Filtering"

"## a.Year Filtering"
from PIL import Image
photo = Image.open('remix-moshkeldari-reza-pishro-hitava.ir_.jpg')

b1 = st.slider("ENTER THE BEGIN YEAR",min_value=1921,max_value=2023, key="10")
b2 = st.slider("ENTER THE END YEAR",min_value=1921,max_value=2023, key="20")

df = pd.read_csv('movie.csv', dtype={'id': str})

if b2<b1:
    st.image(photo)
elif b2 == b1:
    filtered_df = df[(df['year'] == b1)]
    st.table(filtered_df)
else:
    filtered_df = df[(df['year'] >= b1) & (df['year'] <= b2)]
    st.table(filtered_df)
    
"## b.Runtime Filtering"

t1 = st.slider("ENTER THE BEGIN YEAR",min_value=45,max_value=238, key="30")
t2 = st.slider("ENTER THE END YEAR",min_value=45,max_value=238, key="40")

if t2<t1:
    st.image(photo)
elif t2 == t1:
    filtered_df = df[(df['runtime'] == t1)]
    st.table(filtered_df)
else:
    filtered_df = df[(df['runtime'] >= t1) & (df['runtime'] <= t2)]
    st.table(filtered_df)
    
"## c.Stars Filtering"

person_df = pd.read_csv('person.csv',dtype={'person_id': str})
movie_df = pd.read_csv('movie.csv',dtype={'id': str})
cast_df = pd.read_csv('cast.csv',dtype={'person_id': str, 'movie_id': str})
new = pd.merge(cast_df,person_df,  how='left', left_on='person_id', right_on = 'person_id')
new_new = pd.merge(new,movie_df,  how='left', left_on='movie_id', right_on = 'id')
lis = new_new['name']

count = st.number_input('How many stars are you looking for?', min_value=1, step=1)

selected_values = []

for i in range(count):
    selected_value = st.selectbox(f'Star number {i+1}', options=lis.unique())
    selected_values.append(selected_value)
    
filtered_df = new_new[new_new['name'].isin(selected_values)]
st.table(filtered_df[['title','name']])

"## d.Genre Filtering"

genre_df = pd.read_csv('genre.csv',dtype={'movie_id': str})
genre_df.rename(columns={'name' : 'genre'}, inplace = True)
merged_genre = pd.merge(genre_df,movie_df,  how='left', left_on='movie_id', right_on = 'id')

lis_genre = merged_genre['genre']
selected_value = st.selectbox('Choose your Genre', options=lis_genre.unique())
    
filtered_df = merged_genre[merged_genre['genre']== selected_value]
st.table(filtered_df[['title','genre']])


"# 📊 Part_Two : Analysis"

"## a.10 Most Sales Films"

import matplotlib.pyplot as plt
sorted_df = movie_df.sort_values(by='gross_us_canada', ascending=False)
top_10_movies = sorted_df.head(10)
s = plt.figure(figsize=(10, 6))
plt.bar(top_10_movies['title'], top_10_movies['gross_us_canada'], width = 0.4)
plt.ylabel('gross_us_canada')
plt.title('10 Most Sales')
plt.xticks(rotation=45,fontsize=6)
st.pyplot(s)

"## b.5 Most Appearance Stars"

actor_counts = new_new['name'].value_counts()
top_5_actors = actor_counts.head(5)
e = plt.figure(figsize=(10, 6))
plt.bar(top_5_actors.index, top_5_actors.values, width = 0.4)
plt.ylabel('Appearances')
plt.title('5 Most Appearances')
plt.xticks(rotation=45,fontsize=10)
st.pyplot(e)

"## c.Genres Disribution"

genre_counts = merged_genre['genre'].value_counts()
p = plt.figure(figsize=(8, 8))
plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%')
plt.title('genres')
st.pyplot(p)

"## c.Parental Disribution"

genre_counts = merged_genre['parental_guide'].value_counts()
q = plt.figure(figsize=(8, 8))
plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%')
plt.title('Parental')
st.pyplot(q)

"## d.Age Ratings in Movie Genres"

genre_age_counts = merged_genre.groupby(['genre', 'parental_guide']).size()
plt.figure(figsize=(10, 6))
genre_age_counts.unstack().plot(kind='bar', stacked=True)
plt.title('frquency of parental guides in each genre')
plt.ylabel('frequency')
plt.legend(title='parental_guide')
st.pyplot(plt.show())


"# 📊 Part_Three : Interactive Charts"

g = st.radio('Choose the genre:',options=lis_genre.unique())
filtered_merged_genre = merged_genre[merged_genre['genre'] == g]
top_selling_movies = filtered_merged_genre.nlargest(3, 'gross_us_canada')
plt.figure(figsize=(10, 6))
plt.bar(top_selling_movies['title'], top_selling_movies['gross_us_canada'],width = 0.4)
plt.title(f'Most top selling of {g}')
plt.ylabel('sales')
plt.xticks(rotation=45,fontsize=10)
st.pyplot(plt)
