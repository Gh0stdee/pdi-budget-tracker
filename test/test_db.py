import pytest
from sqlmodel import SQLModel, select

from database_feature.db import Database
from database_feature.models import Category

TEST_DATABASE = "sqlite:///test.db"


@pytest.fixture
def test_db():
    db = Database(TEST_DATABASE)
    yield db
    SQLModel.metadata.drop_all(db.engine)


@pytest.mark.parametrize(
    "category, budget, expected",
    [("pet", 300, [("Pet", 300)]), ("entertainment", 500, [("Entertainment", 500)])],
)
def test_create_category(test_db, category, budget, expected):
    test_db.create_category(category, budget)
    with test_db.get_session() as session:
        result = session.exec(select(Category.category_name, Category.budget)).all()
        assert result == expected


@pytest.mark.parametrize(
    "category1,budget1,category2,budget2,test_category,expected",
    [
        ("pet", 300, "entertainment", 500, "Pet", 1),
        ("pet", 300, "entertainment", 500, "Entertainment", 2),
    ],
)
def test_get_category_id(
    test_db, category1, category2, budget1, budget2, test_category, expected
):
    test_db.create_category(category1, budget1)
    test_db.create_category(category2, budget2)
    assert test_db.get_category_id(test_category) == expected


@pytest.mark.parametrize("category,budget,amount,id", [("transport", 240, 4.5, 1)])
def test_update_used_budget(test_db, category, budget, amount, id):
    test_db.create_category(category, budget)
    with test_db.get_session() as session:
        test_db.update_used_budget(session, amount, id)
        assert session.exec(select(Category.used_budget)).one() == amount


@pytest.mark.parametrize(
    "category, budget, amount, remark, id, expected",
    [
        ("pet", 300, 100, "cheap pet toy", 1, False),
        ("pet", 300, 400, "expensive pet toy", 1, True),
    ],
)
def test_add_transaction_and_check_budget_deficit(
    test_db, category, budget, amount, remark, id, expected
):
    test_db.create_category(category, budget)
    assert (
        test_db.add_transaction_and_check_budget_deficit(amount, remark, id, False)
        == expected
    )


@pytest.mark.parametrize(
    "category1,budget1,category2,budget2,expected",
    [
        ("pet", 300, "entertainment", 500, ["Pet", "Entertainment"]),
        ("food", 2400, "transport", 240, ["Food", "Transport"]),
    ],
)
def test_get_categories(category1, budget1, category2, budget2, expected, test_db):
    test_db.create_category(category1, budget1)
    test_db.create_category(category2, budget2)
    assert test_db.get_categories() == expected


@pytest.mark.parametrize(
    "category, budget, amount1, remark1,amount2,remark2, id",
    [("transport", 240, 4.5, "MTR", 8.1, "Bus", 1)],
)
def test_get_budget_info(
    category, budget, amount1, remark1, amount2, remark2, id, test_db
):
    test_db.create_category(category, budget)
    test_db.add_transaction_and_check_budget_deficit(amount1, remark1, id, False)
    test_db.add_transaction_and_check_budget_deficit(amount2, remark2, id, False)
    with test_db.get_session() as session:
        assert test_db.get_budget_info() == session.exec(select(Category)).all()
