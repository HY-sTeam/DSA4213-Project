
# Use an official Python runtime as the base image
FROM python:3.11.8

# Set the working directory in the container
WORKDIR /src

# Create the requirements file from the Pipfile.lock
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./


# Install the dependencies
RUN pipenv install --deploy
RUN pipenv run pip freeze > requirements.txt

# Copy the rest of the application code to the working directory
COPY /src /src

# Expose the port on which the application will run
EXPOSE 9000

# Define the command to run the application
ENTRYPOINT ["pipenv", "run", "python"]
CMD ["/src/app.py"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:9000/api/v1/health || exit 1
