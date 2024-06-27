# predictor/utils.py

import pandas as pd

def cargar_diccionarios():
    cantones = pd.read_csv('ETL/DD/canton_dict.csv').set_index('CANTON')['CODIGO'].to_dict()
    categorias = pd.read_csv('ETL/DD/categoria_dict.csv').set_index('CATEGORIA DEL EVENTO')['CODIGO'].to_dict()
    causas = pd.read_csv('ETL/DD/causa_dict.csv').set_index('CAUSA')['CODIGO'].to_dict()
    eventos = pd.read_csv('ETL/DD/evento_dict.csv').set_index('EVENTO')['CODIGO'].to_dict()
    
    return cantones, categorias, causas, eventos
