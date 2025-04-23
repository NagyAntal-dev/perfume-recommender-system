CREATE ROLE replicator WITH REPLICATION LOGIN ENCRYPTED PASSWORD 'replicator_pass';
SELECT pg_create_physical_replication_slot('replication_slot');