import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px 
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import streamlit as st
import country_converter as coco
from pathlib import Path


# Custom library
from app_functions import create_df_countries, create_map, load_data, create_text, countries, create_df_keywords

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- SETTING UP THE APP
#--------------------------------- ---------------------------------  ---------------------------------

st.set_page_config(page_title="Home | Vegan News", 
                   page_icon=":newspaper:", 
                   layout='wide')

# Set up a sidebar that remains throughout the app, in all pages. 
# Use session_state to save keywords entered by user.
if 'fill_kws' not in st.session_state:
    st.session_state['fill_kws'] = 'alternative protein'

def change_value():
    st.session_state['fill_kws'] = keywords
    return
    
with st.sidebar:
    st.markdown("### **Choose keywords**")
    st.markdown('These keywords will apply throughout the site. Feel free to change them as you want.')
    keywords = st.text_input(label = 'Write your keywords, separated by commas: ', value=st.session_state.fill_kws, key='fill_kws')
    enter = st.button("Let's do it!", key='submit_kws', on_click=change_value)

# Load dataset
news = pd.read_csv(Path(__file__).parents[1] / 'Vegan/Vegan_Articles.csv')
news['Date'] = pd.to_datetime(news['Date'], format="%m/%d/%Y")
news_lower = news.apply(lambda x: x.astype(str).str.lower())
news_lower['Date'] = pd.to_datetime(news_lower['Date'], format="%Y/%m/%d")
if 'original_df' not in st.session_state:
        st.session_state['original_df'] = news
if 'lower_df' not in st.session_state:
        st.session_state['lower_df'] = news_lower

input_df = create_df_keywords(st.session_state['fill_kws'], st.session_state['lower_df'])

#---------------------------------------------------------------#
# APP
#---------------------------------------------------------------#

# Introduction
col1, col2, col3 = st.columns((1,3,1))
with col1:
    st.write('')
with col2:
    title_image = Image.open(Path(__file__).parents[1] / 'Vegan/resources/header_christina-deravedisian-unsplash.jpg')
    st.image(title_image)
    st.write("")
with col3:
    st.write('')
st.write('')
st.markdown("An exploration of vegan news in the past 5 years, looking at keywords and the evolution of their use.")
st.markdown("""This app is a way to explore the [Vegan News dataset](https://www.kaggle.com/datasets/adrinlandaverdenava/vegan-news).
For more information, visit the [GitHub repo](https://github.com/mairasalazar/Data-Portfolio/tree/master/Vegan) or drop me a message on [LinkedIn](https://www.linkedin.com/in/maira-salazar/).""")
st.write('')

# Main app
col1_1, col1_2 = st.columns(2, gap="medium")

with st.container():
    # Dataframe containing articles
    with col1_1:
        st.markdown('### **Articles containing keywords**')
        # Display a sample:
        if len(input_df)>0:
            st.markdown("Here is a sample of articles containing your keyword(s):")
            x = min([10, len(input_df)])
            input_df_original = news[news.index.isin(input_df.index.to_list())]
            df_display = input_df_original.sample(x).reset_index(drop=True)
            st.dataframe(df_display)
            st.write(f'There are {len(input_df)} articles containing your keyword(s): {st.session_state["fill_kws"]}.')
            st.write("You can download a CSV file with all these articles containing your keywords 👇")
            csv = input_df_original.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download articles as CSV",
                csv,
                "articles.csv",
                "text/csv",
                key='articles-data'
            )
            
        else:
            st.write('Sorry, it seems like this word does not appear in the articles we have.')

    # Create and display wordcloud
    with col1_2:
        st.markdown("### **Common words in articles containing your keywords**")
        where_to_look_wordcloud = st.radio(
        "Create wordcloud based on:",
        ("Articles' text", "Articles' title"), horizontal=True)
        if where_to_look_wordcloud == "Articles' text":
            text = create_text(input_df, 'Text')
        else:
            text = create_text(input_df, 'Title')    
        stopwords = set(STOPWORDS) | set('s')
        stopwords_input = st.text_input('Type words to be excluded, separated by commas.',
                                            help='If you want any extra words to be excluded from the wordcloud, type them here. If not, leave the field blank.') 
        stopwords_list = [word.strip() for word in stopwords_input.split(',')]
        stopwords.update(stopwords_list)
        try:
            wordcloud = WordCloud(stopwords=stopwords, width=800, height=400, colormap='GnBu').generate(text)
            # Display the generated image:
            fig_cloud, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            fig_cloud.tight_layout(pad=0)
            st.pyplot(fig_cloud)
        except:
            st.write('Sorry, it seems like the keyword(s) you chose do not appear in the articles, so we cannot plot the wordcloud.')
