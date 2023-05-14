import csv
from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

# Загружаем данные в таблицу из csv

table_name = "public.cars2"

def insert_data_py():
    src = PostgresHook(postgres_conn_id='qiberry')
    print("Postgres connect success")
    csv_path = "./dags/used_cars_data_specify_columns.csv"
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if (row[2] != ''):
                print(row)
                src.insert_rows(table=table_name, rows=[row])

def select_data_py():
    import numpy as np

    class brand(object):
        name = ''
        price = np.array([])
        middle_price = 0
        power = np.array([])
        days_on_market = np.array([])
        middle_days_on_market = 0
        has_accidents = np.array([])
        has_accidents_percent = 0

        def __init__(self, name):
            self.name = name

        def calculate_params(self):
            self.middle_price = np.sum(self.price) / self.price.size
            self.middle_days_on_market = np.sum(self.days_on_market) / self.days_on_market.size
            if (self.has_accidents.size != 0):
                self.has_accidents_percent = np.count_nonzero(self.has_accidents == True) / self.has_accidents.size
            else:
                self.has_accidents_percent = 0
            print(self.name, ',', self.middle_price, ',', self.middle_days_on_market, ',', self.has_accidents_percent)

        def add_values_price_power(self, price, power):
            self.price = np.append(self.price, [price])
            self.power = np.append(self.power, [power])

        def add_values_price(self, price):
            self.price = np.append(self.price, [price])

        def add_values_has_accidents(self, has_accidents):
            self.has_accidents = np.append(self.has_accidents, [has_accidents])

        def add_values_days_on_market(self, days_on_market):
            self.days_on_market = np.append(self.days_on_market, [days_on_market])

    total_list = []
    brands_in_list = []

    src = PostgresHook(postgres_conn_id='qiberry')
    src_conn = src.get_conn()
    print("Postgres connect success")
    cursor = src_conn.cursor()
    select_query ="""
    SELECT * FROM """ + table_name
    cursor.execute(select_query)
    for (id, make_name, power, price, daysonmarket, has_accidents) in cursor:
        if str(power) != 'None':
            print('ok data')
            power = float(power[0:power.index(' ')])
            print(power)
            if not make_name in brands_in_list:
                print(make_name)
                total_list.append(brand(make_name))
                brands_in_list.append(make_name)

            total_list[brands_in_list.index(make_name)].add_values_price_power(price, power)

    print('brand , middle_price , middle_days_on_market , has_accidents_percent')
    for x in total_list:
        x.calculate_params()

with DAG(
    dag_id = "hypothesis2",
    start_date = datetime(2021, 12, 1),
    schedule = None,
    catchup = False,
    tags = ['qiberry']
) as dag:
    src = PostgresHook(postgres_conn_id='qiberry')
    src_conn = src.get_conn()

    # Удалить таблицу/таблицы
    delete_table = PostgresOperator(
        task_id="delete_table",
        postgres_conn_id="qiberry",
        sql="""
        DROP TABLE if exists """ + table_name + """
        """
    )

    # Создаем таблицу в БД airflow (схема public)
    create_table = PostgresOperator(
        task_id="create_table",
        #trigger_rule='one_failed',
        postgres_conn_id="qiberry",
        sql="""
        CREATE TABLE IF NOT EXISTS """ + table_name + """ (
            id int,
            make_name varchar,
            power varchar,
            price float,
            daysonmarket float,
            has_accidents bool
        );
        """
    )

    insert_data = PythonOperator(
        task_id='insert_data',
        python_callable=insert_data_py,
        provide_context=True
    )

    select_data = PythonOperator(
        task_id='select_data',
        python_callable=select_data_py,
        provide_context=True
    )


    delete_table >> create_table >> insert_data >> select_data
