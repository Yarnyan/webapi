
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

if settings.postgres_password:
    auth = f"{settings.postgres_user}:{settings.postgres_password}"
else:
    auth = settings.postgres_user

DATABASE_URL = (
    f"postgresql+asyncpg://{auth}@"
    f"{settings.postgres_host}:{settings.postgres_port}/"
    f"{settings.postgres_db}"
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)