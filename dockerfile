# Use an official Python runtime as the base image
FROM python:3.11.8

# Set the working directory in the container
WORKDIR /

# Copy the rest of the application code to the working directory
COPY . .

# Create the requirements file from the Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pip install --no-cache-dir pipenv==2023.12.1
RUN pipenv install --deploy
# RUN pipenv run pip freeze > requirements.txt
# RUN pip3 install -r requirements.txt

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose the port on which the application will run. In this case, streamlit runs on 8501
EXPOSE 8501

# Define the command to run the application
ENTRYPOINT ["pipenv", "run", "streamlit", "run", "app.py", "--server.port=8501"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8501/api/v1/health || exit 1
