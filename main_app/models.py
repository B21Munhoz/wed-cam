from datetime import datetime
import secrets
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Unicode, Integer, Boolean, ForeignKey, Table, String
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


guests_at_event = Table('guests_at_event', Base.metadata,
                        Column('events_id', ForeignKey('events.id')),
                        Column('users_id', ForeignKey('users.id'))
                        )


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    photos = relationship("Photo", back_populates="author", )
    guest_at = relationship("Event", secondary="guests_at_event", )
    hosted_events = relationship("Event", back_populates="host", )

    def verify_password(self, password):
        return self.password == password


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    host_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    host = relationship("User", back_populates="hosted_events")
    guests = relationship("User", secondary="guests_at_event",)
    album = relationship("Album", back_populates="event", uselist=False,)

    def __init__(self):
        super(Event, self).__init__()
        self.album = Album()


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    file = Column(Unicode, nullable=False)
    approved = Column(Boolean, default=False)
    album_id = Column(Integer, ForeignKey('albums.id'), nullable=False)
    album = relationship("Album", back_populates="photos")
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship("User", back_populates="photos")


class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    photos = relationship("Photo", back_populates="album",)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship("Event", back_populates="album")
