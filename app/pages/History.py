import base64
import json
import os
from datetime import date, datetime, timedelta
from io import BytesIO

import pandas as pd
import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt

st.title('Hello World')
st.error(st.session_state.email)
st.error(st.session_state)
