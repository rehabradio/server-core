FROM ubuntu:14.04
MAINTAINER Mark McConnell <mark@rehabstudio.com>

# keep upstart quiet
RUN dpkg-divert --local --rename --add /sbin/initctl
RUN ln -sf /bin/true /sbin/initctl

# no tty
ENV DEBIAN_FRONTEND noninteractive

# get up to date
RUN apt-get update --fix-missing

# global installs [applies to all envs!]
RUN apt-get install -y build-essential git
RUN apt-get install -y python python-dev python-setuptools
RUN apt-get install -y python-pip python-virtualenv
RUN apt-get install -y nginx supervisor

# stop supervisor service as we'll run it manually
RUN service supervisor stop

# build dependencies for postgres and image bindings
RUN apt-get build-dep -y python-imaging python-psycopg2

# create a virtual environment and install all depsendecies from pypi
RUN virtualenv /opt/venv
ADD ./app/requirements.txt /opt/venv/requirements.txt
RUN /opt/venv/bin/pip install -r /opt/venv/requirements.txt
RUN apt-get install -y wget
RUN wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh

# default run command
CMD bash

# expose port(s)
EXPOSE 8000
EXPOSE 5000
