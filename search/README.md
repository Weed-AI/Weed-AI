# Starter Guide

## Clone repository for Weed-AI and submodules and go to workdir

```
git clone --recurse-submodules -j8 -b release-candidate-2.0 git@github.com:Weed-AI/Weed-AI.git
cd Weed-AI/search/
```

## Include a `.env` file to store key credentials:

```
DJANGO_SECRET_KEY=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
SMTP_HOST=smtp.sydney.edu.au
SMTP_PORT=
FROM_EMAIL=Sender Name <sender@host>
# The following works when they are local directories on the host, which are periodically rsynced to a remote
GIT_REMOTE_PATH=/path/to/git/remote/on/rds
DVC_REMOTE_PATH=/path/to/dvc/remote/on/rds
# The following is to let traefik know which hosts are legit
HTTP_HOST=<http host>
HTTPS_HOST=<https host such as weed-ai.sydney.edu.au>
CVAT_BASEPATH='/cvat-annotation'
```

**NOTE:** if working on Linux, you need to `sudo` all docker commands.

## Initialise database, migrate and create superuser

- Database init
	1. Start PostgreSQL server: `docker-compose -f docker-compose-dev.yml up -d db`
	2. Enter server container: `docker exec -it db bash`
	3. Log in with the credential stored in `.env` file: `psql -U <POSTGRES_USER>`
	4. Create database: `create database <POSTGRES_DB>`
- Build Django:
	1. `docker build django`
- Django Migration and create superuser
	1. Start Django server: `docker-compose -f docker-compose-dev.yml up db django`
	2. Enter server container: `docker exec -it django bash`
	3. Create superuser: `python manage.py createsuperuser` and follow the prompt instruction

## Start the server in Development and Production mode:

- DEV: 
	`docker-compose -f docker-compose-dev.yml build`
	`docker-compose -f docker-compose-dev.yml up`
- PROD:
	`docker-compose -f docker-compose.yml build`
	`docker-compose -f docker-compose.yml up`
