from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

from tgbot.config import load_config
from tgbot.db.models import BaseModel




async def get_async_sessionmaker(config) -> sessionmaker:
    """Get sessionmaker instance"""

    engine = create_async_engine(
        f"postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.database}",
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_= AsyncSession)

    return async_sessionmaker

