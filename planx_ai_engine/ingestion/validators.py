def validate_required_columns(df, required_columns, file_name: str):
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"{file_name} is missing required columns: {missing}")