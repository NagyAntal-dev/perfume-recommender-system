#!/usr/bin/env bash

set -e
set -x

# Check if the data directory is uninitialized (no PG_VERSION file)
if [ ! -s "$PGDATA/PG_VERSION" ]; then
  echo "Data directory empty. Running replica initialization script (00_init_replica.sh)..."
  /docker-entrypoint-initdb.d/00_init_replica.sh
  echo "Replica initialization script finished."
else
  echo "Existing data found in $PGDATA, skipping replica initialization script."
  touch "$PGDATA/standby.signal"
fi

echo "Copying replica configuration files..."
cp /etc/postgresql/replica/postgresql.conf "$PGDATA/postgresql.conf"
cp /etc/postgresql/replica/pg_hba.conf     "$PGDATA/pg_hba.conf"

chown postgres:postgres "$PGDATA/postgresql.conf" "$PGDATA/pg_hba.conf"
chmod 600 "$PGDATA/postgresql.conf" "$PGDATA/pg_hba.conf"

echo "Setting ownership of $PGDATA to postgres user..."
chown -R postgres:postgres "$PGDATA"

echo "Setting permissions of $PGDATA to 0700..."
chmod 0700 "$PGDATA"

# Start the PostgreSQL server process as the 'postgres' user in standby mode
# The 'postgres' command will respect the standby.signal file
echo "Starting PostgreSQL in standby mode as user postgres..."
exec gosu postgres postgres
