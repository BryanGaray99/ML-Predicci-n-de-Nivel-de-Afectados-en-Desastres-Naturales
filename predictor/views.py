# predictor/views.py

from django.shortcuts import render
from django.http import JsonResponse
import json
import pandas as pd
from .models import cargar_modelo, predecir_probabilidades, conectar_a_rapidminer, preparar_datos, guardar_csv, ejecutar_proceso, procesar_resultados
from .utils import cargar_diccionarios

# Cargar el modelo de Python una vez al iniciar
modelo_path = 'arbol_modelo.pkl'
modelo_python, columnas_python = cargar_modelo(modelo_path)

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
            resultados = predecir_probabilidades(modelo_python, nuevos_datos, columnas_python)
        elif modelo_seleccionado == 'rapidminer':
            rm_home = "C:/Program Files/RapidMiner/RapidMiner Studio"
            process_path = "//Local Repository/PAD_Proyecto_Final_Nivel_Afectados/Decision Tree/score"
            csv_file_path = "dataToTest.csv"
            
            connector = conectar_a_rapidminer(rm_home)
            if connector:
                guardar_csv(nuevos_datos, csv_file_path)
                scoring_results = ejecutar_proceso(connector, process_path, csv_file_path)
                if scoring_results is not None:
                    resultados = procesar_resultados(scoring_results)
                else:
                    resultados = []
            else:
                resultados = []
        else:
            resultados = []

        return JsonResponse({"resultados": resultados})
