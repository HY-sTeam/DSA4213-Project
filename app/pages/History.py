import boto3
import base64
import json
import os
from datetime import date, datetime, timedelta
from io import BytesIO

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt

st.title("History")
st.subheader("Your past presentations:")
# Initialising client for AWS
s3 = boto3.client(
    "s3",
    aws_access_key_id="YOUR_ACCESS_KEY_ID",
    aws_secret_access_key="YOUR_SECRET_ACCESS_KEY",
    region_name="Singapore",
)

# Creating S3 bucket
history = s3.create_bucket(Bucket="history")


# Function to list ppt from S3 bucket
def list_presentations(history):
    presentations = []
    response = s3.list_objects(Bucket=history)
    history_list = response["Contents"]
    if history_list:
        for obj in history_list:
            presentations.append(obj["Key"])
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
            presigned_url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": history, "Key": presentation},
                ExpiresIn=3600,
            )  # URL expires in 1 hour
            st.markdown(f"[Download {presentation}]({presigned_url})")
    else:
        st.write("No presentations found.")
