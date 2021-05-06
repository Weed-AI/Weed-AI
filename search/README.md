# Starter Guide

1. `docker-compose up --build --force-recreate`
2. Mount RDS and run `scripts/load_data_from_rds.sh` to load all prepared data
3. Open http://localhost:1337 for the reactive search UI
4. localhost:5601 for kibana and elastic stack

## Start the server in Development and Production mode:

- DEV: 
	`docker-compose -f docker-compose-dev.yml build`
	`docker-compose -f docker-compose-dev.yml up`
- PROD:
	`docker-compose -f docker-compose.yml build`
	`docker-compose -f docker-compose.yml up`

### Include a `.env` file to store key credentials:
```
DJANGO_SECRET_KEY=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
SMTP_HOST=smtp.sydney.edu.au
SMTP_PORT=
FROM_EMAIL=Sender Name <sender@host>
```