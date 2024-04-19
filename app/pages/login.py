import datetime
import random
import re
from io import BytesIO

import psycopg2
import src.login_helper as lg
import streamlit as st

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'credential_status' not in st.session_state: # comment or uncomment this both line will throw AttributeError
    st.session_state.credential_status = None
if 'otp_tbc' not in st.session_state:
    st.session_state.otp_tbc = None
if 'new_password' not in st.session_state:
    st.session_state.new_password = None
if 'confirm_password' not in st.session_state:
    st.session_state.confirm_password = None
if 'login_button' not in st.session_state:
    st.session_state.login_button = None

# Function to check user credentials
def check_credentials():
    if st.session_state.login_email == '' or st.session_state.login_password == '':
        st.session_state.no_mail_no_pin = False
        return st.session_state.no_mail_no_pin
    else: 
        conn = lg.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users WHERE email = %s", (st.session_state.login_email,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result:
            # check user input same as db input, True if pin matches, False otherwise, store in credential_status
            st.session_state.credential_status = (result[2] == st.session_state.login_password)  
            return st.session_state.credential_status
        else: 
            return st.session_state.credential_status # Email does not exist in the database

def login(): # if uncomment this line, all below lines should be right-indented one lot
    conn = lg.get_db_connection()
    cur = conn.cursor()
    with st.form(key='usrlogin'):
        st.write('Login here. ')
        st.text_input(label = 'Enter your email. ', key='login_email')
        st.text_input(label='Enter your password. ', type = 'password', key='login_password')
        # st.session_state.login_email = login_email
        # login_password = st.text_input(label='Enter your password. ', type = 'password')
        # st.session_state.login_password = login_password
        login_button = st.form_submit_button('Log In', on_click=check_credentials)
        try:
            if st.session_state.credential_status is True: 
                st.success('Logged in successfully. ')
                # yeong hui, ur work can be appended here, the below juz a page-redirecting demo
                with st.spinner("Redirecting you to main page... "):
                    try:
                        st.session_state.page = "main"
                    except Exception as e:
                        st.error(f"Sorry. There's an {e}. ")
            elif st.session_state.credential_status is False: # not login_button, login_button is False
                st.error("User password doesn't match. ")
            elif st.session_state.no_mail_no_pin is False:
                st.error("Please enter your email and password at the same time! ")
            else:
                st.error("Email doesn't exist in the database. Welcome, my ever-first user. ")
                # yeong hui, ur work can be appended here, the below juz a page-redirecting demo
                with st.spinner("Redirecting you to signup page... "):
                    try:
                        st.session_state.page = "signup"
                    except Exception as e:
                        st.error(f"Sorry. There's an {e}. ")
        except:
            st.error('You are already logged in! ')

    # Close the cursor and connection
    # cur.close()
    # conn.close()

    # def forgot_password(): # if uncomment this line, all lines from here and below should be left-indented first, then right-indented one lot
    # conn = lg.get_db_connection()
    # cur = conn.cursor()

    # with st.expander('Forgot password? '):
    #     forgot_email = st.text_input("Please key in your email address here. ")
    #     if not forgot_email:
    #         st.write("Please enter your email! ")
    #     if st.button("Send OTP"):
    #         try: 
    #             lg.send_otp(st.session_state.email) # if otp had been sent
    #             # if lg.send_otp(st.session_state.email) is True:
    #             st.success("Password reset link has been sent.  Please use the generated OTP in 10 mins. ")
    #             otp_tbc = st.text_input("Enter OTP")
    #             st.session_state.otp_tbc = otp_tbc
                
    #             if lg.verify_otp(st.session_state.email, st.session_state.otp_tbc): # if verify_otp is true
    #                 new_password = st.text_input("New password", type='password')
    #                 st.session_state.new_password = new_password
    #                 confirm_password = st.text_input("Confirm new password", type='password')
    #                 st.session_state.confirm_password = confirm_password

    #                 if st.button("Reset password"): 
    #                     if st.session_state.confirm_password == st.session_state.new_password:
    #                         lg.update_password(st.session_state.email, st.session_state.new_password)
    #                         st.success("Password reset successfully. ")
    #                         st.session_state.page = "login" # Redirect to the signup page.
    #                         #st.experimental_rerun()

    #                     else:
    #                         st.error("Passwords do not match. Please re-enter! ")
    #             else:
    #                 st.error("Invalid OTP or OTP has expired. Please try again. ")
    #         except:
    #             st.error("Failed to send OTP. Please try again. ")

    # Close the cursor and connection
    cur.close()
    conn.close()

login()

# Page Routing
if st.session_state.page == "login": # ideally streamlit shd be initiated to this page
    login()