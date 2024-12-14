<!-- Logo -->
<!-- <p align="center">
  <a href="https://www.freepik.com/icon/pill_5419351"><img width="256" height="256" src="https://raw.githubusercontent.com/maekind/shortener/main/logo.png"></a>
</p> -->
<!-- Shields -->
<p align="center">
<a href="https://github.com/maekind/shortener/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-orange.svg" hspace="5"></a>
<a href="https://github.com/maekind/shortener"><img src="https://img.shields.io/github/repo-size/maekind/shortener?color=red" hspace="5"></a>
<a href="https://github.com/maekind/shortener"><img src="https://img.shields.io/github/last-commit/maekind/shortener?color=black" hspace="5"></a>
<a href="https://www.python.org/downloads/"><img src="https://img.shields.io/github/languages/top/maekind/shortener?color=darkgreen" hspace="5"></a>
<a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python%20version-%3E3.12-lightblue" hspace="5"></a>
</p>

<h1 align="center">Shortener backend</h1>

## Development

### pre-commit hooks

This project uses [pre-commit](https://pre-commit.com/) to enforce code quality and consistency.
To install the pre-commit hooks, run:

```bash
pre-commit install
pre-commit autoupdate
```

### Settings

Can be obtained from a `.env` file placed in the backend directory or exporting the following environment variables:

```bash
export PROJECT_NAME=shortener
export POSTGRES_SERVER=localhost
export POSTGRES_PORT=5432
export POSTGRES_DB=shortener
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
```

### Database

This project uses postgresql as the database. To run the database, you can use the following command:

```bash
docker run --name shortener-local-db -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -d postgres:latest
```

First time, you need to create the database and then run the migrations.
Make sure you have the environment variables set up correctly.
To create the database go to `scripts` directory and run:

```bash
python cli.py create-db
```

Then, run the migrations:

```bash
alembic revision --autogenerate -m "Initial migration"
```

First time we run it, the migration will fail, because alembic does not import sqlmodel module. To fix this,
we need to add it to the migration file generated, downgrade the migration, delete manually the table `alembic_version`
and run the migration again:

```bash
alembic downgrade base
# delete the table alembic_version
```

Then, apply the migration:

```bash
alembic upgrade head
```
