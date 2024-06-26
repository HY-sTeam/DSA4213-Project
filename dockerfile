# Use an official Python runtime as the base image
FROM python:3.11.8

# Set the working directory in the container
WORKDIR /app

# Copy the rest of the application code to the working directory
COPY . .

# Create the requirements file from the Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pip install --no-cache-dir pipenv==2023.12.1
RUN pipenv install
# RUN pipenv run pip freeze > requirements.txt
# RUN pip3 install -r requirements.txt

# Expose the port on which the application will run. In this case, streamlit runs on 8501
EXPOSE 8501

# Define the command to run the application
# ENTRYPOINT ["pipenv", "run", "streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
ENTRYPOINT ["pipenv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8501/api/v1/health || exit 1
