import pandas as pd
import numpy as np
import streamlit as st
import pickle
from streamlit_option_menu import option_menu
#from pandas_profiling import ProfileReport
import time
import pickle
from pathlib import Path

import streamlit_authenticator as stauth

#----------------------------User Authentication-------------------------#


#-------------------------------------------------------------------------#

#loading the model
#weather_model = pickle.load(open('C:\Users\gkuma\Documents\Python\DeployedModel\weathercloudmodel\weather_model.sav', 'rb'));



#sidebar for navigation
with st.sidebar:
    selected = option_menu('Welcome To Our Model Prediction',
    ['Home','Data','Weather Prediction','Conversion'],
    icons = ['house','bar-chart','cloud-haze2','arrows-angle-contract'],  #through bootstrap
    default_index=0
    )

if(selected == 'Home'):
    #page title
    st.title('Secure Communication Based IoT Weather Forecasting')
    with st.expander('About this Project'):
        st.subheader('Provides refined and targeted forecasts as it involve the integration of advanced technologies such as machine learning, big data analysis, and cloud computing, to produce more accurate and localized forecasts.')
    #st.image('')
   # if st.button('Click to continue',):
   # slider = st.slider('text', 0, 130, 25)

if(selected == 'Data'):
    st.header('Data profile')
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        #slider completion
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1)
        st.subheader('DataFrame')
        st.write(df)
        st.subheader('Descriptive Statistics')
        st.write(df.describe())
   
#      df = pd.read_csv('C:/Users/gkuma/Downloads/JupyterNotebook/Datasets/drug200.csv')
#      profile = ProfileReport(df,title='Profile Report')


if(selected == 'Weather Prediction'):
    #page title
    st.title('Weather Prediction Using ML')
    
    #creating columns
    col1, col2, col3 = st.columns(3)

    with col1:
        Temperature = st.text_input('Temperature level')

    with col2:
        Humidity = st.text_input('Humidity level')
    with col3:
        Pressure = st.text_input('Pressure Level')

    #creating a null string to store outcome result
    weather_result = ''

    #creating a button for prediction
    if st.button('Weather Prediction Result'):
        #weather_predict = weather_model.predict([[Temperature,Humidity,Pressure]])  #weather_model function in which model is defined

       # if(weather_predict[0]==1):
            weather_result = 'It will rain'
       # else:
            weather_result = 'No rainfall'

if(selected == 'Conversion'):
    st.header('Converting Celsius to Farenheit and Vice-versa')
    def fh_to_cel():
        st.session_state.cel = (st.session_state.fh/0.5556 - 32)
    def cel_to_fh():
        st.session_state.fh = (st.session_state.cel*1.8 + 32)
    
    col1, spacer, col2 = st.columns([2,1,2])
    with col1:
        fahrenheit = st.number_input("Fahrenheit:", key = "fh", on_change = fh_to_cel)
    with col2:
          celsius = st.number_input("Celsius:", key = "cel", on_change = cel_to_fh)
    st.button('Reset')
        


    
###########################################################################footer ctrl+/
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)