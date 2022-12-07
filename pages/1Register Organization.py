import streamlit as st
import base64
import sqlite3
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
t = '<p style = "font-size:60px; text-align:center; font-family:Georgia">TeamZ for Organizations</p>'
st.markdown(t, unsafe_allow_html=True)
comp = "Register"
if(comp == "Register"):
    sqliteConnection = sqlite3.connect('teams.db')
    cursor = sqliteConnection.cursor()
    with st.form("form2", clear_on_submit=True):
        name = text_field("Enter the Organization name : ").lower()
        loc = text_field("Enter the Organization location : ").lower()
        password = text_field("Enter your Password : ", type = "password")
        submit = st.form_submit_button(label="Submit")  
    if submit:
        cursor.execute('SELECT org_name, org_loc FROM teamy')
        ans = cursor.fetchall()
        flag = 0
        namel, locl = name.lower(), loc.lower()
        for x in ans:
            if(x[0] == namel and x[1] == locl):
                st.error("Some company in your location is present in our database with same name...")
                st.error("Please try with some suffixes")
                flag = 1
                break 
        if(flag == 0):
            cursor.execute("INSERT INTO teamy(org_name, org_loc, o_password) values(?, ?, ?)", (name, loc, password))
            st.success("Successfully registered!!!")
sqliteConnection.commit()
sqliteConnection.close()