FROM rehabstudio/python-base
MAINTAINER Peter McConnell <peter.mcconnell@rehabstudio.com>

RUN virtualenv /opt/venv

# start supervisor to run our wsgi server
CMD workon rehabradio
CMD wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh
CMD cd /opt/app/ && foreman run python manage.py makemigrations
CMD cd /opt/app/ && foreman run python manage.py migrate
CMD cd /opt/app/ && foreman run python manage.py runserver 0.0.0.0:80
#CMD cd /opt/app/ && /opt/venv/bin/python manage.py runserver 0.0.0.0:80
#CMD cd /opt/app/ && /opt/venv/bin/coverage run --source='.' manage.py test apps
#CMD cd /opt/app/ && /opt/venv/bin/coverage report
