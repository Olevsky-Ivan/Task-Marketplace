import asyncio
import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from app.database.base import Base
from app.models import *

load_dotenv()

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url(driver: str = "asyncpg") -> str:
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL не встановлено в .env")

    url = url.replace("postgresql+asyncpg://", "postgresql://") \
              .replace("postgresql+psycopg2://", "postgresql://")

    if driver == "asyncpg":
        return url.replace("postgresql://", "postgresql+asyncpg://")
    return url.replace("postgresql://", "postgresql+psycopg2://")


def run_migrations_offline() -> None:
    context.configure(
        url=get_url("psycopg2"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()



def do_run_migrations(connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(
        get_url("asyncpg"),
        poolclass=pool.NullPool,
    )

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await engine.dispose()



if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())