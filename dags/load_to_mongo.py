from pendulum import datetime
from airflow.sdk import dag, task

from include.reviews_config import DATE_COLS, FINAL_FILE, PROCESSED_ASSET, RATING_COL

@dag(
    dag_id="load_to_mongo",
    start_date=datetime(2026, 9, 30),
    schedule=[PROCESSED_ASSET],
    catchup=False,
    tags=["etl", "mongo"],
)
def load_to_mongo():
    @task
    def load(src: str, mongo_db: str, mongo_collection: str) -> int:
        import pandas as pd

        from airflow.providers.mongo.hooks.mongo import MongoHook

        df = pd.read_csv(src)

        # типы нужны для агрегаций: даты -> Date, рейтинг -> число
        for col in DATE_COLS:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        df[RATING_COL] = pd.to_numeric(df[RATING_COL], errors="coerce")

        df = df.astype(object).where(df.notna(), None)
        docs = df.to_dict("records")

        collection = MongoHook(mongo_conn_id="mongo_default").get_conn()[mongo_db][mongo_collection]
        collection.delete_many({})  # идемпотентность: повторный запуск не дублирует данные
        if docs:
            collection.insert_many(docs)
        return len(docs)

    load(
        src=FINAL_FILE,
        mongo_db="{{ var.json.reviews_config.mongo_db }}",
        mongo_collection="{{ var.json.reviews_config.mongo_collection }}",
    )


load_to_mongo()