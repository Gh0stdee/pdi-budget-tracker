from sqlmodel import Session, SQLModel, create_engine

SQLLITE_URL = "sqlite:///database.db"

engine = create_engine(SQLLITE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
