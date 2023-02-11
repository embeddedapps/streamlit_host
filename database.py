import os

from deta import Deta
from dotenv import load_dotenv

# #load the environment variables
load_dotenv(".env")
DETA_KEY = os.getenv('DETA_KEY')
#DETA_KEY= 'd061eczc_2bi3UJ9a98PvDdmtYaciksXwJbuqoXi8'
#initialize with a product key
deta = Deta(DETA_KEY)

#connecting to database
db = deta.Base('streamlit_db')
def insert_user(username, name, password):
    return db.put({'key':username, 'name': name, 'password': password})

#for inserting users to db
#insert_user('gkumar', 'Gaurav Kumar', '123')

# #for fetching data from db
def fetch_all_users():
     res = db.fetch()
     return res.items
#print(fetch_all_users())

def get_user(username):
    return db.get(username)

def update_user(username, updates):
    return db.update(updates, username)

def delete_user(username):
    return db.delete(username)
#delete_user('gkumar')