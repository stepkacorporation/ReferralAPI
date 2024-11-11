#!/usr/bin/env bash

# Script to create an Alembic migration in Docker for development
# Usage example:
# ./scripts/dev/new_migration.sh "initial migration"

if [ -z "$1" ]; then
  echo "Error: Please provide a migration message"
  echo "Usage example: ./scripts/dev/new_migration.sh \"initial migration\""
  exit 1
fi

MIGRATION_MESSAGE="$1"

if docker-compose -f ./docker/dev/docker-compose.yml exec web alembic revision --autogenerate -m "$MIGRATION_MESSAGE"; then
  echo "Migration created successfully"
else
  echo "Error: failed to create migration"
  exit 1
fi
