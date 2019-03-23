import json
from datetime import timedelta

import airflow
from airflow.hooks.http_hook import HttpHook
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

args = {
    'owner': 'airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id='python',
    default_args=args,
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=5),
)


headers = {
    'Content-Type': "application/json;charset=UTF-8",
    'X-Appearin-Device-Platform': "web",
    'Authorization': "Basic MTUzNTMyYmQtNmNiYi00OTM2LTliZTctMzY0MDc0ZGNkYjcyOmY1MDRkN2VkYTc1MmIxNDBkNjNiOGRjNTM5N2FiNjVhMGQwYTkzYWUzOWJiOTEwNmZlZjcwZTViNDk2OTZhNDM=",
}


def log(*args, **kwargs):
    connection = HttpHook(http_conn_id='appear_in')
    data = json.dumps({
        "displayName": "TyVikMail",
        "email": {"value": "tyvik@mail.ru", "verificationCode": "123455"}
    })
    result = connection.run(endpoint='/organizations/1/users', data=data, headers=headers)
    print(result)


login = PythonOperator(
    task_id='login',
    python_callable=log,
    provide_context=True,
    dag=dag,
)


if __name__ == "__main__":
    dag.cli()
