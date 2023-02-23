import pandas as pd
from pandas import DataFrame
import streamlit as st
import pickle
from streamlit_option_menu import option_menu
import time
import pickle

from pathlib import Path
import streamlit_authenticator as stauth
import database as db

from gspread_pandas import Spread,Client
from google.oauth2 import service_account

st.set_page_config(page_title="Weather App", page_icon=":bar_chart:", layout="wide")

#----------------------------User Login-------------------------#
users = db.fetch_all_users()

usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

credentials = {"usernames":{}}
for uname,name,pwd in zip(usernames, names, hashed_passwords):
    user_dict = {"name":name,"password":pwd}
    credentials["usernames"].update({uname:user_dict})

#authentication  
authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status == True:
    #loading the model
    #weather_model = pickle.load(open('C:\Users\gkuma\Documents\Python\DeployedModel\weathercloudmodel\weather_model.sav', 'rb'));
 
    #sidebar for navigation
    authenticator.logout("Logout","sidebar")
    with st.sidebar:
        selected = option_menu('Welcome To Our Model Prediction',
        ['Home','Algorithm','Live Data','Prediction','Conversion'],
        icons = ['house','bar-chart','activity','cloud-haze2','arrows-angle-contract'],  #through bootstrap
        default_index=0
        )

    if(selected == 'Home'):
        #page title
        st.title('Secure Communication Based IoT Weather Forecasting')
        with st.expander('About this Project'):
            st.subheader('Provides refined and targeted forecasts as it involve the integration of advanced technologies such as machine learning, data analysis, and cloud computing to produce more accurate and localized forecasts.')

    if(selected == 'Algorithm'):
        st.header('Select Algorithm')
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
                st.subheader('Data Info')
                st.bar_chart(df)
    
    #      df = pd.read_csv('C:/Users/gkuma/Downloads/JupyterNotebook/Datasets/drug200.csv')
    #      profile = ProfileReport(df,title='Profile Report')

    if(selected == 'Live Data'):
        with st.spinner('Loading...'):
            time.sleep(5)
        st.success('Done!')
        # Creating a Google Authentication connection object
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes = scope)
        client = Client(scope=scope,creds=credentials)
        spreadsheetname = "Data_From_Esp8266"
        spread = Spread(spreadsheetname,client = client)

        sh = client.open(spreadsheetname)
        worksheet_list = sh.worksheets()

        # Functions 
        @st.cache_data()
        def worksheet_names():
            sheet_names = []
            for sheet in worksheet_list:
                sheet_names.append(sheet.title)
            return sheet_names
        
        # Get the sheet as dataframe
        def load_the_spreadsheet(spreadsheetname):
            worksheet = sh.worksheet(spreadsheetname)
            df = DataFrame(worksheet.get_all_records())
            return df

        # Check whether the sheets exists
        what_sheets = worksheet_names()
        ws_choice = st.selectbox('Available worksheets',what_sheets)

        # Load data from worksheets
        df = load_the_spreadsheet(ws_choice)
        st.write(df)
  
    if(selected == 'Prediction'):
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
            # reset_state
            
 ###########################################################################footer ctrl+/
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)