#!/bin/bash
# Uncomment for local postgres testing under default postgres credentials on postgres database,
# These environment variables are all present on my deployment via render cloud platform
# export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"
# export EXCITED="true"
# export FLASK_APP=app.py
# export FLASK_ENV=development
# export AUTH0_DOMAIN="dev-y4dtlj6thn26xy28.us.auth0.com"
# export ALGORITHMS="RS256"
# export API_AUDIENCE="https://NoahCapstone"
# export LOGIN_LINK="https://dev-y4dtlj6thn26xy28.us.auth0.com/authorize?audience=https://NoahCapstone&response_type=token&client_id=68eXrXxz4NSdBSNiERhGMn6sHVUzaIwb&redirect_uri=http://127.0.0.1:5000/"
pip install -r requirements.txt
python manage.py db init
python manage.py db migrate
echo "setup.sh script executed successfully!"