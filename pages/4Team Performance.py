import streamlit as st
import base64
import sqlite3
from collections import defaultdict as dd
import pandas as pd 
st.set_page_config(page_title='Register', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)
def text_field(label, columns=None, **input_params):
    c1, c2 = st.columns(columns or [1, 4])
    c1.markdown("##")
    c1.markdown(label)
    input_params.setdefault("key", label)
    return c2.text_input("", **input_params)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
def validate(name, loc, password):
    sqliteConnection = sqlite3.connect('teams.db')
    cursor = sqliteConnection.cursor()
    name = name.lower()
    loc = loc.lower()
    cursor.execute('SELECT o_password FROM teamy WHERE org_name = (?) AND org_loc = (?)', (name, loc))
    ans = cursor.fetchall()
    for x in ans:
        if(x[0] == password):
            return True
    return False
add_bg_from_local('images/bg.jpg')
t = '<p style = "font-size:60px; text-align:center; font-family:Georgia">TeamZ for Teams</p>'
st.markdown(t, unsafe_allow_html=True)
sqliteConnection = sqlite3.connect('teams.db')
cursor = sqliteConnection.cursor()
with st.form("form2", clear_on_submit=True):
    cursor.execute("SELECT DISTINCT org_name, org_loc FROM teamy")
    ans = cursor.fetchall()
    options = [" "]
    for x in ans:
        if x[0] and x[1]:
            options.append(x[0]+","+x[1])
    org = (st.selectbox('Select your company : ',(options)))
    password = text_field("Enter password : ", type = "password")
    submit = st.form_submit_button(label="Submit")
if(submit):
    name, loc = org.split(",")
    if(validate(name, loc, password)):
        teams = []
        cursor.execute("SELECT DISTINCT t_id FROM teamy WHERE org_name = (?) AND org_loc = (?)", (name, loc))
        ans = cursor.fetchall()
        dicti = dd(list)
        for x in ans:
            if x[0]:
                cursor.execute("SELECT COUNT(*) FROM teamy WHERE t_id = (?) AND org_name = (?)", (x[0], name))
                a = cursor.fetchall()
                dicti["Team ID"].append(x[0])
                dicti["Remaining Tasks"].append(a[0])
        st.table(dicti)
sqliteConnection.commit()
sqliteConnection.close()