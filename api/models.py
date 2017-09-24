from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Numeric

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String())
    phone_number = Column(Integer)
    company = Column(String(50))
    address = Column(String(50))
    street_address = Column(String(50))
    unit_number = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    zip_code = Column(String(50))
    country = Column(String(50))
    notes = Column(String(50))

    def as_dict(self):
        return {c.name: getattr(self, c.name)
                for c in self.__table__.columns}

engine = create_engine('sqlite:///test_app.db')
Base.metadata.create_all(engine)
