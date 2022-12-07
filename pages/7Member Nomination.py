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
add_bg_from_local("images/bg4.jpg")
with st.expander('', expanded=True):
    t = '<p style = "text-align: center; color:violet; font-family: Georgia; font-size: 30px;">Nominate yourself for your Creative or Social works</p>'    
    st.markdown(t, unsafe_allow_html=True)
    t = '<p style = "text-align: center; color:violet; font-family: Georgia; font-size: 30px;">You may get rewarded for your works !!!</p>'    
    st.markdown(t, unsafe_allow_html=True)
    sqliteConnection = sqlite3.connect('teams.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT DISTINCT org_name, org_loc FROM teamy")
    ans = cursor.fetchall()
    options = [" "]
    for x in ans:
        if x[0] and x[1]:
            options.append(x[0]+","+x[1])
    t = '<p style = "text-align: center; color:white; font-family: Georgia; font-size: 25px;">View Other Nominations</p>'    
    st.markdown(t, unsafe_allow_html=True)
    with st.form("my_form"):
        org = (st.selectbox('Select company : ',(options)))
        submit = st.form_submit_button(label="Submit")
    if submit:
        t = '<p style = "color: violet; text-align: center; font-family: Georgia; font-size: 25px;">Creativity Nominations</p>'
        st.markdown(t, unsafe_allow_html=True)
        cursor.execute("SELECT mem_creative FROM teamy WHERE c_id = (?)", (org,))
        ans = cursor.fetchall()
        for x in ans:
            t = '<p style = "text-align: center; color:white; font-family: Georgia; font-size: 20px;">{c}</p>'.format(c = x[0])  
            st.markdown(t, unsafe_allow_html=True)
        t = '<p style = "color: violet; text-align: center; font-family: Georgia; font-size: 25px;">Social Works Nominations</p>'
        st.markdown(t, unsafe_allow_html=True)
        cursor.execute("SELECT mem_social FROM teamy WHERE c_id = (?)", (org,))
        ans = cursor.fetchall()
        for x in ans:
            t = '<p style = "text-align: center; color:white; font-family: Georgia; font-size: 20px;">{c}</p>'.format(c = x[0])  
            st.markdown(t, unsafe_allow_html=True)
    with st.form("my_form5"):
        submit3 = st.form_submit_button(label="Nominate Yourself")
    if submit3:
        with st.form("my_form2"):
            org = (st.selectbox('Select company : ',(options)))
            name = text_field("Enter your Name : ")
            type = text_field("Is you work Social or Creative ? ")
            work = st.text_area("Enter your work details and Why you nominate ?")
            submit2 = st.form_submit_button(label="Submit")
        if submit2:
            if(type.lower() == "creative"):
                cursor.execute("INSERT INTO teamy (c_id, mem_creative,mem_name) VALUES (?, ?, ?)", (org, work, name))
                sqliteConnection.commit()
            else:
                cursor.execute("INSERT INTO teamy (c_id, mem_social, mem_name) VALUES (?, ?, ?)", (org, work, name))
                sqliteConnection.commit()
    sqliteConnection.commit()
    sqliteConnection.close()