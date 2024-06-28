import pandas as pd
import os

def filtrar_columnas(csv_file_path):
    # Lista de columnas a mantener
    columnas_a_mantener = [
        "CANTON", "EVENTO", "CAUSA", "CATEGORIA DEL EVENTO", "MES", "FALLECIDAS", "HERIDAS",
        "PERSONAS DESAPARECIDAS", "FAMILIAS AFECTADAS", "PERSONAS AFECTADAS DIRECTAMENTE", "AFECTADAS INDIRECTAS",
        "FAMILIAS DAMNIFICADAS", "PERSONAS DAMNIFICADAS", "PERSONAS EVACUADAS", "PERSONAS ALBERGADAS",
        "P. EN FAMILIAS ACOGIENTES", "PERSONAS EN OTROS MEDIOS", "VIVIENDAS AFECTADAS", "VIVIENDAS DESTRUIDAS",
        "ESTABLECIMIENTOS EDUCATIVOS AFECTADOS", "ESTABLECIMIENTOS EDUCATIVOS DESTRUIDOS", "CENTROS DE SALUD AFECTADOS",
        "CENTROS DE SALUD DESTRUIDOS", "PUENTES AFECTADOS", "PUENTES DESTRUIDOS", "BIENES PUBLICOS AFECTADOS",
        "BIENES PUBLICOS DESTRUIDOS", "BIENES PRIVADOS AFECTADOS", "BIENES PRIVADOS DESTRUIDOS"
    ]

    # Leer el archivo CSV
    df = pd.read_csv(csv_file_path, low_memory=False)

    print(f"Original dataset size: {df.shape}")

    # Renombrar columna con salto de línea
    df.rename(columns={"PERSONAS EN\n  OTROS MEDIOS": "PERSONAS EN OTROS MEDIOS"}, inplace=True)

    # Filtrar las columnas
    df_filtrado = df[columnas_a_mantener]
    # print(f"Dataset size after column filtering: {df_filtrado.shape}")


    return df_filtrado

def procesar_y_filtrar_dataset(df):
    eventos_permitidos = [
        "ACTIVIDAD VOLCÁNICA", "ALUVIÓN", "AVALANCHA", "DESLIZAMIENTO", "GRANIZADA", "HELADA", "HUNDIMIENTO",
        "INCENDIO FORESTAL", "INUNDACIÓN", "OLEAJE", "SISMO", "SOCAVAMIENTO", "TORMENTA ELÉCTRICA", "TSUNAMI", "VENDAVAL"
    ]
    categorias_permitidas = [
        "GLP", "NATURAL", "NIÑA", "SISMO", "ÉPOCA LLUVIOSA", "ÉPOCA SECA"
    ]
    causas_permitidas = [
        "ACTIVIDAD SÍSMICA", "INUNDACIÓN", "ACTIVIDAD VOLCÁNICA", "LLUVIAS", "AGUAJE", "OLEAJE", "AGUAJE/MAREJADA",
        "OTRA CAUSA", "DESBORDAMIENTO", "PROCESO ERUPTIVO", "DESCONOCIDA", "SISMO", "DETERIORO", "INESTABILIDAD",
        "EROSIÓN", "VENDAVAL", "FALLA", "VIENTOS FUERTES", "FALLA GEOLÓGICA", "CONDICIONES ATMOSFÉRICAS",
        "CAMBIOS INTENSOS DE TEMPERATURAS", "TORMENTAS ELÉCTRICAS", "LIBERACIÓN DE ENERGÍA INTERNA DE LA TIERRA",
        "DESBORDAMIENTO DE CUERPOS DE AGUA", "ACUMULACIÓN DE AGUA EN EL SUELO",
        "TECTONISMO (ROCE DE PLACAS TECTÓNICAS Y FALLAS GEOLÓGICAS SUPERFICIALES)"
    ]

    # Eliminar filas con valores vacíos en las columnas seleccionadas
    df = df.dropna()
    # print(f"Dataset size after dropping NA: {df.shape}")

    # Limpieza de texto y conversión a mayúsculas
    columnas_texto = ["CANTON", "EVENTO", "CAUSA", "CATEGORIA DEL EVENTO"]
    for columna in columnas_texto:
        df.loc[:, columna] = df[columna].str.upper().str.strip()

    # Corregir categorías iguales que se diferencian por algún símbolo o caracter
    df["CATEGORIA DEL EVENTO"] = df["CATEGORIA DEL EVENTO"].str.strip()
    df["CAUSA"] = df["CAUSA"].str.strip()
    df["EVENTO"] = df["EVENTO"].str.strip()

    # Filtrar por valores permitidos
    df_filtrado = df[
        (df["EVENTO"].isin(eventos_permitidos)) &
        (df["CAUSA"].isin(causas_permitidas)) &
        (df["CATEGORIA DEL EVENTO"].isin(categorias_permitidas))
    ]
    # print(f"Dataset size after filtering values: {df_filtrado.shape}")

    # Ordenar el DataFrame alfabéticamente por la columna CANTON
    df_ordenado = df_filtrado.sort_values(by="CANTON")
    # print(f"Dataset size after sorting: {df_ordenado.shape}")

    return df_ordenado

def agregar_totales(df):
    # Columnas que suman para TOTAL DE PERSONAS AFECTADAS
    columnas_personas_afectadas = [
        "FALLECIDAS", "HERIDAS", "PERSONAS DESAPARECIDAS", "FAMILIAS AFECTADAS",
        "PERSONAS AFECTADAS DIRECTAMENTE", "AFECTADAS INDIRECTAS", "FAMILIAS DAMNIFICADAS",
        "PERSONAS DAMNIFICADAS", "PERSONAS EVACUADAS", "PERSONAS ALBERGADAS",
        "P. EN FAMILIAS ACOGIENTES", "PERSONAS EN OTROS MEDIOS"
    ]

    # Columnas que suman para TOTAL DE INFRAESTRUCTURA AFECTADA
    columnas_infraestructura_afectada = [
        "VIVIENDAS AFECTADAS", "VIVIENDAS DESTRUIDAS", "ESTABLECIMIENTOS EDUCATIVOS AFECTADOS",
        "ESTABLECIMIENTOS EDUCATIVOS DESTRUIDOS", "CENTROS DE SALUD AFECTADOS", "CENTROS DE SALUD DESTRUIDOS",
        "PUENTES AFECTADOS", "PUENTES DESTRUIDOS", "BIENES PUBLICOS AFECTADOS", "BIENES PUBLICOS DESTRUIDOS",
        "BIENES PRIVADOS AFECTADOS", "BIENES PRIVADOS DESTRUIDOS"
    ]

    # Filtrar las columnas para asegurarse de que sean numéricas
    for col in columnas_personas_afectadas + columnas_infraestructura_afectada:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Eliminar las filas que tengan NaN en las columnas a sumar
    df = df.dropna(subset=columnas_personas_afectadas + columnas_infraestructura_afectada)

    # Sumar las columnas especificadas para cada fila
    df["TOTAL DE PERSONAS AFECTADAS"] = df[columnas_personas_afectadas].sum(axis=1).astype(int)
    df["TOTAL DE INFRAESTRUCTURA AFECTADA"] = df[columnas_infraestructura_afectada].sum(axis=1).astype(int)

    # Eliminar las columnas que sirvieron para las sumas
    columnas_a_eliminar = columnas_personas_afectadas + columnas_infraestructura_afectada
    df = df.drop(columns=columnas_a_eliminar)

    # Logs para verificar las columnas y el tamaño del dataset
    # print(f"Dataset columns after adding totals: {df.columns.tolist()}")
    # print(f"Dataset size after adding totals: {df.shape}")

    return df


def unificar_registros(df):
    # Agrupar por las columnas especificadas y sumar los valores de totales
    df_unificado = df.groupby(["CANTON", "EVENTO", "CAUSA", "CATEGORIA DEL EVENTO", "MES"], as_index=False).agg({
        "TOTAL DE PERSONAS AFECTADAS": "sum",
        "TOTAL DE INFRAESTRUCTURA AFECTADA": "sum"
    })

    # Logs para verificar las columnas y el tamaño del dataset
    # print(f"Dataset columns after unification: {df_unificado.columns.tolist()}")
    # print(f"Dataset size after unification: {df_unificado.shape}")

    return df_unificado

def agrupar_rangos_personas_afectadas(df):
    # Definir una función para asignar el rango basado en el valor de TOTAL DE PERSONAS AFECTADAS
    def asignar_rango(valor):
        if valor >= 0 and valor <= 4:
            return "Rango 1"
        elif valor >= 5 and valor <= 50:
            return "Rango 2"
        else:
            return "Rango 3"

    # Aplicar la función de asignación de rangos directamente en la columna TOTAL DE PERSONAS AFECTADAS
    df["TOTAL DE PERSONAS AFECTADAS"] = df["TOTAL DE PERSONAS AFECTADAS"].apply(asignar_rango)

    # Logs para verificar las columnas y el tamaño del dataset
    # print(f"Dataset columns after adding range: {df.columns.tolist()}")
    # print(f"Dataset size after adding range: {df.shape}")

    return df

def codificar_columnas(df, canton_dict_path, evento_dict_path, causa_dict_path, categoria_dict_path):
    # Leer los diccionarios de codificación
    canton_dict = pd.read_csv(canton_dict_path).set_index("CANTON").to_dict()["CODIGO"]
    evento_dict = pd.read_csv(evento_dict_path).set_index("EVENTO").to_dict()["CODIGO"]
    causa_dict = pd.read_csv(causa_dict_path).set_index("CAUSA").to_dict()["CODIGO"]
    categoria_dict = pd.read_csv(categoria_dict_path).set_index("CATEGORIA DEL EVENTO").to_dict()["CODIGO"]

    # Codificar las columnas
    df["CANTON"] = df["CANTON"].map(canton_dict)
    df["EVENTO"] = df["EVENTO"].map(evento_dict)
    df["CAUSA"] = df["CAUSA"].map(causa_dict)
    df["CATEGORIA DEL EVENTO"] = df["CATEGORIA DEL EVENTO"].map(categoria_dict)

    # Descartar filas con valores no encontrados en los diccionarios
    df = df.dropna(subset=["CANTON", "EVENTO", "CAUSA", "CATEGORIA DEL EVENTO"])

    # Codificar la columna "TOTAL DE PERSONAS AFECTADAS"
    df["TOTAL DE PERSONAS AFECTADAS"] = df["TOTAL DE PERSONAS AFECTADAS"].map({
        "Rango 1": 1,
        "Rango 2": 2,
        "Rango 3": 3
    })
    
    # Asegurar que las columnas relevantes sean enteras
    df["CANTON"] = df["CANTON"].astype(int)
    df["MES"] = df["MES"].astype(int)
    df["EVENTO"] = df["EVENTO"].astype(int)
    df["CAUSA"] = df["CAUSA"].astype(int)
    df["CATEGORIA DEL EVENTO"] = df["CATEGORIA DEL EVENTO"].astype(int)
    df["TOTAL DE INFRAESTRUCTURA AFECTADA"] = df["TOTAL DE INFRAESTRUCTURA AFECTADA"].astype(int)
    df["TOTAL DE PERSONAS AFECTADAS"] = df["TOTAL DE PERSONAS AFECTADAS"].astype(int)
    
    # Logs para verificar las columnas y el tamaño del dataset
    print(f"Dataset columns after encoding: {df.columns.tolist()}")
    print(f"Dataset size after encoding: {df.shape}")

    return df

# Uso
def procesar_csv_completo(csv_file_path, output_csv_path):
    # Diccionarios
    canton_dict_path = "./ETL/DD/canton_dict.csv"
    evento_dict_path = "./ETL/DD/evento_dict.csv"
    causa_dict_path = "./ETL/DD/causa_dict.csv"
    categoria_dict_path = "./ETL/DD/categoria_dict.csv"
    
    # Aplicar las funciones en orden
    df_filtrado = filtrar_columnas(csv_file_path)
    df_procesado = procesar_y_filtrar_dataset(df_filtrado)
    df_totales = agregar_totales(df_procesado)
    df_unificado = unificar_registros(df_totales)
    df_con_rangos = agrupar_rangos_personas_afectadas(df_unificado)


    df_codificado = codificar_columnas(df_con_rangos, canton_dict_path, evento_dict_path, causa_dict_path, categoria_dict_path)
    
    # Ordenar las columnas en el DataFrame final
    columnas_finales = [
        "CANTON", "EVENTO", "CATEGORIA DEL EVENTO", "CAUSA", "MES", 
        "TOTAL DE PERSONAS AFECTADAS", "TOTAL DE INFRAESTRUCTURA AFECTADA"
    ]
    df_codificado = df_codificado[columnas_finales]
    
    # Guardar el resultado final en un archivo CSV
    df_codificado.to_csv(output_csv_path, index=False)
    print("Procesamiento completado y archivo guardado.")

# Prueba
# procesar_csv_completo("./ETL/Dataset/SGR_EventosPeligrosos_2010_2022Diciembre.csv", "./ETL/Dataset/SGR_EventosPeligrosos_2010_2022DiciembrePrueba.csv")