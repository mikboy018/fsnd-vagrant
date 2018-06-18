from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

""" Setup Users table, no serialization option, to protect users."""
class Users(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    admin = Column(Boolean(False), nullable = False)

""" Setup Categories table """
class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship(Users)

    """ Serialize table """
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
        }

""" Setup Items table """
class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    description = Column(String(250), nullable = False)
    category_id = Column(Integer, ForeignKey('Categories.id'))
    owner_id = Column(Integer, ForeignKey('Users.id'))
    category = relationship(Categories)
    owners = relationship(Users)

    """ Serialize table """
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

engine = create_engine('sqlite:///restaurantmenuwithusers.db')

Base.metadata.create_all(engine)