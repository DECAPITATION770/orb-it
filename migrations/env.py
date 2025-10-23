from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context


from core.config import settings
from core.db import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

cfg = config.get_section(config.config_ini_section, {})

async_url = getattr(settings, "DB_URL", cfg.get("sqlalchemy.url"))
if async_url and "+asyncpg" in async_url:
    sync_url = async_url.replace("+asyncpg", "+psycopg")
else:
    sync_url = async_url or cfg.get("sqlalchemy.url")
cfg["sqlalchemy.url"] = sync_url


target_metadata = getattr(Base, "metadata", None)


def run_migrations_offline() -> None:
    url = cfg.get("sqlalchemy.url") or config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        cfg,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
