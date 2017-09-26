from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

from settings import SQLITE_DB_PATH

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(), nullable=False)
    phone_number = Column(Integer)
    company = Column(String(50))
    address = Column(String(50))
    street_address = Column(String(50), nullable=False)
    unit_number = Column(String(50))
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(50), nullable=False)
    country = Column(String(50), default="US")
    notes = Column(String(50))

    def as_dict(self):
        return {c.name: getattr(self, c.name)
                for c in self.__table__.columns}

if __name__ == "__main__":
    engine = create_engine(SQLITE_DB_PATH)
    Base.metadata.create_all(engine)
