from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<databasename>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@"\
                          f"{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

#responsible for establishing that connection 
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#our modals will be extending this base class 
Base = declarative_base()

# Dependency
#session object talks to our database and send sql statements to it (more efficient)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
