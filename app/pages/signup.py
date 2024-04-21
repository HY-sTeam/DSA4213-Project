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

def signup():
    """Execute streamlit signup page.
    """

    conn =  lg.get_db_connection()
    cur = conn.cursor()
    with st.form(key='register'):
        st.write("Signup Here! ")
        st.text_input(label='Enter your email. ', key='signup_email')
        st.text_input(label='Enter your username. ', key='name')
        st.text_input(label='Enter your password. ', type = 'password', key='signup_password')
        sign_up = st.form_submit_button('Sign up')
        if sign_up:
            # Check if the username already exists
            cur.execute("SELECT * FROM Users WHERE name = %s", (st.session_state.name,))
            if cur.fetchone():
                st.error('Username already exists.')
                st.session_state.page = "login"
                # st.experimental_rerun()
            else:
                try: 
                    cur.execute("INSERT INTO Users (email, name, pin) VALUES (%s, %s, %s)", (st.session_state.signup_email, st.session_state.name, st.session_state.signup_password))
                    conn.commit()
                    st.success('User registered successfully. ') # page-redirecting to main page
                    st.session_state.page = "main"
                    # st.experimental_rerun()

                except psycopg2.errors.UniqueViolation as e:
                    conn.rollback()
                    st.error('User already exists.')
                    st.session_state.page = "login" # Redirect to login page

                    # st.experimental_rerun()

                except psycopg2.Error as e:
                    conn.rollback()  # Rollback the transaction
                    st.error('An error occurred. ')

    # Close the cursor and connection
    cur.close()
    conn.close()


if st.session_state.page == "signup":
    signup()