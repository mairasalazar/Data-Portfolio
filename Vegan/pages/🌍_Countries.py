#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
from app_functions import create_df_countries, create_map, countries, create_df_keywords

#--------------------------------- ---------------------------------  ---------------------------------
#--------------------------------- SETTING UP THE APP
#--------------------------------- ---------------------------------  ---------------------------------

st.set_page_config(page_title="Countries | Vegan News", 
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
    title_image = Image.open(Path(__file__).parents[2] / 'Vegan/resources/header_christina-deravedisian-unsplash.jpg')
    st.image(title_image)
with col3:
    st.write('')

st.write('') # Horizontal space
st.text("") # Horizontal space

st.markdown("### **How often countries are mentioned in articles**")
col2_1, col2_2, col2_3 = st.columns((1,1,2), gap="large")
with st.container():
    # Dataframe and display how many times countries are mentioned in articles    
    with col2_1:
        where_to_look = st.radio(
        "Count countries mentioned in:",
        ("Articles' text", "Articles' title"), horizontal=True)

        if where_to_look == "Articles' text":
            df_countries = create_df_countries(input_df, 'Text')
        else:
            df_countries = create_df_countries(input_df, 'Title')
        st.dataframe(df_countries[['Country', 'Number of times']].head(10), hide_index=True)
    with col2_2:
        # See how many times a specific country was mentioned
        country_input = st.selectbox(label = 'What country do you want to check?', options = countries(with_abbreviations=False), help='Pick a country to see how many times it was mentioned.')
        try:
            number = df_countries[df_countries.Country==country_input.capitalize()]['Number of times'].item()
            st.write(f'{country_input} was cited {number} time(s)')
        except:
            st.write(f'Sorry, "{country_input}" is not a valid country name.')
        st.info('United Kingdom results include mentions of "UK". United States results include mentions of "USA".')
    
    # Display map
    with col2_3:
        projection_type = st.radio(
        "Which type of projection do you want for the map below?",
        ("Orthographic (globe)", "Equirectangular (plane)"), horizontal=True)

        if projection_type == "Orthographic (globe)":
            figure = create_map(df_countries, 'orthographic')
        else:
            figure = create_map(df_countries, 'equirectangular')
        st.plotly_chart(figure, use_container_width=True, sharing="streamlit")
    

