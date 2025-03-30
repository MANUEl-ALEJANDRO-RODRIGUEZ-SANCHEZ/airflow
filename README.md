# **AirFlow**

## **¿QUE ES APACHE AIRFLOW?**

Apache Airflow es una plataforma de código abierto para la automatización, programación y monitoreo de flujos de trabajo (workflows) en proyectos de datos. Permite crear y gestionar tareas complejas mediante la creación de DAGS (grafos acíclicos dirigidos), lo que facilita la ejecución secuencial o paralela de procesos. Airflow es ideal para coordinar tareas en pipelines de datos, como la extracción, transformación y carga (ETL), y es muy utilizado en entornos de big data y ciencia de datos.

---

## **Ejemplo de uso**

Para ejecutar Apache AirFlow en mi caso en Windows, lo hare con la ayuda de Docker y una vez corriendo AirFlow se usa un programa en python para calcular el promedio de una columna de un dataset .csv


### **Instalacion de Docker**

Como primer paso debemos instalar [Docker desktop](https://www.docker.com/products/docker-desktop/), elijo esta version ya que esta ya cuenta con otras versiones de docker instaladas que seran de suma importancia como docker compose


### **Descargar archivo docker-compose.yaml**

Una vez descargado e instalado docker desktop, debemos crear una carpeta donde tendremos nuestro proyecto
Ahora en la terminal de la carpeta recien creada escribimos el siguiente comando para descargar el archivo docker-compose.yaml

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml'
```


### **Cambio de variable de entorno**

Abrimos el archivo recien descargado y cambiamos el valor de la variable de entorno AIRFLOW__CORE__EXECUTOR a LocalExecutor

```env
AIRFLOW__CORE__EXECUTOR: LocalExecutor
```


### **Puertos**

Ahora en el mismo archivo docker-compose en la linea 118 veremos un bloque de codigo similar o identico a este:

```yaml
  airflow-webserver:
    <<: *airflow-common
    command: webserver
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
```

Debemos cuidar que no tengamos ningun servicio corriendo en este puerto, si es asi debemos cambiar de puerto


### **Creación de carpertas**

En la carpeta de nuestro proyecto debemos crear 4 carpetas con los siguientes nombres:

```bash
New-Item -ItemType Directory -Path dags, logs, plugins, config
```


### **Iniciación del archivo docker-compose**

Ahora ejecutamos los siguientes comandos:

```bash
docker compose up airflow-init
```

```bash
docker compose up
```


### **Programa en python**

Ahora escribimos el siguiente programa en python y el archivo lo guardamos en la carpeta dags que creamos

```python
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
```


### **Abrir AirFlow**

Ahora abrimos el navegador y nos dirijimos a [localhost:8080](localhost:8080) o al puerto que se haya definido

![image](https://github.com/user-attachments/assets/f9a78d40-42b5-4a10-a9d5-df87db48e4a8)

El usuario y contraseña en airflow

Una vez dentro, buscamos a procesar_iris y lo ejecutamos

![image](https://github.com/user-attachments/assets/63abe90d-fae9-4a4e-ac70-aad1c39c24f2)

Esto lo que hara es ejecutar el programa de python, el resultado se guarda en el sistema de archivos del contenedor, por lo que debemos ejecutar el siguiente comando para visualizar el archivo resultante

```bash
docker exec -it <ID_CONTENEDOR> bash
```

```bash
cat /tmp/promedio_sepal_length.txt
```

![image](https://github.com/user-attachments/assets/e995b664-0611-473d-91dd-b8385a3537a9)
