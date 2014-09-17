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
RUN apt-get install -y vim

# stop supervisor service as we'll run it manually
RUN service supervisor stop

# build dependencies for postgres and image bindings
RUN apt-get build-dep -y python-imaging python-psycopg2

# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# Add PostgreSQL's repository. It contains the most recent stable release of PostgreSQL, ``9.3``.
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Install ``python-software-properties``, ``software-properties-common`` and PostgreSQL 9.3
RUN apt-get -y -q install python-software-properties software-properties-common
RUN apt-get -y -q install postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

# create a virtual environment and install all depsendecies from pypi
RUN virtualenv /opt/venv
ADD /scripts/requirements.txt /opt/venv/requirements.txt
RUN /opt/venv/bin/pip install -r /opt/venv/requirements.txt
RUN apt-get install -y wget
RUN wget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh

# Run the rest of the commands as the ``postgres`` user created by the ``postgres-9.3`` package when it was ``apt-get installed``
USER postgres

# Create a PostgreSQL role named ``rehabradio`` with ``rehabradio`` as the password and
# then create a database `rehabradio` owned by the ``rehabradio`` role.
ADD /scripts/initial-db.sql /opt/venv/initial-db.sql
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER rehabradio WITH SUPERUSER PASSWORD 'rehabradio';" &&\
    createdb -O rehabradio rehabradio &&\
    psql rehabradio < /opt/venv/initial-db.sql

USER root

# default run command
CMD bash

# expose port(s)
EXPOSE 8000
EXPOSE 5432