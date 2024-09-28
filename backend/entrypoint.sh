#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Docker registry credentials (can be passed as environment variables)
DOCKER_REGISTRY=${DOCKER_REGISTRY:-"dreg.knust.edu.gh"}
DOCKER_USERNAME=${DOCKER_USERNAME}
DOCKER_PASSWORD=${DOCKER_PASSWORD}

# Docker registry credentials (can be passed as environment variables)
DOCKER_REGISTRY=${DOCKER_REGISTRY:-"https://index.docker.io/v1/"}
DOCKER_USERNAME=${DOCKER_USERNAME}
DOCKER_PASSWORD=${DOCKER_PASSWORD}

echo "***********************************"
echo " RUNNING STARTUP CHECKS"
echo "***********************************"


echo "***********************************"
echo " SEEDING DATABASE CHECKS"
echo "***********************************"
python -m prestart
# Create initial data in DB
python -m init_data


# Start the FastAPI app with Uvicorn
echo "***********************************"
echo " *** CHECKS COMPLETED, STARTING APP SERVER ... ***"
echo "***********************************"
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload --root-path=/api/
