from sqlalchemy.orm import Session
from . import models, schemas

def get_genres(db: Session):
    """get all genres in the db."""
    return db.query(models.Genre).all()

def get_genre(db: Session, name: str):
    """get a genre from the db that matches the name."""
    return db.query(models.Genre).filter(models.Genre.name == name).first()

def get_genre_names(db: Session):
    """get all genre names from the db"""
    return db.query(models.Genre.name).all()

def get_songs(db: Session, genre: str = None):
    """get songs that matches a genre from the db. If no genre is provided, gets all songs in the db.
    """
    if genre == None:
        return db.query(models.Song.title).all()
    else:
        return db.query(models.Song.title).join(models.Genre).filter(models.Genre.name == genre).all()

def get_song_by_id(db: Session, id: int):
    """get a song by its id."""
    return db.query(models.Song).filter(models.Song.id==id).first()

def create_song(db: Session, song: schemas.SongCreate):
    """adds a song to the db."""
    db_song = models.Song(id=song['id'], title=song['title'], genre=song['genre'])
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

def create_genre(db: Session, genre: schemas.GenreCreate):
    """adds a genre to the db."""
    db_genre = models.Genre(name=genre['name'])
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

