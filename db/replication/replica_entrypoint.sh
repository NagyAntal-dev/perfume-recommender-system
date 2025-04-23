#!/usr/bin/env bash
# filepath: c:\Users\xy\Desktop\BEADANDO\perfume-recommender-system\db\replication\replica_entrypoint.sh

set -e # Exit immediately if a command exits with a non-zero status.
set -x # Print commands and their arguments as they are executed.

# Check if the data directory is uninitialized (no PG_VERSION file)
if [ ! -s "$PGDATA/PG_VERSION" ]; then
  echo "Data directory empty. Running replica initialization script (00_init_replica.sh)..."
  # Run the script that performs pg_basebackup
  # Note: This script should handle waiting for the primary, pg_basebackup, and creating standby.signal/postgresql.auto.conf
  /docker-entrypoint-initdb.d/00_init_replica.sh
  echo "Replica initialization script finished."
else
  echo "Existing data found in $PGDATA, skipping replica initialization script."
  # Ensure standby.signal exists if restarting an existing replica volume
  # This is crucial for subsequent starts after the initial pg_basebackup
  touch "$PGDATA/standby.signal"
fi

# Copy replica-specific config files from temp location into PGDATA
# This overwrites any versions included in the base backup or default initdb
echo "Copying replica configuration files..."
cp /etc/postgresql/replica/postgresql.conf "$PGDATA/postgresql.conf"
cp /etc/postgresql/replica/pg_hba.conf     "$PGDATA/pg_hba.conf"
# Ensure correct ownership (postgres user/group) and permissions for config files
chown postgres:postgres "$PGDATA/postgresql.conf" "$PGDATA/pg_hba.conf"
chmod 600 "$PGDATA/postgresql.conf" "$PGDATA/pg_hba.conf"

# Ensure the entire data directory is owned by the postgres user
# This must happen AFTER all files are created/copied by root (e.g., pg_basebackup, touch, cp)
# and BEFORE starting the server as the postgres user.
echo "Setting ownership of $PGDATA to postgres user..."
chown -R postgres:postgres "$PGDATA" # Add this line

# Ensure the data directory has the correct permissions (must be done after chown)
echo "Setting permissions of $PGDATA to 0700..."
chmod 0700 "$PGDATA" # Add this line

# Start the PostgreSQL server process as the 'postgres' user in standby mode
# The 'postgres' command will respect the standby.signal file
echo "Starting PostgreSQL in standby mode as user postgres..."
exec gosu postgres postgres
