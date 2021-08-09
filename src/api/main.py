import yaml
from io import StringIO
from typing import List
from pydantic import BaseModel

from fastapi import Depends, FastAPI, File, UploadFile, HTTPException
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import Session, engine

import pandas as pd

from classifier import Classifier
from generate_features import FeatureTransformer

app = FastAPI()

# load model
with open('../../configs/configs.yaml', "r") as f:
    configs = yaml.load(f, Loader=yaml.CLoader)

model_configs = configs['model']
feature_configs = configs['features']

classifier = Classifier(model_configs)
featureTransformer = FeatureTransformer(feature_configs)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.get("/genres", response_model=List[str],
    summary="Get all genre names.")
def get_genres(db: Session = Depends(get_db)):
    """Get the names of all the genres."""
    genres = crud.get_genres(db)
    return [g.name for g in genres]

@app.get("/songs", response_model=List[str],
    summary="Get all song titles..")
def get_songs(db: Session = Depends(get_db)):
    """Get the titles of all the songs."""
    songs = crud.get_songs(db)
    return [song.title for song in songs]

@app.get("/songs/{genre}", response_model=List[str],
    summary="Get all song titles from a genre.")
def get_titles(genre: str,db: Session = Depends(get_db)):
    """Get the titles of all the songs that belong to the same genre.
    
    - **genre**: a string specifying the genre to match songs.
    """
    genres = crud.get_genres(db)
    if genre not in [g.name for g in genres]:
        raise HTTPException(status_code=404, detail="Genre not found.")
    songs = crud.get_songs(db, genre)
    return [song.title for song in songs]

@app.post("/add/songs", response_model=List[schemas.Song],
    summary="Adds a song item.")
def classify(file: UploadFile = File(...),db: Session = Depends(get_db)):
    """Adds a song item and classifies the song to a genre.
    
    - *file**: a csv file containing the song title and features.

    Creates a song item with the following information:
    - **id** : track id of the song.
    - **title** : title of the song.
    - **genre** : genre of the song.
    """
    df = pd.read_csv(StringIO(str(file.file.read(),'utf-8')),encoding='utf-8')
    songs = []
    features = featureTransformer.transform(df)
    predicted_genres = classifier.predict(features,labels=True)
    df['genre'] = predicted_genres
    genres = [g.name for g in crud.get_genres(db)]
    for _,row in df.iterrows():
        if not crud.get_song_by_id(db, row['trackID']):
            genre_name = row['genre']
            if genre_name not in genres:
                print('adding new genre:', genre_name)
                genre = {'name': genre_name}
                genre = crud.create_genre(db,genre)
                genres = [g.name for g in crud.get_genres(db)]
            else:
                genre = crud.get_genre(db,genre_name)
            song = {'id': row['trackID'], 'title': row['title'], 'genre':genre}
            songs.append(crud.create_song(db,song))
        else:
            songs.append(crud.get_song_by_id(db, row['trackID']))
    return songs

@app.post('/add/genre', response_model=schemas.Genre,
    summary="Adds a genre.",
    description="Adds a genre.")
def add_genre(genre: schemas.Genre, db: Session=Depends(get_db)):
    return crud.create_genre(db, genre)

@app.get('/song/track/{id}', response_model=schemas.Song,
    summary="Get a song by its trackID.")
def add_genre(id: int, db: Session=Depends(get_db)):
    return crud.get_song_by_id(db, id)

if __name__ == '__main__':
    models.Base.metadata.create_all(bind=engine)