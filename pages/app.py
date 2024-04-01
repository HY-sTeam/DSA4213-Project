import base64
import json
import os
from datetime import date, datetime, timedelta
from io import BytesIO

import boto3
import openai
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt

# Initialisation of Features
if 'topic' not in st.session_state:
    st.session_state.topic = ''
if 'source' not in st.session_state:
    st.session_state.source = 'Wikipedia'
if 'field' not in st.session_state: 
    st.session_state.field = None
if 'language' not in st.session_state:
    st.session_state.language = 'Auto (English)'
if 'writing_tone' not in st.session_state:
    st.session_state.writing_tone = None
if 'number_of_slides' not in st.session_state:
    st.session_state.number_of_slides = 8
if 'style' not in st.session_state:
    st.session_state.style = None
if 'start_date' not in st.session_state:
    st.session_state.start_date = None
if 'end_date' not in st.session_state:
    st.session_state.end_date = None

# set page layout
st.set_page_config(
    page_title = "slides-generator", 
    layout = "wide", 
    page_icon = "🚀", 
    menu_items = {
        # redirect client to the git repo app-doc
        'Get Help': "https://youtu.be/OhPyurx8-N0?list=RDOhPyurx8-N0", 
        # redirect client to the mailbox in charge
        'Report A Bug': "mailto:soowenqiao@gmail.com",
        # redirect client to the git repo README.md
        'About': "mailto:soowenqiao@gmail.com"
    }
)

path = os.path.dirname(__file__)
today = date.today()



st.title("Slides Generator")
st.subheader("Welcome to Powerpoint Generator! We're here to help you generate slides effectively by just one click. :)")
st.write("This is a 2324S2 DSA4213 project, by Team Rojak. ")
  
with st.form("my_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input('TOPIC', placeholder = 'What do you want to generate today ٩(˃̶͈̀௰˂̶͈́)و ? ')
        st.session_state.topic = topic
    
    with col2:
        source = st.selectbox('SOURCE', ['Wikipedia', 'arxiv.org'])
        st.session_state.source = source

    # Align topic, writing tone and number of slides horizontally
    col3, col4, col5 = st.columns([3, 3, 2])
    with col3: 
        field = ['General', 'Physics', 'Mathematics', 'Computer Science', 'Quantitative Biology', 'Quantitative Finance', 'Statistics', 'Electrical Engineering and Systems Science', 'Economics']
        selected_field = st.multiselect(label = 'Relevant Field(s)', options = field, 
                                        placeholder = 'You are encouraged to choose a maximum of 3 labels. ')
        st.session_state.selected_field = selected_field

        start_date = st.date_input('Start Date', date.today() - timedelta(days=30))
        st.session_state.start_date = start_date
    
    with col4: 
        writing_tone = st.selectbox('Writing Tone', ['Auto (Casual)', 'Formal'])
        st.session_state.writing_tone = writing_tone

        end_date = st.date_input('End Date', date.today())
        st.session_state.end_date = end_date

    
    with col5: 
        style = st.radio('Style', ['Minimalist', 'Colorful', 'Geometric', 'Professional'])
        st.session_state.style = style

  
    # Check if the start_date is after end_date and show a warning
    if st.session_state.start_date > st.session_state.end_date:
        st.warning('Start date must be before end date.')
        st.stop()

    # Every form must have a submit button. 
    submitted = st.form_submit_button("Generate presentation")
    st.session_state.submitted = submitted
    if st.session_state.submitted:
        if st.session_state.topic == "":
            # The form is submitted without a topic
            st.error('Please enter a topic to generate the presentation.')
        else:
            with st.spinner('Processing your request, please wait... ⏳'):
                try:
                    # Send user input to backend service
                    data = {
                        'user_query': st.session_state.topic, 
                        'search_engine': st.session_state.source, 
                        'field': st.session_state.selected_field, 
                        'language': st.session_state.language, 
                        'writing_tone': st.session_state.writing_tone, 
                        'number_of_slides': st.session_state.number_of_slides, 
                        'style': st.session_state.style, 
                        'start_date': st.session_state.start_date.isoformat(), 
                        'end_date': st.session_state.end_date.isoformat()
                    }
                    # pptx_file_path = generate_presentation(topic)
                    # Uncomment the line below to test out your request logic
                    # success = send_request_to_backend(topic)  # Replace with your actual request logic
                    #response = requests.post('http://127.0.0.1:5000/simulate', json=data)

                    # Uncomment this block code to check if work, once BE complete!
                    # response = requests.post('http://flask-app:5000/generate_slides', json=data)
                    # # if the response is executed successfully, allow users to download slides from BE
                    # if response.status_code == 200: 
                    #      slides_url = response.text
                    # else: 
                    #      st.error("Searching failed. Please try again. ")

                    success = True
                    # mimic situation
                    if success == True:
                        slides_url = 'https://indico.cern.ch/event/546003/attachments/1329103/1996541/MachineLearningSparkML.pptx'
                        st.markdown(f'[Download Presentation]({slides_url})', unsafe_allow_html=True)
                    else:
                        st.error("Searching failed. Please try again. ")


                    if success:
                        # The request was successful
                        st.success('Presentation generated!')
                        # Read the contents of the pptx file for download
                        # with open(pptx_file_path, "rb") as file:
                        #     btn = st.download_button(
                        #         label="Download Presentation",
                        #         data=file,
                        #         file_name="presentation.pptx",
                        #         mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        #         )
                    else:
                        # The request was made but failed
                        st.error('The request to the backend service failed. Please try again.')
                except Exception as e:
                    # An exception occurred while processing the request
                    st.error(f'An error occurred while processing the request: {e}')

# Add color for the form background
css = """
<style>
    [data-testid = "stForm"] {
    background: LightBlue;
    }
</style>
"""

st.write(css, unsafe_allow_html=True)

# Initialising client for AWS
s3 = boto3.client('s3',
                  aws_access_key_id='YOUR_ACCESS_KEY_ID',
                  aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
                  region_name='Singapore')

# Creating S3 bucket
history = s3.create_bucket(Bucket = 'history')

# Function to list ppt from S3 bucket
def list_presentations(history):
    presentations = []
    response = s3.list_objects(Bucket=history)
    history_list = response['Contents']
    if history_list:
        for obj in history_list:
            presentations.append(obj['Key'])
    return presentations

# Sidebar tab for history
selected_page = st.sidebar.selectbox("Menu", ["Homepage", "History"])

if selected_page == "Homepage":
    # Your existing homepage content goes here
    st.title("Homepage")
elif selected_page == "History":
    # Your presentation history content
    st.title("Presentation History")

    # List presentations from S3 bucket
    presentations = list_presentations(history)

    # Display presentation history
    if presentations:
        st.write("Recent Presentations:")
        for presentation in presentations:
            st.write(presentation)
            # Generate pre-signed URL for download
            presigned_url = s3.generate_presigned_url('get_object',
                                                      Params={'Bucket': history, 'Key': presentation},
                                                      ExpiresIn=3600)  # URL expires in 1 hour
            st.markdown(f'[Download {presentation}]({presigned_url})')
    else:
        st.write("No presentations found.")
