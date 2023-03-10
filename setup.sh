#!/bin/bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"
export EXCITED="true"
export FLASK_APP=app.py
export FLASK_ENV=development
echo "setup.sh script executed successfully!"