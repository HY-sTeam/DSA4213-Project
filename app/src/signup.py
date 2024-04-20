import datetime
import random
import re
from io import BytesIO

import psycopg2
import src.login_helper as lg
import streamlit as st


# Initialize session state variables
if 'email' not in st.session_state:
    st.session_state.email = None
if 'name' not in st.session_state:
    st.session_state.name = None
if 'password' not in st.session_state:
    st.session_state.password = None

def signup(): # if uncomment this line, all below lines should be right-indented one lot

    conn =  lg.get_db_connection()
    cur = conn.cursor()
    with st.form(key='register'):
        st.write("Signup Here! ")
        email = st.text_input(label='Enter your email. ')
        st.session_state.email = email
        name = st.text_input(label='Enter your username. ')
        st.session_state.name = name
        password = st.text_input(label='Enter your password. ', type = 'password')
        st.session_state.password = password
        sign_up = st.form_submit_button('Submit')

        # st.write("Signup Here! ")
        # st.text_input(label='Enter your email. ', key='signup_email')
        # st.text_input(label='Enter your username. ', key='name')
        # st.text_input(label='Enter your password. ', type = 'password', key='signup_password')
        # sign_up = st.form_submit_button('Sign up')

        if sign_up:
            # Check if any required fields are empty
            if not st.session_state.email or not st.session_state.name or not st.session_state.password:
                st.error('Please fill in all fields.')
            else:
                # Check if the email already exists
                cur.execute("SELECT * FROM Users WHERE email = %s", (st.session_state.email,))
                if cur.fetchone():
                    st.error('User already exists. Please return to login page by clicking on "Submit" button.')
                    st.session_state.page = "login"  # Set page state to login
                    # st.rerun()

                    
                else:
                    # Check if the username already exists
                    cur.execute("SELECT * FROM Users WHERE name = %s", (st.session_state.name,))
                    if cur.fetchone():
                        st.error('Username is taken. Please register with another username.')

                    else:
                        try:
                            # Insert the new user into the database
                            cur.execute("INSERT INTO Users (email, name, pin) VALUES (%s, %s, %s)", 
                                        (st.session_state.email, st.session_state.name, st.session_state.password))
                            conn.commit()
                            st.success('User registered successfully. Please proceed by clicking on "Submit" button.')
                            st.session_state.page = "main"
                            # st.rerun()

                        except Exception as e:
                            conn.rollback()
                            st.error('An error occurred during signup.')

    # Close the cursor and connection
    cur.close()
    conn.close()


# if st.session_state.page == "signup":
#     signup()

# signup()