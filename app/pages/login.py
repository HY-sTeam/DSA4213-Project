import datetime
import random
import re
from io import BytesIO

import psycopg2
# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.login_helper as lg
import streamlit as st

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'email' not in st.session_state:
    st.session_state.email = None
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

def login(): # if uncomment this line, all below lines should be right-indented one lot
    conn = lg.get_db_connection()
    cur = conn.cursor()

    with st.form(key='usrlogin'):
        st.write('Login here. ')
        email = st.text_input(label = 'Enter your email. ')
        st.session_state.email = email
        password = st.text_input(label='Enter your password. ', type = 'password')
        st.session_state.password = password
        login = st.form_submit_button('Log In')

        if login:
            credential_status = lg.check_credentials(st.session_state.email, st.session_state.password)
            st.session_state.credential_status = credential_status
            if st.session_state.credential_status is True:
                st.success('Logged in successfully.')
                st.session_state.page = "main"
                st.experimental_rerun()

                # main()
            elif st.session_state.credential_status is False:
                st.error('Wrong password. Try again.')
            else: 
                st.error('Email does not exist. Proceed to signup.')
                st.session_state.page = "signup" # Redirect to the signup page.
                st.experimental_rerun() 

    # Close the cursor and connection
    # cur.close()
    # conn.close()

    # def forgot_password(): # if uncomment this line, all lines from here and below should be left-indented first, then right-indented one lot
    # conn = lg.get_db_connection()
    # cur = conn.cursor()
    with st.expander('Forgot password? '):
        forgot_email = st.text_input("Please key in your email address here. ")
        st.session_state.email = forgot_email
        if st.session_state.email == "":
            st.write("Please enter your email! ")
        if st.button("Send OTP"):
            try: 
                lg.send_otp(st.session_state.email) # if otp had been sent
                # if lg.send_otp(st.session_state.email) is True:
                st.success("Password reset link has been sent.  Please use the generated OTP in 10 mins. ")
                otp_tbc = st.text_input("Enter OTP")
                st.session_state.otp_tbc = otp_tbc
                
                if lg.verify_otp(st.session_state.email, st.session_state.otp_tbc): # if verify_otp is true
                    new_password = st.text_input("New password", type='password')
                    st.session_state.new_password = new_password
                    confirm_password = st.text_input("Confirm new password", type='password')
                    st.session_state.confirm_password = confirm_password

                    if st.button("Reset password"): 
                        if st.session_state.confirm_password == st.session_state.new_password:
                            lg.update_password(st.session_state.email, st.session_state.new_password)
                            st.success("Password reset successfully. ")
                            st.session_state.page = "login" # Redirect to the signup page.
                            st.experimental_rerun()

                        else:
                            st.error("Passwords do not match. Please re-enter! ")
                else:
                    st.error("Invalid OTP or OTP has expired. Please try again. ")
            except:
                st.error("Failed to send OTP. Please try again. ")

    # Close the cursor and connection
    cur.close()
    conn.close()

login()
