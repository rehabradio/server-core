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

- [Virtualbox >= 4.2](https://www.virtualbox.org)
- [Vagrant >= 1.4](http://www.vagrantup.com)
- [Vagrant Hostmanager Plugin](https://github.com/smdahlen/vagrant-hostmanager)
- [Vagrant VBGuest Plugin](https://github.com/dotless-de/vagrant-vbguest)


Provisioning the Vagrant environment
------------------------------------

Using the vagrant box is simple. Provided you have the prerequisites above installed, you can be up and running with a few short commands:

First, clone this repository to an appropriate location.

    dev@box:~/.../projects$ git clone ssh://git@stash.rehabstudio.com:7999/~paddy/rehabradio.git

Next, navigate inside the vagrant folder and provision the guest instance.

    dev@box:~/.../projects$ cd rehabradio/vagrant
    dev@box:~/.../vagrant$ vagrant up

Once provisioned, you can ssh into the running box and complete preparation of your environment:

    dev@box:~/.../vagrant$ vagrant ssh

You'll be dropped at a Bash shell in a Byobu environment. The application data lives in the `~/app/` folder and most actions/commands should be carried out in this folder.


Preparing your Python virtual environment
-----------------------------------------

Whilst the Vagrant box itself provides most of what you'll need to run and develop a simple app, for our purposes (testing, i18n, third-party django apps etc.) we need a few extra dependencies and tools.  Standard Python procedure is to install all dependencies in a virtualenv (both virtualenv and virtualenvwrapper should already be installed inside the Vagrant virtual machine), and so we shall:

    vagrant@rehabradio:~/app$ mkvirtualenv rehabradio

virtualenvwrapper will create and activate your new virtualenv for you. You can now install the required dependencies; the simplest method is to use pip

    (rehabradio)vagrant@rehabradio:~/app$ pip install -r requirements.txt

To deactivate the virtualenv simply type `deactivate`, and to reactivate use `workon rehabradio`.


**NOTE:** Throughout the following examples, all commands to be entered will be shown as though typed on a typical bash prompt. Where the command to be typed needs to be run inside the activated virtualenv, you will see the prompt prepended with `(rehabradio)`.


Preparing your Django environment
---------------------------------

Almost there... Before we can get started we need to complete a few final steps to set up our Django environment locally, such as creating database tables and a superuser.

    (rehabradio)vagrant@rehabradio:~/app$ python manage.py migrate

`migrate` will ask a few questions on the terminal, fill in the required details as appropriate. You should now be ready to start the application locally.

    (rehabradio)vagrant@rehabradio:~/app$ python manage.py runserver 0.0.0.0:8000

You should now be able to access the running Django application in a browser at `http://rehabradio.vagrant.local:8000/api/`

***

**Important:** This guide is woefully incomplete, feel free to expand upon it or to automate some of the above steps :)
