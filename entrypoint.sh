#!/bin/bash
set -ue

echo "Waiting for the database to be up"
sleep 10

echo "Generating tables in database"
pipenv run python smta/manage.py migrate

echo "Load some example users"
pipenv run python smta/manage.py loaddata example_users

echo "#############################################"
echo "Starting app, you should be able to log in:"
echo "---------------------------------------------"
echo "http://localhost:8000"
echo "---------------------------------------------"
echo "user: administrator | password: Barcelona2018"
echo "#############################################"
pipenv run python smta/manage.py runserver
