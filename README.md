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


Installing Docker
=================

***

This application uses [Docker][docker] to provide a standard development
environment for all developers on a project, this is the preferred method of
installation/development.

Linux
-----------------------------------------

Docker is best supported on Linux, you can probably find packages for your
preferred distribution [here][docker_install].

**Note:** Please don't run docker as root (or with sudo), it'll cause files
created within the container to be owned by root on the host system. This will
prevent you from editing/deleting the files using your regular user account.

Adding your user to the `docker` group will allow to run docker without root
privileges. Running `sudo gpasswd -a $USER docker` and logging out/in again
should do the trick.

You can now skip ahead to **"Getting the application"** below.

OSX
-----------------------------------------

Installing and configuring Docker on OSX isn't quite as straightforward as it
is on Linux (yet). The [boot2docker][boot2docker] project provides a
lightweight Linux VM that acts as a (mostly) transparent way to run docker on
OSX.

First, install Docker and boot2docker following the instructions on
[this page][docker_osx_install]. Once you've installed Docker and launched
`boot2docker` for the first time, you need to stop it again so we can make
further modifications: `$ boot2docker stop`.

Since Docker on OSX is technically running inside a virtual machine and not
directly on the host OS, any volumes mounted will be on the VM's filesystem
and any bound ports will be exposed only to the boot2docker VM. We can work
around these limitations with a few tweaks to our setup.

In order to mount folders from your host OS into the boot2docker VM you'll
need to download a version of the boot2docker iso with Virtualbox's Guest
Additions installed:

    $ mkdir -p ~/.boot2docker
    $ curl http://static.dockerfiles.io/boot2docker-v1.2.0-virtualbox-guest-additions-v4.3.14.iso -o ~/.boot2docker/boot2docker.iso

Next, you need to tell Virtualbox to mount your `/Users` directory inside the
VM:

    $ VBoxManage sharedfolder add boot2docker-vm -name home -hostpath /Users

And that should be it. Letâ€™s verify:

    $ boot2docker up
    $ boot2docker ssh "ls /Users"

You should see a list of all user's home folders from your host OS. Next, we
need to forward the appropriate ports so that we can reach the running
appengine development server directly from the host OS:

    $ VBoxManage controlvm boot2docker-vm natpf1 "aesdk,tcp,127.0.0.1,8080,,8080"
    $ VBoxManage controlvm boot2docker-vm natpf1 "aesdkadmin,tcp,127.0.0.1,8000,,8000"

And you should be ready to go, just follow the rest of the setup guide.

Windows
-----------------------------------------

![Tumbleweed](http://media.giphy.com/media/5x89XRx3sBZFC/giphy.gif)



Foreman
-----------------------------------------
Foreman requires a `.env` file to work. Please ensure you create this file
in the project root directory (same directory as manage.py),
and ensure the following keys are listed

    ```
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
    ```


Running server through Docker
=================

***

To build your docker container run:

    $ make run

Once this is finished you will be in the docker container terminal.

Run this project locally from the command line:

    $ source /opt/venv/bin/activate
    $ cd /app/
    $ make run

Visit the running application [http://localhost:8000](http://localhost:8000)

Check out the `Makefile` in the `app/` folder for all available commands.
