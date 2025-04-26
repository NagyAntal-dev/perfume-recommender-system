#!/bin/sh
set -e


echo "Copying custom configuration files to $PGDATA"
cp /etc/postgresql/custom/postgresql.conf "$PGDATA/postgresql.conf"
cp /etc/postgresql/custom/pg_hba.conf "$PGDATA/pg_hba.conf"

chown postgres:postgres "$PGDATA/postgresql.conf" "$PGDATA/pg_hba.conf"
chmod 600 "$PGDATA/postgresql.conf" "$PGDATA/pg_hba.conf"

echo "Custom configuration files copied."
