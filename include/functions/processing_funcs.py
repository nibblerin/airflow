import re

def is_file_empty(path: str) -> bool:
    import os
    import pandas as pd

    if os.path.getsize(path) == 0:
        return True

    try:
        return pd.read_csv(path, nrows=1).empty
    except pd.errors.EmptyDataError:
        return True

def replace_nulls(src: str, dst: str) -> None:
    import pandas as pd

    NA_STRINGS = {"null", "NULL", "Null", "None", "none",
                  "nan", "NaN", "N/A", "n/a"}

    df = pd.read_csv(src, dtype=str, keep_default_na=False)
    df = df.replace(r"^\s*$|^N\W?A$", pd.NA, regex=True)
    df = df.mask(df.isin(NA_STRINGS), pd.NA)
    df = df.fillna("-")
    df.to_csv(dst, index=False)

def sort_by_created_date(src: str, dst: str, column: str) -> None:
    import pandas as pd

    df = pd.read_csv(src)
    df["_sort_key"] = pd.to_datetime(df[column], errors="coerce")
    df = df.sort_values("_sort_key").drop(columns="_sort_key")
    df.to_csv(dst, index=False)

def clean_text(text: object) -> str:
    text = str(text)
    if text == "-":
        return "-"
    cleaned = re.sub(r'[^\w\s.,!?;:\'"()\-]', '', text)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned if cleaned else "-" 


def clean_content(src: str, dst: str, column: str) -> None:
    import pandas as pd
    df = pd.read_csv(src, dtype=str, keep_default_na=False)
    df[column] = df[column].apply(clean_text)
    df.to_csv(dst, index=False)