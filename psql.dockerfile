# Use the official PostgreSQL image from Docker Hub
FROM postgres:latest

# Set the environment variables
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword

# Copy initialization script
COPY db_scripts /docker-entrypoint-initdb.d

# RUN chmod +x /docker-entrypoint-psqldb.sh

USER postgres

# Expose the PostgreSQL port
EXPOSE 5432


# Run PostgreSQL when the container launches
CMD ["postgres"]
