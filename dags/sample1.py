import json
from datetime import timedelta

import airflow
from airflow.hooks.http_hook import HttpHook
from airflow.models import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.python_operator import PythonOperator

from dags.sensors.gmail import GmailSensor

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id='sample1',
    default_args=args,
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=5),
)


headers_code = {
    'Content-Type': "application/json;charset=UTF-8",
    'X-Appearin-Device-Platform': "web",
    'Authorization': "Basic MTUzNTMyYmQtNmNiYi00OTM2LTliZTctMzY0MDc0ZGNkYjcyOmY1MDRkN2VkYTc1MmIxNDBkNjNiOGRjNTM5N2FiNjVhMGQwYTkzYWUzOWJiOTEwNmZlZjcwZTViNDk2OTZhNDM=",
}


check_mark = SimpleHttpOperator(
    http_conn_id='appear_in',
    task_id='receive_code',
    endpoint='/device/link-tokens',
    method='POST',
    data=json.dumps({"email": "tyvik@mail.ru"}),
    headers=headers_code,
    response_check=lambda response: response.status_code == 200,
    xcom_push=True,
    dag=dag,
)

wait_for_email = GmailSensor(dag=dag, task_id='wait_for')


def log(*args, **kwargs):
    connection = HttpHook(http_conn_id='appear_in')
    code = kwargs['task_instance'].xcom_pull(task_ids='wait_for', key='code')
    data = json.dumps({"email": "tyvik@mail.ru", "code": code})
    print(data)
    result = connection.run(endpoint='/device/id-tokens', data=data, headers=headers_code)
    print(result)
    print(result.headers)
    response = result.json()
    print(response)
    result = connection.run(endpoint='/organizations/1/device/links', data=json.dumps(response), headers=headers_code)
    print(result)
    connection.method = 'GET'
    result = connection.run(endpoint='/user?fields=permissions', headers=headers_code)
    print(result.json())


login = PythonOperator(
    task_id='login',
    python_callable=log,
    provide_context=True,
    dag=dag,
)

check_mark >> wait_for_email >> login

if __name__ == "__main__":
    dag.cli()
