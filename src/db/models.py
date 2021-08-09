from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genre_id = Column(Integer, ForeignKey("genre.id"))
    genre = relationship("Genre",back_populates="songs")
    
class Genre(Base):
    __tablename__ = 'genre'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    songs = relationship("Song",back_populates="genre")
