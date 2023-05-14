import csv
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

# Загружаем данные в таблицу из csv

def select_rows_py():
    import pandas as pd
    df = pd.read_csv('./dags/used_cars_data.csv')
    new_df = df.filter(['id','make_name','power','price','daysonmarket','has_accidents'], axis=1)
    new_df.to_csv('./dags/used_cars_data_specify_columns.csv')


with DAG(
    dag_id = "select_rows_from_dataset",
    start_date = datetime(2021, 12, 1),
    schedule = None,
    catchup = False,
    tags = ['qiberry']
) as dag:
    src = PostgresHook(postgres_conn_id='qiberry')
    src_conn = src.get_conn()


    select_rows = PythonOperator(
        task_id='select_rows',
        python_callable=select_rows_py,
        provide_context=True
    )

    #insert_data = PythonOperator(
    #    task_id='insert_data',
    #    python_callable=insert_data_py,
    #    provide_context=True
    #)

    select_rows
