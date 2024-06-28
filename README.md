
# Decision Tree Simulator

![Preview](https://i.ibb.co/6mvdCDD/preview.png)

## Descripción

Decision Tree Simulator es una aplicación web construida con Django que permite predecir datos utilizando modelos de machine learning. La aplicación soporta modelos entrenados en Python y RapidMiner, y proporciona una interfaz intuitiva para cargar datos, entrenar modelos y realizar predicciones.

## Características

- **Predicción con Modelos Python y RapidMiner**: Los usuarios pueden elegir entre utilizar modelos entrenados en Python o RapidMiner para realizar predicciones.
- **Cargador de CSV**: Los usuarios pueden cargar archivos CSV para procesarlos y reentrenar los modelos.
- **Validación de Entradas**: El formulario de predicción incluye validaciones para asegurar que los datos de entrada sean correctos.
- **Gráfico de Resultados**: Los resultados de las predicciones se muestran en un gráfico de barras que indica las probabilidades de diferentes rangos.

## Arquitectura del Proyecto

El proyecto está estructurado en varias partes clave:

- **Backend (Django)**: Maneja las solicitudes del usuario, procesa los datos, y realiza las predicciones utilizando modelos de machine learning.
- **Frontend (HTML, CSS, JavaScript)**: Proporciona la interfaz de usuario para cargar datos, realizar predicciones y mostrar los resultados.
- **Modelos de Machine Learning (Python y RapidMiner)**: Implementaciones de modelos de machine learning que se utilizan para realizar las predicciones.
- **Procesos ETL**: Procesos de extracción, transformación y carga que preparan los datos para el entrenamiento y predicción de modelos.

## Procesos ETL

Los procesos ETL en Decision Tree Simulator se encargan de transformar los datos crudos en datos que pueden ser utilizados por los modelos de machine learning. El flujo de trabajo principal es el siguiente:

1. **Carga del CSV**: El usuario carga un archivo CSV que contiene los datos crudos.
2. **Filtrado de Columnas**: Se filtran las columnas relevantes para el análisis.
3. **Procesamiento y Filtrado del Dataset**: Se aplican transformaciones y filtros adicionales para limpiar y preparar los datos.
4. **Agregación de Totales**: Se calculan totales y otras métricas relevantes.
5. **Unificación de Registros**: Se unifican registros duplicados o relacionados.
6. **Agrupación de Rangos**: Se agrupan los datos en rangos específicos para facilitar el análisis.
7. **Codificación de Columnas**: Se codifican las columnas categóricas utilizando diccionarios predefinidos.
8. **Almacenamiento de Datos**: Los datos procesados se almacenan y se utilizan para entrenar los modelos de machine learning.

## Instalación

1. Clona el repositorio:

    ```sh
    git clone https://github.com/tu-usuario/decision-tree-simulator.git
    cd decision-tree-simulator
    ```

2. Crea y activa un entorno virtual:

    ```sh
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

4. Configura las variables de entorno:

    Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

    ```env
    MODE=development
    SECRET_KEY=your-secret-key
    DEBUG=True
    ```

5. Realiza las migraciones de la base de datos:

    ```sh
    python manage.py migrate
    ```

6. Ejecuta el servidor de desarrollo:

    ```sh
    python manage.py runserver
    ```

## Uso

1. **Formulario de Predicción**:
    - Selecciona el modelo (Python o RapidMiner).
    - Ingresa los datos requeridos en el formulario.
    - Haz clic en "Predecir" para ver los resultados.

2. **Carga de CSV**:
    - Ve a la sección de carga de CSV.
    - Selecciona un archivo CSV y haz clic en "Upload and Process".
    - Descarga el archivo procesado una vez que esté listo.

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request en GitHub.

## Autor

**Bryan Garay**
- **Correo**: bryangarayacademico@gmail.com

Si tienes alguna pregunta o sugerencia, no dudes en ponerte en contacto.

---

¡Gracias por usar Decision Tree Simulator!
