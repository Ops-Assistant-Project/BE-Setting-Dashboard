from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from db.mongodb import connect_to_mongo
from airflow.sync_setting_computers import sync_setting_computers


def send_reminder_task():
    connect_to_mongo()
    sync_setting_computers()

with DAG(
    dag_id="sync_setting_dashboard",
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/15 * * * *",
    catchup=False,
    tags=["setting"],
) as dag:

    send_reminder = PythonOperator(
        task_id="sync_setting_dashboard",
        python_callable=send_reminder_task,
    )