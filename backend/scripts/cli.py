#!/usr/bin/env python
from sqlalchemy import create_engine, text
from typer import Typer, echo

from app.core.config import Settings

# Dynamically load a specific .env file
settings = Settings(model_config={"env_file": "../.env"})

# Create a Typer app
app = Typer()


@app.command()
def create_db(database_name: str = None):
    """Create a database."""
    # Create an engine without connecting to a specific database
    default_engine = create_engine(str(settings.SQLALCHEMY_URI))

    # Create the target database
    with default_engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT").execute(
            text(f"CREATE DATABASE {database_name or settings.POSTGRES_DB}")
        )

    echo(f"Database {settings.POSTGRES_DB} created successfully!", color="green")


@app.command()
def drop_db(database_name: str = None):
    """Drop a database."""
    # Create an engine without connecting to a specific database
    default_engine = create_engine(str(settings.SQLALCHEMY_URI))

    # Drop the target database
    with default_engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT").execute(
            text(f"DROP DATABASE {database_name or settings.POSTGRES_DB}")
        )

    echo(f"Database {settings.POSTGRES_DB} dropped successfully!", color="green")


if __name__ == "__main__":
    app()
