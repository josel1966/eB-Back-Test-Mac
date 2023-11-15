import os
#from decouple import config
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# # Carga de variables de entorno en un ambiente de MacOS local
# load_dotenv()
# DATABASE_URL = os.environ.get("CONNECTION_URL")

# Carga de variables de entorno en un ambiente de MacOS a través de un contenedor Docker
load_dotenv()
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")

DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

#------------------------------------------------------------------------------------------

# # Carga de variables de entorno en un ambiente de Windows
# DATABASE_URL = config("CONNECTION_URL")

#------------------------------------------------------------------------------------------

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base = declarative_base()
