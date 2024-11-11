from sqlalchemy import create_engine, MetaData
from databases import Database

DATABASE_URL = "sqlite:///./expenses.db"

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)
