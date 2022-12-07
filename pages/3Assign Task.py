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

def validate(name, loc, password, id):
    sqliteConnection = sqlite3.connect('teams.db')
    cursor = sqliteConnection.cursor()
    name = name.lower()
    loc = loc.lower()
    cursor.execute('SELECT t_password FROM teamy WHERE org_name = (?) AND org_loc = (?) AND t_ID = (?)', (name, loc, id))
    ans = cursor.fetchall()
    for x in ans:
        if(x[0] == password):
            return True
    return False
def assign():
    sqliteConnection = sqlite3.connect('teams.db')
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT DISTINCT org_name, org_loc FROM teamy")
    ans = cursor.fetchall()
    options = [" "]
    for x in ans:
        if x[0] and x[1]:
            options.append(x[0]+","+x[1])
    with st.form("my_form2"):
        org = (st.selectbox('Select your company : ',(options)))
        t_id = text_field("Give team id : ")
        password = text_field("Enter your Password : ", type = "password")
        submit2 = st.form_submit_button(label="Submit")
    if(org != " "):
        name, loc = org.split(",")
        n = 0
        if(validate(name, loc, password, t_id)):
            f = 0 
            with st.form("my_form3", clear_on_submit=True):
                task = text_field("Enter task name : ")
                time = st.date_input("Enter the Deadline to complete : ")
                cursor.execute("SELECT DISTINCT mem_name FROM teamy WHERE org_name = (?) AND t_id = (?)", (name, t_id))
                options = cursor.fetchall()
                names = []
                agree = []
                for x in options:
                    for i in x:
                        if(i):
                            agree.append(st.checkbox(i))
                            names.append(i)
                            n += 1
                    f = 1
                submit3 = st.form_submit_button(label="Submit")
            if submit3:
                for x in range(n):
                    if(agree[x]):
                        cursor.execute("INSERT INTO teamy(mem_name, t_id, org_name,org_loc,task_name,task_due) values (?,?,?,?,?,?)", (names[x],t_id, name,loc,task,time))
                        sqliteConnection.commit()
                        cursor.execute("UPDATE teamy SET total = total+1 WHERE mem_name = (?) AND t_id = (?)", (names[x], t_id))
                        st.text("Successfully Assigned")
        else:
            st.error("Invalid credentials")
    sqliteConnection.close()  
add_bg_from_local('images/bg.jpg')
t = '<p style = "font-size:60px; text-align:center; font-family:Georgia">TeamZ for Team Leaders</p>'
st.markdown(t, unsafe_allow_html=True)
assign()