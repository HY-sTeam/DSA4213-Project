import datetime
import random
import re
from io import BytesIO

import login_helper as lg
import psycopg2
import streamlit as st


def signup():
    conn = lg.get_db_connection()
    cur = conn.cursor()
    with st.form(key="register"):
        st.write("Signup Here! ")
        email = st.text_input(label="Enter your email. ")
        name = st.text_input(label="Enter your username. ")
        password = st.text_input(label="Enter your password. ", type="password")
        sign_up = st.form_submit_button("Sign up")
        if sign_up:
            # Check if the username already exists
            cur.execute("SELECT * FROM Users WHERE name = %s", (name,))
            if cur.fetchone():
                st.error("Username already exists.")
                st.session_state.page = "Login"
            else:
                try:
                    cur.execute(
                        "INSERT INTO Users (email, name, pin) VALUES (%s, %s, %s)",
                        (email, name, password),
                    )
                    conn.commit()
                    st.success(
                        "User registered successfully. "
                    )  # redirect to main page
                except psycopg2.errors.UniqueViolation as e:
                    conn.rollback()
                    st.error("User already exists.")
                    st.session_state.page = "Login"  # Redirect to login page
                except psycopg2.Error as e:
                    conn.rollback()  # Rollback the transaction
                    st.error("An error occurred.")
    # Close the cursor and connection
    cur.close()
    conn.close()


# signup()


def login():
    conn = lg.get_db_connection()
    cur = conn.cursor()
    with st.form(key="usrlogin"):
        st.write("Login here. ")
        email = st.text_input(label="Enter your email. ")
        password = st.text_input(label="Enter your password. ", type="password")
        login = st.form_submit_button("Log In")
        if login:
            credential_status = lg.check_credentials(email, password)
            if credential_status is True:
                st.success("Logged in successfully.")
                # main()
            elif credential_status is False:
                st.error("Wrong password. Try again.")
            else:
                st.error("Email does not exist. Proceed to signup.")
                st.session_state.page = "Sign Up"  # Redirect to the signup page.
    # Close the cursor and connection
    cur.close()
    conn.close()


def forgot_password():
    conn = lg.get_db_connection()
    cur = conn.cursor()
    with st.expander("Forgot password? "):
        email = st.text_input("Please key in your email address here. ")
        if email is None:
            st.write("Please enter your email! ")
        else:
            submit_otp = st.button("Send OTP")
            if submit_otp:
                try:
                    otp_sent = lg.send_otp(email)
                    if otp_sent:
                        st.session_state["email_for_otp"] = email
                        st.success(
                            "Password reset link has been sent.  Please use the generated OTP in 10 mins. "
                        )
                        if "email_for_otp" in st.session_state:
                            with st.expander("Enter OTP and new password"):
                                otp = st.text_input("OTP")
                                new_password = st.text_input(
                                    "New password", type="password"
                                )
                                confirm_password = st.text_input(
                                    "Confirm new password", type="password"
                                )
                                reset = st.button("Reset password")
                                if reset:
                                    try:
                                        if new_password != confirm_password:
                                            st.error("Passwords do not match. ")
                                        elif lg.verify_otp(
                                            st.session_state.email_for_otp, otp
                                        ):
                                            lg.update_password(
                                                st.session_state.email_for_otp,
                                                new_password,
                                                otp,
                                            )
                                            st.success("Password reset successfully. ")
                                        else:
                                            st.error("Invalid OTP or OTP has expired. ")
                                    except Exception as e:
                                        st.error(f"Password reset failed: {e}")

                    else:
                        st.error("Failed to send OTP. Please try again. ")
                except Exception as e:
                    st.error(f"Operation failed: {e}")

    # if 'email_for_otp' in st.session_state:
    #     with st.expander("Enter OTP and new password"):
    #         otp = st.text_input("OTP")
    #         new_password = st.text_input("New password", type='password')
    #         confirm_password = st.text_input("Confirm new password", type='password')
    #         reset = st.button("Reset password")
    #         if reset:
    #             try:
    #                 if new_password != confirm_password:
    #                     st.error("Passwords do not match. ")
    #                 elif lg.verify_otp(st.session_state.email_for_otp, otp):
    #                     lg.update_password(st.session_state.email_for_otp, new_password, otp)
    #                     st.success("Password reset successfully. ")
    #                 else:
    #                     st.error("Invalid OTP or OTP has expired. ")
    #             except Exception as e:
    #                 st.error(f"Password reset failed: {e}")

    # Close the cursor and connection
    cur.close()
    conn.close()


login()
forgot_password()
# Main Execution
if "page" not in st.session_state:
    st.session_state.page = "Login"
    login()


# Page Routing
if st.session_state.page == "Login":
    login()
if st.session_state.page == "Sign Up":
    signup()
