import pandas as pd


def load_csv_file(file_path: str):
    return pd.read_csv(file_path)


def load_xls_file(file_path: str):
    return pd.read_excel(file_path, header=None, engine="xlrd")


def load_all_xls_sheets(file_path: str):
    return pd.read_excel(file_path, sheet_name=None, header=None, engine="xlrd")