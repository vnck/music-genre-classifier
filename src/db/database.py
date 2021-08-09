from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://{user}:{pw}@{container}:5432/{db}'.format(
    user='root',
    pw='secret',
    container='db',
    db='music_db'
    )

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

Base = declarative_base()