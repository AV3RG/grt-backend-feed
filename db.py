import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

print(os.environ.get("DB_STRING"))
engine = create_async_engine(os.environ.get("DB_STRING").__str__(), echo=True, pool_pre_ping=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)