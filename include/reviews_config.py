import os

from airflow.sdk import Asset

DATA_DIR = os.environ.get("REVIEWS_DATA_DIR", "/usr/local/airflow/include/data")
RAW_DIR = f"{DATA_DIR}/raw"
PROCESSED_DIR = f"{DATA_DIR}/processed"

RAW_FILE = f"{RAW_DIR}/reviews.csv"
STEP1_FILE = f"{PROCESSED_DIR}/step1_no_nulls.csv"
STEP2_FILE = f"{PROCESSED_DIR}/step2_sorted.csv"
FINAL_FILE = f"{PROCESSED_DIR}/processed_reviews.csv"
EMPTY_LOG = f"{PROCESSED_DIR}/empty_file.log"

CREATED_COL = "at"
CONTENT_COL = "content"
RATING_COL = "score"
DATE_COLS = ["at", "repliedAt"]

PROCESSED_ASSET = Asset(name="processed_reviews", uri=f"file://{FINAL_FILE}")