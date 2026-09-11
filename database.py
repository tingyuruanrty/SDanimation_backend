from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column

# 1. Database URL: SQLite stores data locally in 'characters.db'
# When switching to PostgreSQL later, just change this string to:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
SQLALCHEMY_DATABASE_URL = "sqlite:///./characters.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # SQLite requires this flag when used with multiple threads in FastAPI
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Define the Character Relation (Table)
class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    trigger_word: Mapped[str] = mapped_column(String, nullable=False)
    lora_filename: Mapped[str] = mapped_column(String, nullable=False)

# 3. Create all tables on startup
Base.metadata.create_all(bind=engine)

# 4. Dependency to yield database sessions per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()