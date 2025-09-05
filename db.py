from decouple import config
from sqlmodel import Session, SQLModel, create_engine

SQLLITE_URL = config("DATABASE")

engine = create_engine(SQLLITE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
