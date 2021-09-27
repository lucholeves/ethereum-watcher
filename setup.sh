#!/bin/bash

echo "Starting project..."

echo "Building services..."
docker-compose build
echo "Done!"

echo "Running services..."
docker-compose up -d
echo "Done!"

echo "Running migrations..."
docker-compose run django ./manage.py migrate
echo "Done!"

echo "Creating admin user..."
docker-compose run django ./manage.py createsuperuser --noinput
echo "Done!"
