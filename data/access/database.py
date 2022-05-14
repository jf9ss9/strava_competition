from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://postgres:Skaterboy14@localhost:5432/strava_db")
Session = sessionmaker(bind=engine)
session = Session()
