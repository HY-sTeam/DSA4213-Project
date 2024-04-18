import base64
import os
import random
import re
from base64 import b64encode
from datetime import date, datetime, timedelta
from io import BytesIO

import pandas as pd
import psycopg2
import psycopg2.extras
import src.login_helper as lg
import streamlit as st
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Cm, Inches, Pt
from src.llm.lang import (clear_all_collections, clear_all_documents,
                          clear_all_pending_uploads, create_collection,
                          ingest_files_in_dir, query, start_client)
from src.llm.pptgen import (decide_ppt_colour, decide_slide_titles,
                            gen_key_words, generate_ppt)
from src.websearch.search import (clear_dir, download_papers, download_wikis,
                                  search_arxiv, search_wiki)

# Initialize session state variables
if 'user_input' not in st.session_state:
    st.session_state.user_input = None
if 'source' not in st.session_state:
    st.session_state.source = None
if 'wants_arxiv' not in st.session_state:
    st.session_state.wants_arxiv = None
if 'wants_wiki' not in st.session_state:
    st.session_state.wants_wiki = None
if 'submitted' not in st.session_state:
    st.session_state.submitted = None

# Initialize session state variables # for login() and signup(), can consider to uncomment when doing multipage in one py or multi-py
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'email' not in st.session_state:
    st.session_state.email = None
if 'name' not in st.session_state:
    st.session_state.name = None
if 'password' not in st.session_state:
    st.session_state.password = None
if 'credential_status' not in st.session_state:
    st.session_state.credential_status = None
if 'otp_tbc' not in st.session_state:
    st.session_state.otp_tbc = None
if 'new_password' not in st.session_state:
    st.session_state.new_password = None
if 'confirm_password' not in st.session_state:
    st.session_state.confirm_password = None
if 'bytes' not in st.session_state:
    st.session_state.bytes = None

# uncomment if u feel unnecessary
# Function to connect to the database # ok I'll put this here, but it's incl in login_helper.py
def get_connection():
    return psycopg2.connect(
        host="postgre",
        port="5432",
        dbname="mydatabase",
        user="myuser",
        password="mypassword"
    )

# Function to load data from the database
def load_data(email):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cursor.execute("SELECT * FROM Slides WHERE email = %s", (email, ))
    data = cursor.fetchall()
    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
    
    cursor.close()
    conn.close()
    return df

# Function to download the prs generated
def get_bytes(
    ppt, file_name="presentation.pptx"
):
    ppt_bytes = BytesIO()
    ppt.save(ppt_bytes)
    # ppt_bytes.seek(0)
    # b64 = b64encode(ppt_bytes.read()).decode()
    # href = f'<a href="data:application/vnd.openxmlformats-officedocument.presentationml.presentation;base64,{b64}" download="{file_name}">{file_label}</a>'
    return ppt_bytes


# Set page layout
st.set_page_config(page_title="Slides Generator", page_icon="🚀", 
                    menu_items = {
                        # redirect client to the git repo app-doc
                        'Get Help': "https://youtu.be/fLexgOxsZu0", 
                        # redirect client to the mailbox in charge
                        'Report A Bug': "mailto:soowenqiao@gmail.com",
                        # redirect client to the git repo README.md
                        'About': "https://github.com/HY-sTeam/DSA4213-Project/tree/main"})

def signup():
    conn =  lg.get_db_connection()
    cur = conn.cursor()
    with st.expander(key='register', expanded=False):
        st.write("Signup Here! ")
        email = st.text_input(label='Enter your email. ', key='signup_email')
        st.session_state.email = email
        name = st.text_input(label='Enter your username. ', key='signup_username')
        st.session_state.name = name
        password = st.text_input(label='Enter your password. ', type = 'password', key='password')
        st.session_state.password = password
        sign_up = st.button('Sign up')
        if sign_up:
            # Check if the username already exists
            cur.execute("SELECT * FROM Users WHERE name = %s", (st.session_state.name,))
            if cur.fetchone():
                st.error('Username already exists.')
                st.session_state.page = "login"
            else:
                try: 
                    cur.execute("INSERT INTO Users (email, name, pin) VALUES (%s, %s, %s)", (st.session_state.email, st.session_state.name, st.session_state.password))
                    conn.commit()
                    st.success('User registered successfully. ') # redirect to main page
                except psycopg2.errors.UniqueViolation as e:
                    conn.rollback()
                    st.error('User already exists. ')
                    st.session_state.page = "login" # Redirect to login page
                except psycopg2.Error as e:
                    conn.rollback()  # Rollback the transaction
                    st.error('An error occurred. ')
    # Close the cursor and connection
    cur.close()
    conn.close()

def login(): # if uncomment this line, all below lines should be right-indented one lot
    conn = lg.get_db_connection()
    cur = conn.cursor()

    with st.form(key='usrlogin'):
        st.write('Login here. ')
        email = st.text_input(label = 'Enter your email. ', key='login_email')
        st.session_state.email = email
        password = st.text_input(label='Enter your password. ', type = 'password', key='login_password')
        st.session_state.password = password
        login = st.form_submit_button('Log In')
        if login:
            credential_status = lg.check_credentials(st.session_state.email, st.session_state.password)
            st.session_state.credential_status = credential_status
            if st.session_state.credential_status is True:
                st.success('Logged in successfully.')
                # main()
            elif st.session_state.credential_status is False:
                st.error('Wrong password. Try again.')
            else: 
                st.error('Email does not exist. Proceed to signup.')
                st.session_state.page = "signup" # Redirect to the signup page. 
    # Close the cursor and connection
    # cur.close()
    # conn.close()

    # def forgot_password(): # if uncomment this line, all lines from here and below should be left-indented first, then right-indented one lot
    # conn = lg.get_db_connection()
    # cur = conn.cursor()
    with st.expander('Forgot password? '):
        forgot_email = st.text_input("Please key in your email address here. ", key='forgot_email')
        st.session_state.email = forgot_email
        if st.session_state.email == "":
            st.write("Please enter your email! ")
        if st.button("Send OTP"):
            try: 
                lg.send_otp(st.session_state.email) # if otp had been sent
                # if lg.send_otp(st.session_state.email) is True:
                st.success("Password reset link has been sent.  Please use the generated OTP in 10 mins. ")
                otp_tbc = st.text_input("Enter OTP", key='otp')
                st.session_state.otp_tbc = otp_tbc
                if lg.verify_otp(st.session_state.email, st.session_state.otp_tbc): # if verify_otp is true
                    new_password = st.text_input("New password", type='password', key='otppassword')
                    st.session_state.new_password = new_password
                    confirm_password = st.text_input("Confirm new password", type='password')
                    st.session_state.confirm_password = confirm_password
                    if st.button("Reset password"): 
                        if st.session_state.confirm_password == st.session_state.new_password:
                            lg.update_password(st.session_state.email, st.session_state.new_password)
                            st.success("Password reset successfully. ")
                        else:
                            st.error("Passwords do not match. Please re-enter! ")
                else:
                    st.error("Invalid OTP or OTP has expired. Please try again. ")
            except:
                st.error("Failed to send OTP. Please try again. ")

def main():
    st.title("Slides Generator") # the XXX need to link to session_state shortly
    st.subheader("Welcome XXX to Powerpoint Generator! We're here to help you generate slides effectively by just one click. :)")
    st.write("This is a 2324S2 DSA4213 project, by Team Rojak. ")

    with st.expander(label="generator", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            user_input = st.text_input('TOPIC', placeholder = 'What do you want to generate today ٩(˃̶͈̀௰˂̶͈́)و ? ', max_chars=150, key='generation')
            st.session_state.user_input = user_input
        with col2:
            source = st.selectbox('SOURCE', ['Wikipedia', 'arxiv.org', 'both'])
            st.session_state.source = source
            if st.session_state.source == 'Wikipedia':
                st.session_state.wants_arxiv = False
                st.session_state.wants_wiki = True
            elif st.session_state.source == 'arxiv.org': 
                st.session_state.wants_arxiv = True
                st.session_state.wants_wiki = False
            else:
                st.session_state.wants_wiki = st.session_state.wants_arxiv = True
                
        submitted = st.button("Generate presentation") # if the st.form is changed, change here to st.button("Generate presentation")
        st.session_state.submitted = submitted
    if st.session_state.submitted:
        if st.session_state.user_input == "":
            # The form is submitted without a topic
            st.error('Please enter a topic to generate the presentation. ')
        else: 
            
            with st.status('Generating PPT...', expanded=True) as status:
                #conn =  lg.get_db_connection()
                #cur = conn.cursor()
                # 1st Step: conducting web search
                clear_dir()
                st.write("Starting up...")
                user_request = "I want to create a presentation about " + st.session_state.user_input
                client = start_client()
                clear_all_collections(client)
                clear_all_documents(client)
                clear_all_pending_uploads(client)

                st.write("Scouring the web...")
                collection_id = create_collection(client)
                output = gen_key_words(client, user_request)
                if st.session_state.wants_arxiv:
                    papers = search_arxiv(output)
                    download_papers(papers)
                if st.session_state.wants_wiki:
                    wikis = search_wiki(output)
                    download_wikis(wikis)
                
                # 2nd Step: ingesting information
                st.write("Ingesting information...")
                ingest_files_in_dir(client, collection_id)

                # 3rd Step: implementing design layout and preferences ## if ath like colour, font, can be parsed here and added to above using with argument
                st.write("Thinking about design...")
                colour_dict = decide_ppt_colour(client, st.session_state.user_input)
                files = [file.split("/")[-1] for file in os.listdir("./src/websearch/temp_results") if file.endswith(".txt") or file.endswith(".pdf")]
                list_of_slide_titles = decide_slide_titles(client, st.session_state.user_input, files)

                # 4th Step: Generating PPT
                chat_session_id = client.create_chat_session()
                st.write("Generating PPT...")
                prs = generate_ppt(client, chat_session_id, list_of_slide_titles, colour_dict)
                st.session_state.bytes = get_bytes(prs)
                st.session_state.title = list_of_slide_titles[0]
                st.download_button(label="Download File!", data=st.session_state.bytes, file_name="Presentation.pptx")
                status.update(label="Done!", state="complete", expanded=True)
                # cur.execute("INSERT INTO Slides (title, bytes, email) VALUES (%s, %s, %s)", (st.session_state.title, st.session_state.bytes, st.session_state.email))
                # conn.commit()
                # cur.close()
                # conn.close()


def history():
    st.title("Session History Records")
    conn =  lg.get_db_connection()
    cur = conn.cursor()
    data = load_data(st.session_state.email)
    st.dataframe(data)    
    cur.close()
    conn.close()


# Main Execution
if 'page' not in st.session_state:
    st.session_state.page = "login"
    # login()

st.sidebar.title("Sidebar Title")
page_names_to_fns = {'Generate Slides': main, 'Past History': history, 
                     'Login': login, 'Signup': signup}
selected_page = st.sidebar.selectbox("How about today? ", page_names_to_fns.keys())
page_names_to_fns[selected_page]()

# Page Routing
if st.session_state.page == "login": # ideally streamlit shd be initiated to this page
    login()

# elif st.session_state.page == "signup":
#     signup()
# elif st.session_state.page == "main":
#     main()
# elif st.session_state.page == "history":
#     history()

# # Page Routing
# if st.session_state.page == "main":
#     main()