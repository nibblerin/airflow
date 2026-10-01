from pendulum import datetime

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.sdk import TaskGroup, dag, task
from include.functions import processing_funcs as f

from include.reviews_config import (
    CONTENT_COL,
    CREATED_COL,
    EMPTY_LOG,
    FINAL_FILE,
    PROCESSED_ASSET,
    RAW_FILE,
    STEP1_FILE,
    STEP2_FILE,
)

@dag(
    dag_id="process_reviews",
    start_date=datetime(2026, 9, 30),
    schedule="@daily",
    catchup=False,
    tags=["process"],
)
def process_reviews():
    wait_for_file = FileSensor(
        task_id="wait_for_file",
        fs_conn_id="fs_default",
        filepath=RAW_FILE,
        poke_interval=30,
        timeout=60 * 60,
        mode="reschedule",
    )

    @task.branch
    def check_file_empty(raw_file: str) -> str:
        if f.is_file_empty(raw_file):
            return "log_empty_file"
        return "processing.replace_nulls"

    log_empty_file = BashOperator(
        task_id="log_empty_file",
        bash_command=f'echo "$(date) - File {RAW_FILE} is empty" | tee -a {EMPTY_LOG}',
    )

    with TaskGroup("processing") as processing:
        replace_nulls = task(f.replace_nulls)
        sort_by_created_date = task(f.sort_by_created_date)
        clean_content = task(f.clean_content, outlets=[PROCESSED_ASSET])

        (
            replace_nulls(RAW_FILE, STEP1_FILE)
            >> sort_by_created_date(STEP1_FILE, STEP2_FILE, CREATED_COL)
            >> clean_content(STEP2_FILE, FINAL_FILE, CONTENT_COL)
        )

    wait_for_file >> check_file_empty(RAW_FILE) >> [log_empty_file, processing]

process_reviews()