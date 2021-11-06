from datetime import datetime
import secrets
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Unicode, Integer, Boolean, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=False)
    password = Column(Unicode, nullable=False)
    token = Column(Unicode, nullable=False)
    name = Column(Unicode, nullable=False)
    hosted_events = relationship("Event", back_populates="host",)
    guest_at = relationship("Event", back_populates="guests",)
    photos = relationship("Photo", back_populates="author",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_joined = datetime.now()
        self.token = secrets.token_urlsafe(64)


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    host_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    host = relationship("User", back_populates="hosted_events")
    guests = relationship("User", back_populates="guest_at",)
    album = relationship("Album", back_populates="event", uselist=False,)

    def __init__(self):
        super(Event, self).__init__()
        self.album = Album()


class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    file = Column(Unicode, nullable=False)
    approved = Column(Boolean, default=False)
    album_id = Column(Integer, ForeignKey('album.id'), nullable=False)
    album = relationship("Album", back_populates="photos")
    author = relationship("User", back_populates="photos")


class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    photos = relationship("Photo", back_populates="album",)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    event = relationship("Event", back_populates="album")
