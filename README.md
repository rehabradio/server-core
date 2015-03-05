+rehabradio
===========

![Docker](http://www.linux.com/news/galleries/image/docker?format=image&thumbnail=small)
![Django](https://lh5.googleusercontent.com/-BjCviey1170/AAAAAAAAAAI/AAAAAAAAABQ/A9zxQUjc3C4/photo.jpg?sz=64)
![Python](http://blog.magiksys.net/sites/default/files/pictures/python-logo-64.png)

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


Foreman
-----------------------------------------
Foreman requires a `.env` file to work. Please ensure you create this file
in the project root directory (same directory as manage.py),
and ensure the following keys are listed

    ENVIRONMENT=[LOCAL/LIVE/TEST]

    SECRET_KEY=[django secret key]

    GOOGLE_OAUTH2_CLIENT_ID=[google client id]
    GOOGLE_OAUTH2_CLIENT_SECRET=[google client secret]
    GOOGLE_WHITE_LISTED_DOMAINS=[list of email domains that can access the api]

    SOUNDCLOUD_CLIENT_ID=[soundcloud client id]
    SOUNDCLOUD_CLIENT_SECRET=[soundcloud client secret]

    SPOTIFY_CLIENT_ID=[soundcloud client id]
    SPOTIFY_CLIENT_SECRET=[soundcloud client secret]

    TEST_USERNAME=[username for test login]
    TEST_PASSWORD=[password for test login]

    DATABASE_URL=[url to live database server]
    LOCAL_DATABASE_URL=[url to local database server]

    REDIS_LOCATION=[url to redis server]


Running server through Docker
=================

***

To run your docker container run automatically run:

    $ make run

Visit the running application [http://localhost:8000/api/](http://localhost:8000/api/)

To have more controll over the server run:

    $ make start

This is start the container and start the containers terminal. From here use the app/Makefile to start your server

    $ cd app
    $ make run

Check out the `Makefile` in the `app/` folder for all available commands.


***
Please be aware that any changes in the database will be destroyed when you stop your container.
So if you need to make any permanent changes remember to dump your database before you stop the container

Note that the database is created with some test data to get your started

    Username: admin
    Password: rehabradio


Deploying to Heroku
=================

***
To push your app up to heroku, the recommended method with git.
Note all of the following commands shoud be run from outside of the docker container.

Create your ssh key (or use existing key)

    $ ssh-keygen -t rsa

Add the contents of the new key to your heroku account under the "SSH Keys" tab. [https://dashboard.heroku.com/account](https://dashboard.heroku.com/account)

Add heroku to your local git repo

    $ git remote add heroku git@heroku.com:{heroku-app-name}.git

Note you only want to push up the `app` folder, so you can use git subtree to achieve this.

    $ git subtree push --prefix app heroku master


[boot2docker]: http://boot2docker.io/  "boot2docker"
[docker]: https://docker.io  "Docker"
[docker_install]: https://docs.docker.com/installation/  "Docker Installation"
[docker_osx_install]: https://docs.docker.com/installation/mac/  "Docker Installation OSX"