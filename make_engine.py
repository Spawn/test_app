import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contacts.models import Base

engine = create_engine(settings.SQLITE_DB_PATH)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
