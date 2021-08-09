from typing import List, Optional
from pydantic import BaseModel

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):

    class Config:
        orm_mode = True

class SongBase(BaseModel):
    title: str

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: int
    genre: Genre

    class Config:
        orm_mode = True