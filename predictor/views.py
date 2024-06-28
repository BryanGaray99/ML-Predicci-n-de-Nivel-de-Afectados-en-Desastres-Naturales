# predictor/views.py
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
import pandas as pd
from .models import (
    cargar_modelo_python, 
    predecir_probabilidades_python,
    procesar_y_reentrenar, 
    conectar_a_rapidminer, 
    preparar_datos_rapidminer, 
    guardar_csv_rapidminer, 
    ejecutar_proceso_rapidminer, 
    procesar_resultados_rapidminer
)
from .utils import cargar_diccionarios
from django.conf import settings
from django_ratelimit.decorators import ratelimit

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
        'eventos': eventos,
        'meses': range(1, 13), 
        'mode': settings.MODE
    }
    return render(request, 'predictor/index.html', context)

@ratelimit(key='ip', rate='50/d', method=ratelimit.ALL, block=True)
def predict(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        modelo_seleccionado = data.get('modelo')
        datos_usuario = data['datos']
        
        # Validaciones y conversiones
        try:
            total_infra = int(datos_usuario['TOTAL DE INFRAESTRUCTURA AFECTADA'])
            if total_infra < 0 or total_infra > 10000000:
                raise ValueError("El total de infraestructura debe estar entre 0 y 10,000,000.")
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        
        datos_usuario['CANTON'] = cantones[datos_usuario['CANTON']]
        datos_usuario['CATEGORIA DEL EVENTO'] = categorias[datos_usuario['CATEGORIA DEL EVENTO']]
        datos_usuario['CAUSA'] = causas[datos_usuario['CAUSA']]
        datos_usuario['EVENTO'] = eventos[datos_usuario['EVENTO']]

        nuevos_datos = pd.DataFrame(datos_usuario, index=[0])

        if settings.MODE == 'production' and modelo_seleccionado == 'rapidminer':
            return JsonResponse({"error": "RapidMiner predictions are disabled in production mode."}, status=403)

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

@ratelimit(key='ip', rate='20/d', method=ratelimit.ALL, block=True)
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        csv_file_path = f"./ETL/Dataset/{csv_file.name}"
        
        with open(csv_file_path, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)
        
        try:
            processed_csv_path = procesar_y_reentrenar(csv_file_path)
            with open(processed_csv_path, 'rb') as processed_file:
                response = HttpResponse(processed_file.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename={os.path.basename(processed_csv_path)}'
                return response
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)