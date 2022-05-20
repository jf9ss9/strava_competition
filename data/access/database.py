from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:Skaterboy14@localhost:5432/strava_db")
_Session = sessionmaker(bind=engine)
session = _Session()
