from sqlalchemy.ext.asyncio import async_sessionmaker


async def get_async_session(session_factory: async_sessionmaker):
    async with session_factory() as session:
        yield session