+rehabradio
===========

***

A collaborative, online playlist manager

![A collaborative, online playlist manager](http://bloodsweatandfashion.com/wp-content/uploads/LL-Cool-J-Ghetto-Blaster.jpg)


Overview
========

***

+rehabradio is a collaborative, online playlist manager and general music browser/search tool. Its purpose is to enable simple collaborative control of music in all rehabstudio offices. rehabradio initally has a very limited feature set but will be expanded with time to allow a more comprehensive music management experience.


Platform
--------

* Platform: Amazon EC2 (Ubuntu 14.04)
* Language: Python 2.7
* Framework: Django 1.7
* Database: Amazon RDS (PostgreSQL)
* File Storage/Serving: Amazon S3
* Caching: Amazon Elasticache (Redis)
* Queueing/Asynchronous operation: RQ (via Django-RQ)


Getting Started
===============

***

Requirements
------------

Before you can use this project, you'll need to install a few dependencies:

- [Foreman/Heroku-Toolbelt](https://toolbelt.heroku.com/)
- [virtualenvWrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html)


Foreman
-----------------------------------------
Foreman requires a `.env` file to work. Please ensure you create this file in the project root directory (same directory as manage.py), and ensure the following keys are listed

SECRET_KEY=[django secret key]

GOOGLE_OAUTH2_CLIENT_ID=[google client id]
GOOGLE_OAUTH2_CLIENT_SECRET=[google client secret key]
GOOGLE_WHITE_LISTED_DOMAINS=[list of email domains that can access the api]

SOUNDCLOUD_CLIENT_ID=[soundcloud secret key]

TEST_USERNAME=[username for test login]
TEST_PASSWORD=[password for test login]

DATABASE_URL=[url to database server]

REDIS_LOCATION=[url to redis server]


Preparing your Python virtual environment
-----------------------------------------

Standard Python procedure is to install all dependencies in a virtualenv (both virtualenv and virtualenvwrapper should already be installed before this step), and so we shall:
    vagrant@rehabradio:~/$ cd server-core
    vagrant@rehabradio:~/server-core$ mkvirtualenv rehabradio

virtualenvwrapper will create and activate your new virtualenv for you. You can now install the required dependencies; the simplest method is to use pip

    (rehabradio)vagrant@rehabradio:~/server-core$ pip install -r requirements.txt

To deactivate the virtualenv simply type `deactivate`, and to reactivate use `workon rehabradio`.


**NOTE:** Throughout the following examples, all commands to be entered will be shown as though typed on a typical bash prompt. Where the command to be typed needs to be run inside the activated virtualenv, you will see the prompt prepended with `(rehabradio)`.


Preparing your Django environment
---------------------------------

Almost there... Before we can get started we need to complete a few final steps to set up our Django environment locally, such as creating database tables and a superuser.

    (rehabradio)vagrant@rehabradio:~/server-core$ mkdir databases
    (rehabradio)vagrant@rehabradio:~/server-core$ python manage.py migrate

`migrate` will ask a few questions on the terminal, fill in the required details as appropriate. You should now be ready to start the application locally.

    (rehabradio)vagrant@rehabradio:~/server-core$ python manage.py runserver

You should now be able to access the running Django application in a browser at `http://localhost:8000/api/`

***

**Important:** This guide is woefully incomplete, feel free to expand upon it or to automate some of the above steps :)
