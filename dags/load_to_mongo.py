from pendulum import datetime
from airflow.sdk import dag, task

from include.reviews_config import DATE_COLS, FINAL_FILE, PROCESSED_ASSET, RATING_COL

@dag(
    dag_id="load_to_mongo",
    start_date=datetime(2026, 9, 30),
    schedule=[PROCESSED_ASSET],
    catchup=False,
    tags=["mongo"],
)
# i tried to apply single responsibility for functions so that each step has its own function as it is in the first dag
# but it decreses performance DRASTICALLY (30 seconds against 1.5 min), so everything is in one task
def load_to_mongo():
    @task
    def load(src: str, mongo_db: str, mongo_collection: str) -> None:
        import pandas as pd

        from airflow.providers.mongo.hooks.mongo import MongoHook

        df = pd.read_csv(src, keep_default_na=False)

        for col in DATE_COLS:
            df[col] = pd.to_datetime(df[col], errors="coerce")
        df[RATING_COL] = pd.to_numeric(df[RATING_COL], errors="coerce")

        df = df.astype(object).where(df.notna(), "-")
        docs = df.to_dict("records")

        hook = MongoHook(mongo_conn_id="mongo_default")
        with hook.get_conn() as client:
            db = client[mongo_db]
            staging = db[f"{mongo_collection}_staging"]
            staging.drop()
            staging.insert_many(docs)
            staging.rename(mongo_collection, dropTarget=True)
    load(
        src=FINAL_FILE,
        mongo_db="{{ var.json.reviews_config.mongo_db }}",
        mongo_collection="{{ var.json.reviews_config.mongo_collection }}",
    )


load_to_mongo()