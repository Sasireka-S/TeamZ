import sqlite3
import streamlit as st
import base64
st.set_page_config(page_title='Home', page_icon='', layout="wide", initial_sidebar_state="expanded", menu_items=None)
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

add_bg_from_local('images/bg5.jpg')
t = '<p style = "color:violet; font-size:60px; text-align:center; font-family:Georgia">TeamZ</p>'
st.markdown(t, unsafe_allow_html=True)
t = '<p style = "color:white; font-size: 40px; text-align : center; font-family:Georgia">The best way to improve Workspace Productivity</p>'
st.markdown(t, unsafe_allow_html=True)
with st.expander('', expanded=True):
    st.markdown(f'''
    <ul style = "margin-left : 300px;">
      <li style="color:white;"><p style="font-size:25px; font-family:Georgia; color:LightBlue;">Assign tasks<p>
      </li>
      <li style="color:white;"><p style="font-size:25px; font-family:Georgia; color:LightBlue;">Track and Manage Workloads<p>
      </li>
      <li style="color:white;"><p style="font-size:25px; font-family:Georgia; color:LightBlue;">Find out the Best team for Rewards</p></li> 
      <li style="color:white;"><p style="font-size:25px; font-family:Georgia; color:LightBlue;">Vote for Creative and Social Works</p></li>
    </ul>
    ''', unsafe_allow_html=True)