import streamlit_authenticator as stauth

#importing the database.py file
import database as db

usernames = ["gkumar", "gkumar1"]
names = ["GAURAV", "KUMAR"]
passwords = ["123", "123"]
hashed_passwords = stauth.Hasher(passwords).generate()


for (username, name, hash_password) in zip(usernames, names, hashed_passwords):
    db.insert_user(username, name, hash_password)