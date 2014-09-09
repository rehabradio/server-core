FROM rehabstudio/python-base
MAINTAINER Peter McConnell <peter.mcconnell@rehabstudio.com>

# start supervisor to run our wsgi server
CMD cd /opt/app/ && /opt/venv/bin/python manage.py makemigrations
CMD cd /opt/app/ && /opt/venv/bin/python manage.py migrate
CMD cd /opt/app/ && /opt/venv/bin/python manage.py runserver

EXPOSE 8000