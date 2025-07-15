#!/bin/bash
set -e

# --- Configuration ---
DB_NAME="your_db"
DB_USER="your_user"
DB_HOST="localhost"  # Optional
DB_PORT="5432"       # Optional
MIGRATIONS_DIR="./migrations"

# --- Get current schema version from DB ---
CURRENT_VERSION=$(psql -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT version FROM schema_version;" | xargs)
echo "Current schema version: $CURRENT_VERSION"

# --- Loop through migration files in order ---
for FILE in $(ls "$MIGRATIONS_DIR"/*.sql | sort); do
  # Extract numeric version from filename (e.g., 006 from 006_add_column.sql)
  FILE_VERSION=$(basename "$FILE" | cut -d'_' -f1 | sed 's/^0*//') # remove leading 0s
  FILE_VERSION=${FILE_VERSION:-0}  # default to 0 if empty

  # Apply only if newer than current version
  if [ "$FILE_VERSION" -gt "$CURRENT_VERSION" ]; then
    echo "Applying migration $FILE_VERSION from file $FILE"
    psql -U "$DB_USER" -d "$DB_NAME" -f "$FILE"
    psql -U "$DB_USER" -d "$DB_NAME" -c "UPDATE schema_version SET version = $FILE_VERSION;"
    echo "Updated schema_version to $FILE_VERSION"
  fi
done

echo "✅ All pending migrations applied."
