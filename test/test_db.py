import pytest
from sqlmodel import SQLModel, create_engine, select

from database_feature.db import (
    add_transaction_and_check_budget_deficit,
    create_category,
    get_budget_info,
    get_categories,
    get_category_id,
    get_session,
    init_db,
    update_used_budget,
)
from database_feature.models import Category

TEST_DATABASE = "sqlite:///test.db"


@pytest.fixture
def create_test_engine():
    engine = create_engine(TEST_DATABASE, echo=False)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.mark.parametrize(
    "category, budget, expected",
    [("pet", 300, [("Pet", 300)]), ("entertainment", 500, [("Entertainment", 500)])],
)
def test_create_category(create_test_engine, category, budget, expected):
    init_db(create_test_engine)
    create_category(category, budget, create_test_engine)
    with get_session(create_test_engine) as session:
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
    create_test_engine, category1, category2, budget1, budget2, test_category, expected
):
    init_db(create_test_engine)
    create_category(category1, budget1, create_test_engine)
    create_category(category2, budget2, create_test_engine)
    assert get_category_id(test_category, create_test_engine) == expected


@pytest.mark.parametrize("category,budget,amount,id", [("transport", 240, 4.5, 1)])
def test_update_used_budget(create_test_engine, category, budget, amount, id):
    init_db(create_test_engine)
    create_category(category, budget, create_test_engine)
    with get_session(create_test_engine) as session:
        update_used_budget(session, amount, id)
        assert session.exec(select(Category.used_budget)).one() == amount


@pytest.mark.parametrize(
    "category, budget, amount, remark, id, expected",
    [
        ("pet", 300, 100, "cheap pet toy", 1, False),
        ("pet", 300, 400, "expensive pet toy", 1, True),
    ],
)
def test_add_transaction_and_check_budget_deficit(
    create_test_engine, category, budget, amount, remark, id, expected
):
    init_db(create_test_engine)
    create_category(category, budget, create_test_engine)
    assert (
        add_transaction_and_check_budget_deficit(
            amount, remark, id, engine=create_test_engine
        )
        == expected
    )


@pytest.mark.parametrize(
    "category1,budget1,category2,budget2,expected",
    [
        ("pet", 300, "entertainment", 500, ["Pet", "Entertainment"]),
        ("food", 2400, "transport", 240, ["Food", "Transport"]),
    ],
)
def test_get_categories(
    category1, budget1, category2, budget2, expected, create_test_engine
):
    init_db(create_test_engine)
    create_category(category1, budget1, create_test_engine)
    create_category(category2, budget2, create_test_engine)
    assert get_categories(create_test_engine) == expected


@pytest.mark.parametrize(
    "category, budget, amount1, remark1,amount2,remark2, id",
    [("transport", 240, 4.5, "MTR", 8.1, "Bus", 1)],
)
def test_get_budget_info(
    category, budget, amount1, remark1, amount2, remark2, id, create_test_engine
):
    init_db(create_test_engine)
    create_category(category, budget, create_test_engine)
    add_transaction_and_check_budget_deficit(
        amount1, remark1, id, engine=create_test_engine
    )
    add_transaction_and_check_budget_deficit(
        amount2, remark2, id, engine=create_test_engine
    )
    with get_session(create_test_engine) as session:
        assert (
            get_budget_info(create_test_engine) == session.exec(select(Category)).all()
        )
