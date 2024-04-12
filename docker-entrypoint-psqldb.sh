#!/bin/sh

# Ensure the script has execute permissions
# chmod +x /docker-entrypoint-initdb.d/docker-entrypoint.sh

# Error handling - exit immediately if any command fails
set -e

# Initialize the PostgreSQL database cluster
initdb -D /var/lib/postgres/data

# Start the PostgreSQL server
pg_ctl -D "/var/lib/postgres/data" -o "-c listen_addresses=''" -w start

# Create a PostgreSQL user
psql -d postgres -c "CREATE USER someuser WITH PASSWORD 'jkhkjah';"

# Create a PostgreSQL database owned by the user
psql -v ON_ERROR_STOP=1 -d postgres -c "CREATE DATABASE dockertest OWNER someuser;"

# Stop the PostgreSQL server
pg_ctl -v ON_ERROR_STOP=1 -D "/var/lib/postgres/data" -m fast -w stop

# Replace the shell process with the specified command or arguments
exec "$@"
