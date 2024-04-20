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
from src.login import login
from src.signup import signup
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

# Set page layout
st.set_page_config(page_title="Slides Generator", page_icon="🚀", 
                    menu_items = {
                        # redirect client to the git repo app-doc
                        'Get Help': "https://youtu.be/fLexgOxsZu0", 
                        # redirect client to the mailbox in charge
                        'Report A Bug': "mailto:soowenqiao@gmail.com",
                        # redirect client to the git repo README.md
                        'About': "https://github.com/HY-sTeam/DSA4213-Project/tree/main"})

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
if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

if 'page' not in st.session_state:
    st.session_state.page = "login"
    # login()
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




# Function to load data from the database
def load_data(email):
    conn = lg.get_db_connection()
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
    ppt
):
    ppt_bytes = BytesIO()
    ppt.save(ppt_bytes)
    return ppt_bytes


def main():
    st.title("Slides Generator")
    st.subheader(f"Welcome, {st.session_state.name}, to the Powerpoint Generator!")
    st.subheader("We're here to help you generate slides with just one click :)")
    st.write("This is a AY23/24 Sem2 DSA4213 project, by Team Rojak.")
    with st.expander(label="Generator", expanded=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            user_input = st.text_input('TOPIC', placeholder = 'What do you want to generate today ٩(˃̶͈̀௰˂̶͈́)و ? ', max_chars=100, key='generation')
            st.session_state.user_input = user_input
        with col2:
            source = st.selectbox('SOURCE', ['Wikipedia', 'arxiv.org', 'Both'])
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
                completion = 0
                bar = st.progress(completion, text="Starting up...")
                conn =  lg.get_db_connection()
                cur = conn.cursor()
                # 1st Step: conducting web search
                clear_dir()
                
                user_request = "I want to create a presentation about " + st.session_state.user_input
                client = start_client()
                clear_all_collections(client)
                clear_all_documents(client)
                clear_all_pending_uploads(client)

                completion += 0.1
                bar.progress(completion, text="Scouring the web...")

                collection_id = create_collection(client)
                output = gen_key_words(client, user_request)

                completion += 0.1
                bar.progress(completion, text="Scouring the web...")

                if st.session_state.wants_arxiv:
                    papers = search_arxiv(output)
                    download_papers(papers)
                completion += 0.15
                bar.progress(completion, text="Scouring the web...")
                if st.session_state.wants_wiki:
                    wikis = search_wiki(output)
                    download_wikis(wikis)
                completion += 0.15
                bar.progress(completion, text="Scouring the web...")
                
                # 2nd Step: ingesting information
                ingest_files_in_dir(client, collection_id)
                completion += 0.1
                bar.progress(completion, text="Thinking about design...")

                # 3rd Step: implementing design layout and preferences ## if ath like colour, font, can be parsed here and added to above using with argument

                colour_dict = decide_ppt_colour(client, st.session_state.user_input)
                files = [file.split("/")[-1] for file in os.listdir("./src/websearch/temp_results") if file.endswith(".txt") or file.endswith(".pdf")]
                list_of_slide_titles = decide_slide_titles(client, st.session_state.user_input, files)
                completion += 0.1
                bar.progress(completion, text="Ingesting information...")

                # 4th Step: Generating PPT
                chat_session_id = client.create_chat_session()
                bar.progress(completion, text="Generating PPT...")
                prs = generate_ppt(client, chat_session_id, list_of_slide_titles, colour_dict, bar, completion)
                st.session_state.bytes = get_bytes(prs)
                st.session_state.title = list_of_slide_titles[0]
                
                completion += 0.25 # incrememnts a total of 0.25 in ppt generation
                bar.progress(completion, text="Updating history...")

                if st.session_state.email:
                    cur.execute("INSERT INTO Slides (title, bytes, email) VALUES (%s, %s, %s)", (st.session_state.title, st.session_state.bytes.read(), st.session_state.email))
                    conn.commit()
                    cur.close()
                    conn.close()

                # 5th Step: After generating the presentation, update the session history
                bar.progress(1.0, text="Completed!")
                st.session_state.history_updated = True
                st.download_button(label="Download File!", data=st.session_state.bytes, file_name=f"{list_of_slide_titles[0]}.pptx")
                status.update(label="Done!", state="complete", expanded=True)

    # Expander for viewing past presentations
    with st.expander(label="View Past Presentations", expanded=True):
        history()

def history():
    st.title("Session History Records")
    conn = lg.get_db_connection()
    cur = conn.cursor()
    data = load_data(st.session_state.email)
    
    if not data.empty:

        # Add download buttons for each presentation entry
        for index, row in data.iterrows():
            bytes_data = row['bytes']
            title = row['title']
            file_name = f"{title}.pptx"

            # Convert bytes data to PowerPoint presentation
            ppt_bytes = BytesIO(bytes_data)
            ppt_bytes.seek(0)

            # Display a download button for each presentation
            download_button_label = f"Download {file_name}"
            st.download_button(label=download_button_label, data=ppt_bytes, file_name=file_name)

    else:
        st.write("No past presentations found.")

    cur.close()
    conn.close()





if st.session_state.is_logged_in:
    st.session_state.page = "main"
    


# Page Routing
if st.session_state.page == "login":
    login()
    if st.button('Signup'):
            st.session_state.page = 'signup'
            st.rerun()

elif st.session_state.page == "signup":
    signup()

elif st.session_state.page == "main":
    main()
    if st.button('Logout'):
        st.session_state.is_logged_in = False
        st.session_state.email = st.session_state.name = st.session_state.password = None
        st.session_state.page = 'login'
        st.rerun()