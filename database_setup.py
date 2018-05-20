from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String(255), nullable=False)
    picture = Column(String)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    picture = Column(String)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'picture': self.picture
        }


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    creationtime = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)
    picture = Column(String)

    @property
    def serialize(self):
        return {
            'title': self.name,
            'description': self.description,
            'pic_url': self.picture
        }


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
