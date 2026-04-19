import math


def clean_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return str(value).strip()


def clean_int(value) -> int:
    text = clean_text(value)
    if text == "":
        return 0
    return int(float(text))


def clean_bool(value) -> bool:
    text = clean_text(value).lower()
    return text in {"1", "true", "yes", "y"}


def clean_optional_text(value):
    text = clean_text(value)
    return text if text != "" else None


def clean_float_or_none(value):
    text = clean_text(value)
    if text == "":
        return None
    return float(text)