import pytest
from sqlmodel import SQLModel, create_engine, select

from database_feature.db import create_category, get_session, init_db
from database_feature.models import Category

TEST_DATABASE = "sqlite:///test.db"


@pytest.fixture
def create_test_engine():
    engine = create_engine(TEST_DATABASE, echo=False)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.mark.parametrize(
    "arg1, arg2, expected",
    [("pet", 300, [("pet", 300)]), ("entertainment", 500, [("entertainment", 500)])],
)
def test_create_category(create_test_engine, arg1, arg2, expected):
    init_db(create_test_engine)
    create_category(arg1, arg2, create_test_engine)
    with get_session(create_test_engine) as session:
        result = session.exec(select(Category.category_name, Category.budget)).all()
        assert result == expected
