#!/usr/bin/env python
# coding: utf-8


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
import datetime
from pathlib import Path

# Custom library
from app_functions import create_df_keywords, dates_article

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- SETTING UP THE APP
#--------------------------------- ---------------------------------  ---------------------------------

st.set_page_config(page_title="Dates | Vegan News", 
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

# Load data
input_df = create_df_keywords(st.session_state['fill_kws'], st.session_state['lower_df'])

#---------------------------------------------------------------#
# APP
#---------------------------------------------------------------#

# Image
col1, col2, col3 = st.columns((1,3,1))
with col1:
    st.write('')
with col2:
    title_image = Image.open(Path(__file__).parents[1] / 'Vegan/resources/header_christina-deravedisian-unsplash.jpg')
    st.image(title_image)
with col3:
    st.write('')

st.write('') # Horizontal space
st.text("") # Horizontal space


st.markdown("### **Date distribution for articles containing your keywords**")
col1_1, col1_2 = st.columns(2, gap="large")
with st.container():
    # Create and display histogram
    with col1_1:
        fig = px.histogram(input_df, x="Date", title='Frequency of publication of articles containing your keywords',
         color_discrete_sequence=['#a8ddb5'])
        st.plotly_chart(fig, use_container_width=True, sharing="streamlit")
    
    # Display summary of stats
    with col1_2:
        st.write("")
        st.write("")
        st.write('**Date stats**')  
        st.write(f'Your keyword(s): {st.session_state["fill_kws"]}')
        dic = dates_article(input_df)
        st.markdown(f"""
        * Month with most number of articles containing one of your keywords: **{dic['month_year']}**.
        * Year with most number of articles containing one of your keywords: **{dic['year']}**.
        * Longest time between articles: **{dic['max_time_between']}**, on **{dic['date_of_publication']}**.\
            The article before that was on **{dic['date_previous_publication']}**.
        * Last date of publication of an article containing one of your keywords: **{dic['date_max']}**.
        """)
        