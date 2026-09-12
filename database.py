from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column

# 1. Database URL: SQLite stores data locally in 'characters.db'
# When switching to PostgreSQL later, just change this string to:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
# it gives engine three important fact: 1, what database , sqlite in this case; 2, database api, it could be omitted, default option will take in charge; 3, 

# make engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./characters.db"
# establish connections to database
engine = create_engine(
    # URL string for the database
    SQLALCHEMY_DATABASE_URL,
    # SQLite requires this flag when used with multiple threads in FastAPI
    connect_args={"check_same_thread": False}
)

# i want to use the facade of sqlalchemy, which is session

# it's a boilerplate for session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# base is the blueprint of table
# make table
Base = declarative_base()
# 2. Define the Character Relation (Table)
class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    trigger_word: Mapped[str] = mapped_column(String, nullable=False)
    lora_filename: Mapped[str] = mapped_column(String, nullable=False)

# 3. Create all tables on startup
# metadata is like the blue print book, the tables are bluepritn
# create the data base
Base.metadata.create_all(bind=engine)

# 4. Dependency to yield database sessions per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()