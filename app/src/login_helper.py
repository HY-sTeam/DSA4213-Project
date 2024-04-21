import random
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import psycopg2
import streamlit as st


# Database connection function (fill in your database credentials)
def get_db_connection():
    """Connects to the database.

    Returns:
        A connection.
    """    
    conn = psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="postgres",
        port="5432",
    )
    return conn


# Function to check user credentials
def check_credentials(email: str, pin: str):
    """Check credentials of user for authentication

    Args:
        email (str): User email.
        pin (str): User password

    Returns:
        A boolean value for correct or wrong password, or None if the email does not exist.
    """    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE email = %s", (email,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result != None:
        return result[2] == pin  # check user input same as db input, True if pin matches, False otherwise
    else: 
        return None # Email does not exist in the database

    
def store_otp(email: str, otp: str) -> None:
    """Stores one-time-password into the temporary table in the database.

    Args:
        email (str): user email
        otp (str): one-time-password.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Temps (otp, email) VALUES (%s, %s)", (otp, email)
    )  # time_otp is default to be curr_time
    conn.commit()
    cur.close()
    conn.close()


def get_recent_record(email):
    """Fetches the most recent record from the Temps table.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM Temps WHERE email = %s ORDER BY time_otp DESC LIMIT 1", (email,)
    )
    record = cur.fetchone()  # fetch the most recent row
    cur.close()
    conn.close()
    return record if record else None


def send_email(receiver_email, otp):
    """Sends email containing an otp to users who have lost their password.

    Args:
        receiver_email (str): Recipient of user with a lost password.
        otp (str): The one-time-password.
    """    
    
    sender_email = "soowenqiao@gmail.com"
    app_password = "lzhmfvtprtrvacgw"

    # Create a multipart message
    subject = "Slides Generator App - Reset Password"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    body = f"""Dear user, 
    
Wish you have a nice day! Recently, a failed login attempt from our interface had come to our notice. 

If you did not perform any login action, please ignore this email. Otherwise, here's your verification code: 

ROJAK-{otp}

Please copy and paste the code into the app to proceed with resetting your password. 

You're advised not to share this code with others.

Warmest Regards,
DSA4213 Rojak Team
    """
    message.attach(MIMEText(body, "plain"))

    # Create secure connection with server and send email
    server = smtplib.SMTP("smtp.gmail.com", 587)  # Use the correct SMTP server and port
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()


def send_otp(user_email: str) -> bool:
    """Randomly generates a one-time-password and stores

    Args:
        user_email (str): user email.

    Returns:
        bool: Boolean value for success or failure.
    """    
    otp = str(random.randint(100000, 999999)) # Generate the OTP
    try: 
        send_email(user_email, otp)  # Send the OTP to the user's email
        store_otp(user_email, otp)   # Store the OTP in the database
        return True
    except:
        return False


def verify_otp(
    user_email, user_otp
): 
    """Verifies a user's OTP.
    """    
     # user_otp is user input, stored_otp is in database storage
    record = get_recent_record(user_email)
    curr_time = record[0]
    curr_otp = record[1]
    # user input otp same with stored otp and 10 mins validity period
    if (
        record
        and user_otp == curr_otp
        and (time.time() - time.mktime(curr_time.timetuple()) <= 600)
    ):
        # OTP is valid
        return True
    else:
        # OTP is invalid or expired
        return False


def update_password(user_email: str, new_password: str):
    """Updates a user's email account with a new password
    """    
    conn = get_db_connection()
    cur = conn.cursor()
    try: 
        cur.execute("UPDATE Users SET pin = %s WHERE email = %s", (new_password, user_email))
        conn.commit()
    finally:
        cur.close()
        conn.close()


# Function to load data from the database
def load_data(email: str) -> pd.DataFrame:
    """Loads data from the database given an email and returns the data.

    Args:
        email (str): User email

    Returns:
        pd.DataFrame: A dataframe consisting of all columns with the user email.
    """    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    cursor.execute("SELECT * FROM Slides WHERE email = %s", (email, ))
    data = cursor.fetchall()

    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data, columns=[desc[0] for desc in cursor.description])
    
    cursor.close()
    conn.close()
    return df