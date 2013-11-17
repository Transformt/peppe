from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('postgresql+psycopg2://trans:transformer@localhost/mydatabase', convert_unicode=True, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  import models
  Base.metadata.create_all(bind=engine)
  
