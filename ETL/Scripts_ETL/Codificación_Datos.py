import pandas as pd

# Cargar el archivo CSV
file_path = '03-Transformación_Datos.csv'
df = pd.read_csv(file_path)

# # Crear diccionarios para las variables de texto asegurando unicidad
canton_dict = {idx + 1: canton for idx, canton in enumerate(sorted(df['CANTON'].unique()))}
evento_dict = {idx + 1: evento for idx, evento in enumerate(sorted(df['EVENTO'].unique()))}
categoria_dict = {idx + 1: categoria for idx, categoria in enumerate(sorted(df['CATEGORIA DEL EVENTO'].unique()))}
causa_dict = {idx + 1: causa for idx, causa in enumerate(sorted(df['CAUSA'].unique()))}

# Guardar los diccionarios en archivos CSV
pd.DataFrame(list(canton_dict.items()), columns=['CODIGO', 'CANTON']).to_csv('canton_dict.csv', index=False)
pd.DataFrame(list(evento_dict.items()), columns=['CODIGO', 'EVENTO']).to_csv('evento_dict.csv', index=False)
pd.DataFrame(list(categoria_dict.items()), columns=['CODIGO', 'CATEGORIA DEL EVENTO']).to_csv('categoria_dict.csv', index=False)
pd.DataFrame(list(causa_dict.items()), columns=['CODIGO', 'CAUSA']).to_csv('causa_dict.csv', index=False)

# Reemplazar las variables de texto con sus códigos correspondientes en el DataFrame
df['CANTON'] = df['CANTON'].map({v: k for k, v in canton_dict.items()})
df['EVENTO'] = df['EVENTO'].map({v: k for k, v in evento_dict.items()})
df['CATEGORIA DEL EVENTO'] = df['CATEGORIA DEL EVENTO'].map({v: k for k, v in categoria_dict.items()})
df['CAUSA'] = df['CAUSA'].map({v: k for k, v in causa_dict.items()})

# Definir la función de conversión
def convertir_rango_a_numero(rango):
    if rango == "Rango 1":
        return 1
    elif rango == "Rango 2":
        return 2
    elif rango == "Rango 3":
        return 3
    else:
        return None  # Maneja valores que no coinciden con ningún rango

# Aplicar la función a la columna 'TOTAL DE PERSONAS AFECTADAS'
df['TOTAL DE PERSONAS AFECTADAS'] = df['TOTAL DE PERSONAS AFECTADAS'].apply(convertir_rango_a_numero)

# Guardar el DataFrame codificado en un archivo CSV
df.to_csv('04_Codificacion_Dataset.csv', index=False)
