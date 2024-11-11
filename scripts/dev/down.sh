#!/usr/bin/env bash

# Stops and removes the development containers
# ./scripts/dev/down.sh

# You can also pass various arguments, for example:
# ./scripts/dev/down.sh -v

docker-compose -f ./docker/dev/docker-compose.yml down "$@"
