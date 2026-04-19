import pandas as pd
import os

def load_csv_file(file_path: str):
    return pd.read_csv(file_path)

def load_xls_file(file_path: str):
    # خليه يختار المحرك (Engine) لوحده بناءً على الامتداد
    ext = os.path.splitext(file_path)[-1].lower()
    engine = "openpyxl" if ext == ".xlsx" else "xlrd"
    return pd.read_excel(file_path, header=None, engine=engine)

def load_all_xls_sheets(file_path: str):
    # خليه يختار المحرك (Engine) لوحده بناءً على الامتداد
    ext = os.path.splitext(file_path)[-1].lower()
    engine = "openpyxl" if ext == ".xlsx" else "xlrd"
    return pd.read_excel(file_path, sheet_name=None, header=None, engine=engine)