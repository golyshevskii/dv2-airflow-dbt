import logging
from datetime import datetime
from inspect import currentframe

import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert

logger = logging.getLogger(__name__)


def max_dt(
    schema: str, table: str, dt_column: str, conn_str: str, **kwargs
) -> datetime | None:
    """Returns max value of datetime column in the table

    ### Parameters:
    schema (str): schema name
    table (str): table name
    dt_column (str): datetime column name
    conn_str (str): connection string
    """
    frame = currentframe().f_code.co_name

    psql_hook = PostgresHook(conn_str)

    with psql_hook.get_conn() as conn:
        sql = f"SELECT MAX({dt_column}) as max_dt FROM {schema}.{table};"
        max_dt = conn.execute(sql).fetchone()[0]
        logger.info(f"{frame} → Data extracted successfully: max_dt={max_dt}")

    kwargs["ti"].xcom_push(key="max_dt", value=max_dt)

    return max_dt


def insert_on_conflict_nothing(
    table, conn, keys, data_iter, primary_index
) -> int:
    """
    Execute SQL statement inserting data

    ### Parameters
    ----------
    table: pandas.io.sql.SQLTable
    conn: sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
    keys (List[str]): Table column names
    data_iter: Iterable that iterates the values to be inserted
    """
    data = [dict(zip(keys, row)) for row in data_iter]

    sql = (
        insert(table.table)
        .values(data)
        .on_conflict_do_nothing(index_elements=primary_index)
    )
    result = conn.execute(sql)

    return result.rowcount


def load_on_conflict_do_nothing(
    query: str, schema: str, table: str, conn_str: str, **kwargs
) -> None:
    """Loads selected data to the PostgreSQL table

    ### Parameters:
    query (str): SELECT query for data extraction before load
    schema (str): load target schema name
    table (str): load target table name
    conn_str (str): PostgreSQL connection string

    kwargs:
        columns (List[str]): list of columns to select before load
        primary_index (List[str]): primary index columns
    """
    frame = currentframe().f_code.co_name

    engine = create_engine(conn_str)

    data = pd.read_sql(query, engine, columns=kwargs.get("columns"))
    logger.info(f"{frame} → Data extracted successfully: shape{data.shape}")
    if data.empty:
        logger.info(f"{frame} → NO DATA")
        return

    primary_index = kwargs.get("primary_index")
    rows = data.to_sql(
        schema=schema,
        name=table,
        con=engine,
        if_exists="append",
        index=False,
        method=lambda table, conn, keys, data_iter: insert_on_conflict_nothing(
            table, conn, keys, data_iter, primary_index
        ),
    )
    logger.info(f"{frame} → Rows inserted: {rows}")
