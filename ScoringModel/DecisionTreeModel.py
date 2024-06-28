# Importar librerías
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import tree
import graphviz
import seaborn as sns
from PIL import Image
from sklearn.tree import DecisionTreeClassifier

# Cargar el archivo CSV
file_path = './ETL/Dataset/04_Codificacion_Dataset.csv'
df = pd.read_csv(file_path)

# Definir las variables independientes y dependiente
X3 = df.drop('TOTAL DE PERSONAS AFECTADAS', axis=1)
y3 = df['TOTAL DE PERSONAS AFECTADAS']

# Conjunto de Entrenamiento y Prueba
X3_entrena, X3_prueba, y3_entrena, y3_prueba = train_test_split(X3, y3, 
                                            test_size=0.2, random_state=3)
print('Conjunto de Entrenamiento set:', X3_entrena.shape, y3_entrena.shape)
print('Conjunto de Prueba:', X3_prueba.shape, y3_prueba.shape)

# Ajustar el modelo de Árbol de Decisión
arbol_modelo = DecisionTreeClassifier(criterion="entropy", max_depth=4)
arbol_modelo.fit(X3_entrena, y3_entrena)

# Precisión y Margen de Error del modelo
arbol_pronostico = arbol_modelo.predict(X3_prueba)
accuracy = metrics.accuracy_score(y3_prueba, arbol_pronostico)
classification_error = 1 - accuracy

print("Precisión del modelo basado en árbol de decisiones: ", accuracy)
print("Error de clasificación del modelo basado en árbol de decisiones: ", classification_error)

# Validación cruzada para calcular la desviación estándar
cv_scores = cross_val_score(arbol_modelo, X3, y3, cv=10, scoring='accuracy')
std_dev_accuracy = np.std(cv_scores)
std_dev_classification_error = np.std(1 - cv_scores)

print("Desviación estándar de la precisión: ", std_dev_accuracy)
print("Desviación estándar del error de clasificación: ", std_dev_classification_error)

# Matriz de Confusión
conf_matrix = metrics.confusion_matrix(y3_prueba, arbol_pronostico)
conf_matrix_df = pd.DataFrame(conf_matrix, index=[f'True {i}' for i in np.unique(y3)], columns=[f'Pred {i}' for i in np.unique(y3)])

# Calcular las precisiones y recalls por clase
class_precisions = conf_matrix.diagonal() / conf_matrix.sum(axis=1)
class_recalls = conf_matrix.diagonal() / conf_matrix.sum(axis=0)

conf_matrix_df['Class Precision'] = [f'{p:.2%}' for p in class_precisions]
conf_matrix_df['Class Recall'] = [f'{r:.2%}' for r in class_recalls]

# Visualización de la matriz de confusión
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(y3), yticklabels=np.unique(y3))
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Matriz de Confusión - Python')
plt.show()

# Mostrar la matriz de confusión con precisiones y recalls por clase
print(conf_matrix_df)

# Definir combinaciones de datos de prueba con el mismo orden de columnas
test_data_combined = {
    'CANTON': [1, 2, 3],
    'EVENTO': [1, 1, 2],
    'CAUSA': [1, 2, 3],
    'CATEGORIA DEL EVENTO': [1, 2, 3],
    'MES': [1, 2, 3],
    'TOTAL DE INFRAESTRUCTURA AFECTADA': [0, 5, 100]
}

# Crear el DataFrame de prueba con las mismas columnas y orden
test_df_combined = pd.DataFrame(test_data_combined, columns=X3.columns)

# Realizar predicciones con los datos de prueba específicos
y_pred_combined = arbol_modelo.predict(test_df_combined)

# Decodificar las predicciones
def decodificar_categoria(pred):
    if pred == 1:
        return "Rango 1"
    elif pred == 2:
        return "Rango 2"
    elif pred == 3:
        return "Rango 3"
    else:
        return "Desconocido"

decoded_predictions = [decodificar_categoria(pred) for pred in y_pred_combined]

# Mostrar los resultados de las predicciones
for i, prediction in enumerate(decoded_predictions):
    print(f"Predicción para el caso {i+1}: El rango de personas afectadas es '{prediction}'")

# Nombres de las características
featureNames = X3.columns
classNames = ["Rango 1", "Rango 2", "Rango 3"]

# Exportar el modelo a formato DOT con nombres truncados
graphicTree = tree.export_graphviz(
    arbol_modelo,
    feature_names=featureNames,
    class_names=classNames,
    out_file=None,
    filled=True,
    rounded=True,
    special_characters=True
)

# Crear un objeto Graphviz para visualizar el árbol de decisiones
graph = graphviz.Source(graphicTree)

# Especifica la ruta y el nombre del archivo donde deseas guardar la imagen
output_path = "decision_tree"

# Guardar el gráfico como PNG
graph.render(filename=output_path, format='png', cleanup=True)

print(f"El gráfico se ha guardado en {output_path}")
