#! /usr/bin/env bash

# Create and run docker
docker-compose up -d --build --force-recreate
sleep 3

# Change to terraform directory and apply infra
cd tf
terraform init
sleep 5
terraform apply -auto-approve

# Deploy chalice local chalice application
sleep 5
cd ..
cd application

# Generate requirements.txt
pipenv requirements > requirements.txt

chalice-local deploy