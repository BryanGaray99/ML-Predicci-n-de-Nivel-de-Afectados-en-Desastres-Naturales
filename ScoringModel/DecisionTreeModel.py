import os
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pickle

def cargar_datos(file_path):
    """
    Carga el archivo CSV y define las variables independientes y dependientes.
    """
    df = pd.read_csv(file_path)
    X = df.drop('TOTAL DE PERSONAS AFECTADAS', axis=1)
    y = df['TOTAL DE PERSONAS AFECTADAS']
    return X, y

def entrenar_modelo(X, y, max_depth=4):
    """
    Entrena el modelo de árbol de decisión y devuelve el modelo entrenado.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
    modelo = DecisionTreeClassifier(criterion="entropy", max_depth=max_depth)
    modelo.fit(X_train, y_train)
    return modelo, X.columns

def guardar_modelo(modelo, columnas, modelo_path):
    """
    Guarda el modelo entrenado y los nombres de las columnas en archivos.
    """
    with open(modelo_path, 'wb') as archivo_modelo:
        pickle.dump(modelo, archivo_modelo)
    with open(modelo_path.replace('.pkl', '_columns.pkl'), 'wb') as archivo_columnas:
        pickle.dump(columnas, archivo_columnas)

def cargar_modelo(modelo_path):
    """
    Carga el modelo entrenado y los nombres de las columnas desde archivos.
    """
    with open(modelo_path, 'rb') as archivo_modelo:
        modelo = pickle.load(archivo_modelo)
    with open(modelo_path.replace('.pkl', '_columns.pkl'), 'rb') as archivo_columnas:
        columnas = pickle.load(archivo_columnas)
    return modelo, columnas

def predecir_probabilidades(modelo, datos, columnas_originales):
    """
    Predice las probabilidades y el rango correcto usando el modelo entrenado.
    """
    datos = datos[columnas_originales]
    probabilidades = modelo.predict_proba(datos)
    predicciones = modelo.predict(datos)
    resultados = []
    for i in range(len(probabilidades)):
        resultado = [float(prob) for prob in probabilidades[i]] + [int(predicciones[i])]
        resultados.append(resultado)
    return resultados

# Parámetros y rutas de archivo
file_path = './ETL/Dataset/04_Codificacion_Dataset.csv'
modelo_path = 'arbol_modelo.pkl'

# Entrenar y guardar el modelo si no existe
if not os.path.exists(modelo_path):
    X, y = cargar_datos(file_path)
    modelo, columnas = entrenar_modelo(X, y)
    guardar_modelo(modelo, columnas, modelo_path)
else:
    modelo, columnas = cargar_modelo(modelo_path)

# Ejemplo de uso de la función para predecir
nuevos_datos = pd.DataFrame({
    'TOTAL DE INFRAESTRUCTURA AFECTADA': [15],
    'CANTON': [5],
    'EVENTO': [4],
    'CAUSA': [5],
    'CATEGORIA DEL EVENTO': [18],
    'MES': [3]
})

resultados = predecir_probabilidades(modelo, nuevos_datos, columnas)
print("Probabilidades y rango correcto:", resultados[0])
