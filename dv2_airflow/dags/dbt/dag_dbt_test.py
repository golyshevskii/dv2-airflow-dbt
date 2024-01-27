from datetime import datetime

from airflow import DAG
from airflow_dbt_python.operators.dbt import DbtRunOperator
from config import DBT_PROFILE, DBT_PROFILES_DIR, DBT_PROJECT_DIR

default_args = {"owner": "airflow", "depends_on_past": False, "task_concurrency": 1}

with DAG(
    dag_id="dbt_dag_test",
    description="Run dbt model",
    tags=["dbt"],
    default_args=default_args,
    start_date=datetime(2023, 10, 10),
    schedule_interval=None,
    catchup=False,
) as dag:
    dbt_run_test = DbtRunOperator(
        task_id="dbt_run_test",
        profiles_dir=DBT_PROFILES_DIR,
        project_dir=DBT_PROJECT_DIR,
        profile=DBT_PROFILE,
        target="datamarts",
        models=["raw_test"],
        full_refresh=True,
    )

    dbt_run_test