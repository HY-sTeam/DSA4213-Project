import datetime
import random
import re
from io import BytesIO

import psycopg2
import src.login_helper as lg
import streamlit as st

# # Initialize session state variables
# if 'page' not in st.session_state:
#     st.session_state.page = "login"
# if 'credential_status' not in st.session_state: # comment or uncomment this both line will throw AttributeError
#     st.session_state.credential_status = None
# if 'otp_tbc' not in st.session_state:
#     st.session_state.otp_tbc = None
# if 'new_password' not in st.session_state:
#     st.session_state.new_password = None
# if 'confirm_password' not in st.session_state:
#     st.session_state.confirm_password = None
# if 'login_button' not in st.session_state:
#     st.session_state.login_button = None

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

# # Function to check user credentials
# def check_credentials():
#     if st.session_state.login_email == '' or st.session_state.login_password == '':
#         st.session_state.no_mail_no_pin = False
#         return st.session_state.no_mail_no_pin
#     else: 
#         conn = lg.get_db_connection()
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM Users WHERE email = %s", (st.session_state.login_email,))
#         result = cur.fetchone()
#         cur.close()
#         conn.close()
#         if result:
#             # check user input same as db input, True if pin matches, False otherwise, store in credential_status
#             st.session_state.credential_status = (result[2] == st.session_state.login_password)  
#             return st.session_state.credential_status
#         else: 
#             return st.session_state.credential_status # Email does not exist in the database

def login():
    conn = lg.get_db_connection()
    cur = conn.cursor()


    if not (st.session_state.email and st.session_state.credential_status):
        with st.form(key='usrlogin'):
            st.write('Login here.')
            email = st.text_input(label='Enter your email.')
            st.session_state.email = email
            password = st.text_input(label='Enter your password.', type='password')
            st.session_state.password = password
            login = st.form_submit_button('Log In')

            if login:
                credential_status = lg.check_credentials(st.session_state.email, st.session_state.password)
                if credential_status is True:
                    st.success('Logged in successfully.')
                    st.session_state.page = "main"
                elif credential_status is False:
                    st.error('Wrong password. Try again.')
                    st.session_state.page = "login"

                # Edited this line to fix routing problem
                else:
                    st.error('Email does not exist. Proceed to signup.')
                    st.session_state.page = "signup"
    else:
        st.success('You are already logged in! Proceeding to the main page...')
        st.session_state.page = "main"

    cur.close()
    conn.close()

    if st.session_state.page == "login":  # Only show forgot password if user is on login page
        with st.expander('Forgot password?'):
            forgot_email = st.text_input("Please key in your email address here.")
            if not forgot_email:
                st.write("Please enter your email!")
            if st.button("Send OTP"):
                try:
                    lg.send_otp(st.session_state.email)
                    st.success("Password reset link has been sent. Please use the generated OTP in 10 mins.")
                    otp_tbc = st.text_input("Enter OTP")
                    st.session_state.otp_tbc = otp_tbc

                    if lg.verify_otp(st.session_state.email, st.session_state.otp_tbc):
                        new_password = st.text_input("New password", type='password')
                        st.session_state.new_password = new_password
                        confirm_password = st.text_input("Confirm new password", type='password')
                        st.session_state.confirm_password = confirm_password


                        if st.button("Reset password"):
                            if st.session_state.confirm_password == st.session_state.new_password:
                                lg.update_password(st.session_state.email, st.session_state.new_password)
                                st.success("Password reset successfully.")
                                st.session_state.page = "login"
                            else:
                                st.error("Passwords do not match. Please re-enter!")
                    else:
                        st.error("Invalid OTP or OTP has expired. Please try again.")
                except:
                    st.error("Failed to send OTP. Please try again.")

