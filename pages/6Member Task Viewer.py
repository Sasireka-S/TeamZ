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
def validate(name, loc, password, n):
    sqliteConnection = sqlite3.connect('teams.db')
    cursor = sqliteConnection.cursor()
    name = name.lower()
    loc = loc.lower()
    cursor.execute('SELECT extra1 FROM teamy WHERE org_name = (?) AND org_loc = (?) AND mem_name= (?)', (name, loc, n))
    ans = cursor.fetchall()
    for x in ans:
        if(x[0] == password):
            return True
    return False
add_bg_from_local('images/bg.jpg')
t = '<p style = "font-size:60px; text-align:center; font-family:Georgia">TeamZ for Members</p>'
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
    n = text_field("Enter name : ").lower()
    password = text_field("Enter password : ", type = "password")
    submit = st.form_submit_button(label="Submit")
if(submit):
    name, loc = org.split(",")
    if(validate(name, loc, password, n)):
        t = '<p style = "font-size:20px; text-align:center; font-family:Georgia">Your Tasks and Dues</p>'
        st.markdown(t, unsafe_allow_html=True)
        cursor.execute("SELECT task_name, task_due FROM teamy WHERE mem_name = (?) and org_name = (?)", (n, name))
        ans = cursor.fetchall()
        dicti = dd(list)
        for x in ans:
            if x[0] and x[1]:
                dicti["Task"].append(x[0])
                dicti["Due"].append(x[1])
        df = pd.DataFrame(dicti)
        st.table(dicti)
    else:
        st.error("Invalid password")
    t = '<p style = "font-size:20px; text-align:center; font-family:Georgia">Mark the completed tasks</p>'
    st.markdown(t, unsafe_allow_html=True)
if(org != " "):
    name, loc = org.split(",")
    if(validate(name, loc, password, n)):
        num = 0
        cursor.execute("SELECT DISTINCT task_name FROM teamy WHERE org_name = (?) AND mem_name = (?)", (name, n))
        options = cursor.fetchall()
        names = []
        agree = []
        with st.form("form3"):
            for x in options:
                for i in x:
                    if(i):
                        agree.append(st.checkbox(i))
                        names.append(i)
                        num += 1
            submit = st.form_submit_button(label="Submit")
        if submit:
            for x in range(num):
                if(agree[x]):
                    st.text(names[x])
                    cursor.execute("DELETE FROM teamy WHERE task_name = (?) AND mem_name = (?)", (names[x], n))
                    cursor.execute("UPDATE teamy SET comp = comp+1 WHERE mem_name = (?) AND org_name = (?)", (n, name))
                    sqliteConnection.commit()
                f = 1
sqliteConnection.commit()
sqliteConnection.close()