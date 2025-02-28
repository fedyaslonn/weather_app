from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.sql_rep_interfaces import T


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> T:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()
