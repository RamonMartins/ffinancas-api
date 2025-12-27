# app/database/base.py

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """ Classe pai de todos os models. Centraliza o metadata """
    pass
