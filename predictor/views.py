# predictor/views.py

from django.shortcuts import render
from django.http import JsonResponse
import json
import pandas as pd
from .models import (
    cargar_modelo_python, 
    predecir_probabilidades_python, 
    conectar_a_rapidminer, 
    preparar_datos_rapidminer, 
    guardar_csv_rapidminer, 
    ejecutar_proceso_rapidminer, 
    procesar_resultados_rapidminer
)
from .utils import cargar_diccionarios

# Cargar el modelo de Python una vez al iniciar
modelo_path = './ScoringModel/arbol_modelo.pkl'
modelo_python, columnas_python = cargar_modelo_python(modelo_path)

# Cargar diccionarios de datos
cantones, categorias, causas, eventos = cargar_diccionarios()

def index(request):
    context = {
        'cantones': cantones,
        'categorias': categorias,
        'causas': causas,
        'eventos': eventos
    }
    return render(request, 'predictor/index.html', context)

def predict(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        modelo_seleccionado = data.get('modelo')
        datos_usuario = data['datos']
        
        # Convertir valores a códigos
        datos_usuario['CANTON'] = cantones[datos_usuario['CANTON']]
        datos_usuario['CATEGORIA DEL EVENTO'] = categorias[datos_usuario['CATEGORIA DEL EVENTO']]
        datos_usuario['CAUSA'] = causas[datos_usuario['CAUSA']]
        datos_usuario['EVENTO'] = eventos[datos_usuario['EVENTO']]

        nuevos_datos = pd.DataFrame(datos_usuario, index=[0])
        
        if modelo_seleccionado == 'python':
            resultados = predecir_probabilidades_python(modelo_python, nuevos_datos, columnas_python)
        elif modelo_seleccionado == 'rapidminer':
            rm_home = "C:/Program Files/RapidMiner/RapidMiner Studio"
            process_path = "//Local Repository/PAD_Proyecto_Final_Nivel_Afectados/Decision Tree/score"
            csv_file_path = "./ScoringModel/dataToTest.csv"
            
            connector = conectar_a_rapidminer(rm_home)
            if connector:
                guardar_csv_rapidminer(nuevos_datos, csv_file_path)
                scoring_results = ejecutar_proceso_rapidminer(connector, process_path, csv_file_path)
                if scoring_results is not None:
                    resultados = procesar_resultados_rapidminer(scoring_results)
                else:
                    resultados = []
            else:
                resultados = []
        else:
            resultados = []

        return JsonResponse({"resultados": resultados})
