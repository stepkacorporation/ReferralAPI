#!/usr/bin/env bash

# Starts the containers for development
# ./scripts/dev/up.sh

# You can also pass various arguments, for example:
# ./scripts/dev/up.sh -d --build

docker-compose -f ./docker/dev/docker-compose.yml up "$@"
