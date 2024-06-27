import rapidminer
import pandas as pd
import os
import time

def conectar_a_rapidminer(rm_home):
    """
    Conecta a RapidMiner Studio y devuelve el conector.
    """
    try:
        start_time = time.time()
        connector = rapidminer.Studio(rm_home, rm_stdout=open(os.devnull, "w"))
        end_time = time.time()
        print(f"Conexión a RapidMiner establecida en {end_time - start_time:.2f} segundos.")
        return connector
    except Exception as e:
        print(f"Error al conectar a RapidMiner: {e}")
        return None

def preparar_datos(data):
    """
    Prepara un DataFrame a partir de un diccionario de datos.
    """
    df = pd.DataFrame(data)
    return df

def guardar_csv(df, file_path):
    """
    Guarda el DataFrame en un archivo CSV.
    """
    start_time = time.time()
    df.to_csv(file_path, index=False)
    end_time = time.time()
    print(f"Archivo CSV guardado en {file_path} en {end_time - start_time:.2f} segundos.")

def ejecutar_proceso(connector, process_path, csv_file_path):
    """
    Ejecuta un proceso de RapidMiner utilizando un archivo CSV como entrada.
    """
    try:
        start_time = time.time()
        scoring_results = connector.run_process(
            process_path,
            inputs={'data': csv_file_path}
        )
        end_time = time.time()
        print(f"Proceso de RapidMiner ejecutado en {end_time - start_time:.2f} segundos.")
        return scoring_results
    except Exception as e:
        print(f"Error al ejecutar el proceso en RapidMiner: {e}")
        return None

def procesar_resultados(scoring_results):
    """
    Procesa los resultados para obtener las probabilidades y el rango correcto.
    """
    start_time = time.time()
    probabilidades = scoring_results[['confidence(1)', 'confidence(2)', 'confidence(3)']].iloc[0].tolist()
    rango_correcto = scoring_results['prediction(TOTAL DE PERSONAS AFECTADAS)'].iloc[0]
    resultado_final = probabilidades + [rango_correcto]
    end_time = time.time()
    print(f"Resultados procesados en {end_time - start_time:.2f} segundos.")
    return resultado_final

# Parámetros y rutas de archivo
rm_home = "C:/Program Files/RapidMiner/RapidMiner Studio"
csv_file_path = "dataToTest.csv"
process_path = "//Local Repository/PAD_Proyecto_Final_Nivel_Afectados/Decision Tree/score"

# Datos de entrada
data = {
    'TOTAL DE INFRAESTRUCTURA AFECTADA': [15],
    'CANTON': [5],
    'EVENTO': [4],
    'CAUSA': [5],
    'CATEGORIA DEL EVENTO': [18],
    'MES': [3],
    'TOTAL DE PERSONAS AFECTADAS': [1]
}

# Conectar a RapidMiner
connector = conectar_a_rapidminer(rm_home)

if connector:
    # Preparar y guardar datos en CSV
    df = preparar_datos(data)
    guardar_csv(df, csv_file_path)

    # Ejecutar proceso en RapidMiner
    scoring_results = ejecutar_proceso(connector, process_path, csv_file_path)

    if scoring_results is not None:
        # Procesar y mostrar resultados
        resultado_final = procesar_resultados(scoring_results)
        print("Probabilidades y rango correcto:", resultado_final)
