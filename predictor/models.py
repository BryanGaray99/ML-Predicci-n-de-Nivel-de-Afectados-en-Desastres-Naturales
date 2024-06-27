# predictor/models.py

import os
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pickle
import rapidminer
import time

# Funciones del modelo de Python
def cargar_datos(file_path):
    df = pd.read_csv(file_path)
    X = df.drop('TOTAL DE PERSONAS AFECTADAS', axis=1)
    y = df['TOTAL DE PERSONAS AFECTADAS']
    return X, y

def entrenar_modelo(X, y, max_depth=4):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
    modelo = DecisionTreeClassifier(criterion="entropy", max_depth=max_depth)
    modelo.fit(X_train, y_train)
    return modelo, X.columns

def guardar_modelo(modelo, columnas, modelo_path):
    with open(modelo_path, 'wb') as archivo_modelo:
        pickle.dump(modelo, archivo_modelo)
    with open(modelo_path.replace('.pkl', '_columns.pkl'), 'wb') as archivo_columnas:
        pickle.dump(columnas, archivo_columnas)

def cargar_modelo(modelo_path):
    with open(modelo_path, 'rb') as archivo_modelo:
        modelo = pickle.load(archivo_modelo)
    with open(modelo_path.replace('.pkl', '_columns.pkl'), 'rb') as archivo_columnas:
        columnas = pickle.load(archivo_columnas)
    return modelo, columnas

def predecir_probabilidades(modelo, datos, columnas_originales):
    datos = datos[columnas_originales]
    probabilidades = modelo.predict_proba(datos)
    predicciones = modelo.predict(datos)
    resultados = []
    for i in range(len(probabilidades)):
        resultado = [float(prob) for prob in probabilidades[i]] + [int(predicciones[i])]
        resultados.append(resultado)
    return resultados

# Entrenar y guardar el modelo si no existe
file_path = './ETL/Dataset/04_Codificacion_Dataset.csv'
modelo_path = 'arbol_modelo.pkl'

if not os.path.exists(modelo_path):
    X, y = cargar_datos(file_path)
    modelo, columnas = entrenar_modelo(X, y)
    guardar_modelo(modelo, columnas, modelo_path)
else:
    modelo, columnas = cargar_modelo(modelo_path)

# Funciones del modelo de RapidMiner
def conectar_a_rapidminer(rm_home):
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
    df = pd.DataFrame(data)
    return df

def guardar_csv(df, file_path):
    start_time = time.time()
    df.to_csv(file_path, index=False)
    end_time = time.time()
    print(f"Archivo CSV guardado en {file_path} en {end_time - start_time:.2f} segundos.")

def ejecutar_proceso(connector, process_path, csv_file_path):
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
    start_time = time.time()
    probabilidades = scoring_results[['confidence(1)', 'confidence(2)', 'confidence(3)']].iloc[0].tolist()
    rango_correcto = scoring_results['prediction(TOTAL DE PERSONAS AFECTADAS)'].iloc[0]
    resultado_final = probabilidades + [rango_correcto]
    end_time = time.time()
    print(f"Resultados procesados en {end_time - start_time:.2f} segundos.")
    return resultado_final
