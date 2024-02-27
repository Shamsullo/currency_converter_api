# # from sqlalchemy import create_engine
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker
# #
# # from .config import settings
# #
# # SQLALCHEMY_DATABASE_URL = settings.database_url
# #
# # engine = create_engine(SQLALCHEMY_DATABASE_URL)
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# #
# # Base = declarative_base()
# import logging
# from typing import Annotated, AsyncIterator
#
# from fastapi import Depends
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
#
# from app.config import settings
#
# logger = logging.getLogger(__name__)
#
# async_engine = create_async_engine(
#     settings.database_url,
#     pool_pre_ping=True,
# )
# AsyncSessionLocal = async_sessionmaker(
#     bind=async_engine,
#     autoflush=False,
#     future=True,
# )
#
#
# async def get_session() -> AsyncIterator[async_sessionmaker]:
#     try:
#         yield AsyncSessionLocal
#     except SQLAlchemyError as e:
#         logger.exception(e)
#
#
# AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings

engine = create_async_engine(settings.database_url)
SessionLocal = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
