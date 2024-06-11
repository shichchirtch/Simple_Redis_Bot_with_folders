from sqlalchemy import Integer, BigInteger, String, ARRAY
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import settings

engine = create_async_engine(settings.DATABASE_URL,
                             echo=True)

session_marker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

metadata = Base.metadata

class User(Base):

    __tablename__ = 'users'
    index: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    id: Mapped[int] = mapped_column(BigInteger) # tg user id
    user_name: Mapped[str] = mapped_column(String(200), nullable=False)
    secret_number: Mapped[int] = mapped_column(Integer, default=0)
    attempts: Mapped[int] = mapped_column(Integer, default=5, nullable=True)
    steps: Mapped[list[list[int]]] = mapped_column(ARRAY(Integer), default=[], nullable=True)
    start_time: Mapped[int] = mapped_column(BigInteger)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

