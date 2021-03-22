# kentish-plovers

![Python version](https://img.shields.io/badge/Python_version-3.8-306998.svg?logo=Python&logoColor=white)
![Python version](https://img.shields.io/badge/Django_version-3.8-0C4B33.svg?logo=Django&logoColor=white)
![Bootstrap version](https://img.shields.io/badge/Bootstrap_version-5.0.0_beta2-563d7c.svg?logo=Bootstrap&logoColor=white)

![Project version](https://img.shields.io/badge/Project_version-1.3.0-ffd43b.svg)

`Kentish-plovers` is the second version of a web app used by citizens and birdwatchers to save observations and get the life track of banded kentish plovers during a program on this specie in Normandy (France).

## How to install the project

1. Install all the dependencies with `pipenv` :

   ```bash
   pipenv install # For production
   pipenv install --dev # For development
   ```

2. Add the `.env` file & fill all the informations needed (`ROLLBAR_ACCESS_TOKEN` is optionnal)

   ```bash
   cp .env.example .env
   ```

3. Migrate the database

   ```bash
   python manage.py migrate
   ```

4. Load seeds if needed

   ```bash
   python manage.py loaddata seeders/*
   ```

### Retreive a rollbar access token

Initiate the Rollbar intergration :

- Go to [https://rollbar.com](https://rollbar.com) and get an access token for this project
- Set it in `ROLLBAR_ACCESS_TOKEN`

## How to lauch the project

In a terminal :

```bash
python manage.py runserver
```
