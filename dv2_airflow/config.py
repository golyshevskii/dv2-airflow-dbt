import os

LOCAL_PATH = "/Users/python_poseur/dv2-adbt-dev/dv2-airflow-dbt/dv2_airflow"
PROD_PATH = "/opt/airflow/dags/"

# DBT
DBT_PROJECT_DIR = "/opt/airflow/dags/dv2_dbt"
DBT_PROFILES_DIR = "/opt/airflow/dags/dv2_dbt/.dbt"
DBT_PROFILE = "dv2_dbt"

# POSTGRESQL
DWH_CONN = os.environ["AIRFLOW_VAR_DWH_CONN"]
