from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase 
from motor.motor_asyncio import AsyncIOMotorClient

# (Configuração centralizada do banco de dados)

DATABASE_URL = "sqlite:///banco_final.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# MONGO_URL = "mongodb+srv://analistaforense:OaQKatRGsPNQS2rZ@cluster0.bqlrw4x.mongodb.net/ArgosDB?retryWrites=true&w=majority"
# client = AsyncIOMotorClient(MONGO_URL)
# db = client["ArgosDB"]
# engine = create_engine(MONGO_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()
class Base(DeclarativeBase):
    """
    Classe base para todos os modelos do SQLAlchemy.
    As ferramentas de checagem de tipo entendem esta declaração.
    """
    pass

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)