#!/usr/bin/env bash
set -e
set -x # Enable debug output

# 00_init_replica.sh
# Bootstraps the standby: waits for primary, then pg_basebackup + standby.signal

PRIMARY_HOST="postgres"
PRIMARY_PORT=5432
REPL_USER="replicator"
REPL_PASS="replicator_pass"
PGDATA="/var/lib/postgresql/data"

export PGPASSWORD="$REPL_PASS"

# 1) Wait until primary is accepting connections (removed -d oltp_db)
until pg_isready -h "$PRIMARY_HOST" -p "$PRIMARY_PORT" -U "$REPL_USER"; do
  echo "Waiting for primary at $PRIMARY_HOST:$PRIMARY_PORT..."
  sleep 1
done

# 2) If PGDATA is empty, take a base backup
if [ ! -s "$PGDATA/PG_VERSION" ]; then
  echo "Initializing standby via pg_basebackup..."
  pg_basebackup \
    -h "$PRIMARY_HOST" \
    -p "$PRIMARY_PORT" \
    -d dbname=oltp_db \
    -D "$PGDATA" \
    -U "$REPL_USER" \
    -Fp -Xs -P --slot=replication_slot
fi

# 3) Create standby.signal (PostgreSQL ≥12) to run in standby mode
touch "$PGDATA/standby.signal"

# 4) Append primary_conninfo and replication slot to postgresql.auto.conf
# Ensure the file exists before appending, especially if base backup was skipped
touch "$PGDATA/postgresql.auto.conf"
cat >> "$PGDATA/postgresql.auto.conf" <<EOF
primary_conninfo = 'host=$PRIMARY_HOST port=$PRIMARY_PORT user=$REPL_USER password=$REPL_PASS'
primary_slot_name = 'replication_slot'
hot_standby = on
EOF

echo "Standby initialization complete; streaming replication will start on launch."
