from sqlmodel import create_engine, text, SQLModel  
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import Config
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(
    url = Config.DATABASE_URL,
    echo = True,
    pool_pre_ping=True,
    connect_args={"statement_cache_size": 0},
)

async def init_db():
    async with engine.begin() as conn:
        from src.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)
        # statement = text("SELECT 'Hello';")
        # result = await conn.execute(statement)
        # print(f"Database connected: {result.all()}")

async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session