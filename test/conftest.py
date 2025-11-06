from fastapi.testclient import TestClient 
import pytest
from app.main import app
from app import schemas
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from app.database import get_db
from app.database import Base

load_dotenv()

SQLALCHEMY_DATABASE_URL=os.getenv('DATABASE_CONNECTION_URI')

engine=create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)




Client=TestClient(app)

# --- Fixture to setup tables once per test session ---
@pytest.fixture()
def session():
    # Create tables at start of test session
     Base.metadata.drop_all(bind=engine)
     Base.metadata.create_all(bind=engine)
     db=TestingSessionLocal()
     try:
         yield db
     finally:
         db.close()
     
    # Drop tables at end of test session
   


# Fixture for client (optional)
@pytest.fixture()
def client(session):
    
    def override_get_db(): #make a session to the database and close it once we are done
        db=TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db       
    yield TestClient(app)
