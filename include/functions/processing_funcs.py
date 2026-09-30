def is_file_empty(path: str) -> bool:
    import os

    import pandas as pd

    try:
        return os.path.getsize(path) == 0 or pd.read_csv(path).empty
    except pd.errors.EmptyDataError:
        return True

def replace_nulls(src: str, dst: str) -> None:
    import pandas as pd

    df = pd.read_csv(src)
    df = df.replace("null", pd.NA).fillna("-")
    df.to_csv(dst, index=False)

def sort_by_created_date(src: str, dst: str, column: str) -> None:
    import pandas as pd

    df = pd.read_csv(src)
    df["_sort_key"] = pd.to_datetime(df[column], errors="coerce")
    df = df.sort_values("_sort_key").drop(columns="_sort_key")
    df.to_csv(dst, index=False)

def clean_text(text: object) -> str:
    import re
    text = re.sub(r"[^\w\s.,!?;:'\"()\-]", "", str(text))
    return re.sub(r"\s+", " ", text).strip()

def clean_content(src: str, dst: str, column: str) -> None:
    import pandas as pd

    df = pd.read_csv(src)
    df[column] = df[column].apply(clean_text)
    df.to_csv(dst, index=False)

