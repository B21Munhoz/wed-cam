import secrets
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, Unicode, Integer, Boolean, ForeignKey, Table, String
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Verificação de autorização por Token
def check_auth(request):
    token = request.headers.get('Authorization', 'Token')[6:]
    session = request.db
    if token:
        user = session.query(User).filter(User.token == token).first()
        if user:
            return user
    return None


# Tabela auxiliar para relação Many-to-Many de Convidados e Eventos
guests_at_event = Table('guests_at_event', Base.metadata,
                        Column('events_id', ForeignKey('events.id')),
                        Column('users_id', ForeignKey('users.id'))
                        )


# Usuário
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    photos = relationship("Photo", back_populates="author", )
    guest_at = relationship("Event", secondary="guests_at_event", back_populates="guests")
    hosted_events = relationship("Event", back_populates="host", )
    token = Column(Unicode)

    def verify_password(self, password):
        return self.password == password

    def generate_token(self):
        self.token = secrets.token_urlsafe(64)
        return self.token

    def clear_token(self):
        self.token = None


# Evento. A temática é casamento mas pode ser qualquer outro evento
class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode, nullable=False)
    invitation = Column(Unicode, nullable=False)
    host_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    host = relationship("User", back_populates="hosted_events")
    guests = relationship("User", secondary="guests_at_event", back_populates="guest_at")
    album = relationship("Album", back_populates="event", uselist=False,)
    started = Column(Boolean, default=False)

    def __init__(self):
        super(Event, self).__init__()
        self.album = Album()
        self.invitation = secrets.token_urlsafe(12)

    def add_guest(self, guest):
        self.guests.append(guest)

    def open_close_event(self):
        self.started = not self.started


# Armazenamento das informações importantes da imagem
class Photo(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    file = Column(Unicode, nullable=False)
    url = Column(Unicode, nullable=False)
    approved = Column(Boolean, default=False)
    album_id = Column(Integer, ForeignKey('albums.id'), nullable=False)
    album = relationship("Album", back_populates="photos")
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship("User", back_populates="photos")

    def approve_disapprove(self):
        self.approved = not self.approved


# Album de imagens. Se necessário, o sistema pode ser expandido para suportar
# vários albums em um evento/casamento.
class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    photos = relationship("Photo", back_populates="album",)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    event = relationship("Event", back_populates="album")
