import os
import sys
sys.path.append('src')
os.chdir('src')
print(os.getcwd())

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from ..src.api.main import app, get_db
from ..src.db.database import Base

class TestAPIMethods(unittest.TestCase):

    engine = create_engine('sqlite:///./test.db')
    TestingSession = sessionmaker(bind=engine)

    def override_get_db(self):
        db = self.TestingSession()
        try:
            yield db
        finally:
            db.close()

    def setUp(self):
        app.dependency_overrides[get_db] = self.override_get_db
        Base.metadata.create_all(bind=self.engine)
        self.client = TestClient(app)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_get_songs_empty(self):
        """query which yields empty results"""
        response = self.client.get('/songs')
        self.assertEqual(response.status_code,200,response.content)
        self.assertEqual(len(response.json()),0,response.json())

    def test_get_genre(self):
        """query which yields empty results"""
        response = self.client.get('/genres')
        self.assertEqual(response.status_code,200,response.content)
        self.assertEqual(len(response.json()),0,response.json())

    def test_add_songs(self):
        """query to add 10 entries to the database results"""
        with open('test/test10.csv','rb') as f:
            response = self.client.post('/add/songs', files={'file':('test10.csv',f,'text/csv')})
        self.assertEqual(response.status_code,200,response.content)
        response = self.client.get('/songs')
        self.assertEqual(response.status_code,200,response.content)
        self.assertEqual(len(response.json()),10,response.json())

if __name__ == "__main__":
    unittest.main()
