from sqlalchemy  import create_engine
from  sqlalchemy.orm  import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
sql_database_url = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(sql_database_url)

sessionlocal = sessionmaker(bind=engine, autocommit=False, autoflush= False)

Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()