import os

import pandas as pd  # type: ignore

from config import DATA_DIR

data_file_patch = os.path.join(DATA_DIR, "operations.xlsx")


def get_transaction_from_xlsx_file(path: str) -> pd.DataFrame:
    """Функция, которая извлекает транзакции из файла xlsx"""
    try:
        df = pd.read_excel(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {path} not found")

    not_cancel_op = df.loc[df["Статус"] == "OK"]
    pd.options.mode.chained_assignment = None
    not_cancel_op["datetime_col"] = pd.to_datetime(not_cancel_op["Дата операции"], dayfirst=True)

    not_cancel_op.sort_values(
        ["datetime_col"],
        axis=0,
        ascending=True,
        inplace=False,
        kind="quicksort",
        na_position="last",
        ignore_index=True,
        key=None,
    )
    return not_cancel_op


def get_dataframe() -> pd.DataFrame:
    return get_transaction_from_xlsx_file(data_file_patch)
