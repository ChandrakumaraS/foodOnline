# #!/bin/bash

# # Add PostgreSQL bin directory to PATH
# export PATH=$PATH:/c/Program\ Files/PostgreSQL/16/bin

# # Navigate to the Django project directory
# cd ~/Desktop/django_project1

# # Activate the virtual environment
# source django_project1/Scripts/activate

# # Export environment variables from the .env file
# export $(grep -v '^#' .env | xargs)

# # Verify database connection
# psql -h localhost -U postgres -d foodonline_db -c '\q'
# if [ $? -ne 0 ]; then
#     echo "Error: Cannot connect to database foodonline_db"
#     exit 1
# fi

# # Run Django migrations
# python manage.py migrate

# # Run Django development server
# python manage.py runserver
