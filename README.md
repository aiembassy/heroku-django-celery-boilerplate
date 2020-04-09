# heroku-django-celery-boilerplate

A boilerplate for a Django application with some Celery workers in the 
background. The repository contains a general file structure for the Django
application with some additional background workers running using Celery. It 
includes a lightweight Docker image which allows to run all the services with 
Docker containers locally, for the purposes of *development* environments.

## Introduction

This boilerplate is set up in order to support any application running with the
following stack:

- **Django**, as a web framework
- **PostgreSQL**, as a database engine
- **Celery**, for the background tasks

### Prerequisites

This document assumes you have already installed the 
[Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). The process
of installation may vary between different environments and is not described
in this document. Other than that, a Python 3.6+ interpreter and pip are also
required, if you are not using Docker for running the services locally. This 
repository, besides using Docker, assumes the 
[deployment with git](https://devcenter.heroku.com/articles/git) strategy, with
the Docker container running just for reproducible environment like the remote
Heroku one.

#### First steps

1. Login to your Heroku account from the console using `heroku login`.
2. Create a new Heroku project with `./heroku.py create [APP_NAME]`. 
3. Provision a PostgreSQL database with 
   `./heroku.py addons:create heroku-postgresql:hobby-dev`.
4. Provision a RabbitMQ task queue with 
   `./heroku.py addons:create cloudamqp:lemur` (that requires to have a credit 
   card configured on Heroku).
5. Deploy the empty project with `./heroku.py deploy`.
6. Open the project in the browser `./heroku.py open`
   
```
./heroku.py create [APP_NAME]-staging
./heroku.py addons:create heroku-postgresql:hobby-dev
./heroku.py addons:create cloudamqp:lemur
./heroku.py deploy
./heroku.py open
```

### Choosing Celery broker

Celery is capable of running with different message brokers. Heroku delivers 
the following options:

- RabbitMQ, through [CloudAMQP](https://elements.heroku.com/addons/cloudamqp)
- Redis, through [Heroku Redis](https://elements.heroku.com/addons/heroku-redis)

This repository uses RabbitMQ message broker, but based on its configuration,
it is fairly easy to set up the similar environment, but with the Redis backend.

### Environments

For the typical application lifecycle, we assume having at least three different
environments:

- **development** - used locally by the developers, one per developer
- **staging** - the testing environment, typically one per project, might be
                running an unstable version of the software
- **production** - the final environment, typically one per project, publicly
                   available, should run the latest stable version of the 
                   application
                   
Each environment will have different values of some configuration properties, 
like the database connection URL and other hostnames, ports, etc. In addition
some cryptographic related attributes might differ between the environments.
Heroku allows to differentiate those by using some different .env files. As a
rule of thumb, they should not be included in the VCS! All the variables 
declared in these files, will be exposed as environmental variables in the 
application and might be accessed via `os.environ` in Python.

For the purposes of this boilerplate, we defines an .env.example file that might
be used as a base for different environments. Providing a postfix to the file 
name, like ".env.production" is a common strategy, and we'll do so in all the
examples below.

See: https://devcenter.heroku.com/articles/multiple-environments

### Important files

## Application structure

### Static files

Static files are going to be served through gunicorn, by using the
[whitenoise](http://whitenoise.evans.io/en/stable/) package. For some 
high-throughput applications you should probably consider using CDN for storing
