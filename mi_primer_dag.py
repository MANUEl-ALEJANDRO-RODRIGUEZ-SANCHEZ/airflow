from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import requests

# Funcion para descargar un CSV de ejemplo
def descargar_csv():
    url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    response = requests.get(url)
    with open("/tmp/iris.csv", "wb") as f:
        f.write(response.content)
    print("Archivo descargado!")

# Funcion para calcular el promedio de una columna
def calcular_promedio():
    data = pd.read_csv("/tmp/iris.csv")
    promedio_sepal_length = data["sepal_length"].mean()
    with open("/tmp/promedio_sepal_length.txt", "w") as f:
        f.write(f"Promedio sepal_length: {promedio_sepal_length}")
    print(f"Promedio calculado: {promedio_sepal_length}")

# Definir el DAG
dag = DAG(
    'procesar_iris',
    default_args={
        'retries': 2,
        'retry_delay': timedelta(minutes=1),
    },
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
)

# Tareas
tarea_descargar = PythonOperator(
    task_id='descargar_csv',
    python_callable=descargar_csv,
    dag=dag,
)

tarea_promedio = PythonOperator(
    task_id='calcular_promedio',
    python_callable=calcular_promedio,
    dag=dag,
)

# Orden de ejecucion
tarea_descargar >> tarea_promedio