from fastapi import FastAPI
from fastapi.routing import APIRoute
from psycopg import connect, errors
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


# Lifespan function for FastAPI lifecycle events
async def lifespan(app: FastAPI):
    """Application lifecycle events"""
    # Database creation logic
    dsn = str(settings.SQLALCHEMY_URI)
    db_name = settings.POSTGRES_DB

    # Establish a connection to the PostgreSQL server
    with connect(dsn, autocommit=True) as conn:
        with conn.cursor() as cur:
            try:
                # Attempt to create the database
                cur.execute(f"CREATE DATABASE {db_name}")
                print(f"Database {db_name} created successfully.")
            except errors.DuplicateDatabase:
                # Database already exists
                print(f"Database {db_name} already exists.")

    # Run migrations (e.g., Alembic)
    from alembic import command
    from alembic.config import Config

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield  # Yield to indicate lifespan end

    # Cleanup or shutdown logic, if any, goes here
    print("Application is shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
