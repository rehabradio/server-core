FROM rehabstudio/python-base
MAINTAINER Peter McConnell <peter.mcconnell@rehabstudio.com>

# start supervisor to run our wsgi server
CMD cd /opt/app/ && /opt/venv/bin/python manage.py makemigrations &&\
/opt/venv/bin/coverage run --source='.' manage.py test apps &&\
/opt/venv/bin/coverage report
#/opt/venv/bin/python manage.py runserver 0.0.0.0:80