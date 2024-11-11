#!/usr/bin/env bash

# Script to apply Alembic migrations in Docker for development
# Usage example:
# ./scripts/dev/migrate.sh

if docker-compose -f ./docker/dev/docker-compose.yml exec web alembic upgrade head; then
  echo "Migrations applied successfully"
else
  echo "Error: failed to apply migrations"
  exit 1
fi
