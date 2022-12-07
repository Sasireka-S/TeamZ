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

def register():
    with st.form("form2", clear_on_submit=True):
        sqliteConnection = sqlite3.connect('teams.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT DISTINCT org_name, org_loc FROM teamy")
        ans = cursor.fetchall()
        options = [" "]
        for x in ans:
            if x[0] and x[1]:
                options.append(x[0]+","+x[1])
        org = (st.selectbox('Select your company : ',(options)))
        t_id = text_field("Enter team id : ")
        mem_name = text_field("Enter your Name : ").lower()
        mem_mail = text_field("Enter your Mail ID : ")
        mem_phone = text_field("Enter your Phone No : ")
        password = text_field("Enter your Password : ", type = "password")
        submit2 = st.form_submit_button(label="Submit")  
    if submit2:
        name, loc= org.split(",")
        cursor.execute("INSERT INTO teamy (t_id, mem_name, mem_mail, mem_phone, extra1, org_name, org_loc, total, comp) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (t_id, mem_name, mem_mail, mem_phone, password, name, loc, 0, 0))
        st.success("Successfully registered")
    sqliteConnection.commit()
    sqliteConnection.close()

add_bg_from_local('images/bg.jpg')
t = '<p style = "font-size:60px; text-align:center; font-family:Georgia">TeamZ for Members</p>'
st.markdown(t, unsafe_allow_html=True)
register()