# app/database/base.py
from sqlalchemy.orm import declarative_base

# Base declarativa do SQLAlchemy — todos os modelos herdarão dela
Base = declarative_base()
