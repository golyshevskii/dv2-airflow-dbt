from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.py.db_tools.postgresql_tools import load_on_conflict_do_nothing, max_dt

from config import DWH_CONN, PROD_PATH

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
}

with DAG(
    dag_id="raw_dag_customer_product_purchase",
    description="Incremental customer product purchase load",
    tags=["raw"],
    default_args=default_args,
    start_date=datetime(2024, 1, 29),
    schedule_interval="* */1 * * *",
    catchup=False,
) as dag:
    get_max_dt = PythonOperator(
        task_id="get_max_dt",
        python_callable=max_dt,
        op_kwargs={
            "schema": "raw",
            "table": "raw_customer_product_purchase",
            "dt_column": "purchase_dt",
            "conn_str": DWH_CONN,
        },
    )

    with open(
        f"{PROD_PATH}scripts/sql/raw/raw_customer_product_purchase.sql", "r"
    ) as file:
        query = file.read()

    logical_date = "{{ ds }}"

    load_raw = PythonOperator(
        task_id="load_raw",
        python_callable=load_on_conflict_do_nothing,
        op_kwargs={
            "query": query % (logical_date, logical_date),
            "schema": "raw",
            "table": "raw_customer_product_purchase",
            "conn_str": DWH_CONN,
        },
    )

    get_max_dt >> load_raw
