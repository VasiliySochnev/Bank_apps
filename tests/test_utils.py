import os
from datetime import datetime

import pandas as pd  # type: ignore
import pytest

from config import TEST_DIR
from src.utils import get_data_group_by_card, get_response, get_top_transact, select_data

test_date1 = "2021-12-31 00:00:01"
test_df = pd.read_excel(os.path.join(TEST_DIR, "test_df.xlsx"))
test_df["datetime_col"] = pd.to_datetime(test_df["Дата операции"], dayfirst=True)


def test_get_response(test_date):  # type: ignore
    """Тест приветствия."""
    result = get_response(test_date)
    assert result == "Доброй ночи."


def test_select_data():  # type: ignore
    """Тест выборка по дате."""
    result = select_data(test_df, test_date1)
    assert len(result) == 5


def test_get_data_group_by_card():  # type: ignore
    """Группировка по картам."""
    result = get_data_group_by_card(test_df)
    assert result == [
        {"cashback": 214.11, "last_digits": "*4556", "total_spent": 21411.4},
        {"cashback": 0.07, "last_digits": "*5091", "total_spent": 7.07},
        {"cashback": 14.13, "last_digits": "*7197", "total_spent": 1412.72},
    ]


def test_get_top_transact():  # type: ignore
    result = get_top_transact(test_df)
    assert result == [
        {"date": "2021-12-30", "amount": -20000.0, "category": "Переводы", "description": "Константин Л."},
        {"date": "2021-12-29", "amount": -1411.4, "category": "Ж/д билеты", "description": "РЖД"},
        {"date": "2021-12-29", "amount": -1411.4, "category": "Ж/д билеты", "description": "РЖД"},
        {"date": "2021-12-30", "amount": -7.07, "category": "Каршеринг", "description": "Ситидрайв"},
        {"date": "2021-12-30", "amount": -1.32, "category": "Каршеринг", "description": "Ситидрайв"},
    ]


@pytest.mark.parametrize(  # type: ignore
    "transactions, date, expected_length",
    [
        (
            pd.DataFrame(
                {
                    "datetime_col": [
                        datetime(2023, 6, 1, 0, 0),
                        datetime(2023, 6, 15, 0, 0),
                        datetime(2023, 6, 30, 23, 59, 59),
                        datetime(2023, 7, 1, 0, 0),
                    ],
                    "value": [10, 20, 30, 40],
                }
            ),
            "2023-06-30 23:59:59",
            2,
        ),
        (
            pd.DataFrame(
                {
                    "datetime_col": [
                        datetime(2023, 5, 31, 23, 59, 59),
                        datetime(2023, 6, 1, 0, 0),
                        datetime(2023, 6, 15, 0, 0),
                        datetime(2023, 6, 30, 23, 59, 59),
                    ],
                    "value": [5, 10, 20, 30],
                }
            ),
            "2023-06-15 00:00:00",
            2,
        ),
        (
            pd.DataFrame(
                {
                    "datetime_col": [
                        datetime(2023, 7, 1, 0, 0),
                        datetime(2023, 7, 15, 0, 0),
                        datetime(2023, 7, 30, 23, 59, 59),
                    ],
                    "value": [50, 60, 70],
                }
            ),
            "2023-07-15 00:00:00",
            2,
        ),
        (
            pd.DataFrame(
                {
                    "datetime_col": [
                        datetime(2023, 5, 1, 0, 0),
                        datetime(2023, 5, 15, 0, 0),
                        datetime(2023, 5, 31, 23, 59, 59),
                    ],
                    "value": [15, 25, 35],
                }
            ),
            "2023-05-31 23:59:59",
            2,
        ),
        (
            pd.DataFrame(
                {
                    "datetime_col": [
                        datetime(2023, 6, 15, 0, 0),
                    ],
                    "value": [15],
                }
            ),
            "2023-06-15 00:00:00",
            1,
        ),
    ],
)
def test_select_data_parametrize(transactions, date, expected_length):
    result = select_data(transactions, date)
    assert len(result) == expected_length, f"Expected {expected_length}, but got {len(result)}"
