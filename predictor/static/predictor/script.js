// predictor/static/predictor/script.js

let predictionChart = null;  // Definir la variable predictionChart a nivel global
let downloadLink = null;  // Definir la variable downloadLink a nivel global

function showLoaderChart() {
    document.getElementById('loader').style.display = 'block';
    document.getElementById('predictionChart').style.display = 'none'; // Ocultar el gráfico cuando se muestra el loader
}

function hideLoaderChart() {
    document.getElementById('loader').style.display = 'none';
    document.getElementById('predictionChart').style.display = 'block'; // Mostrar el gráfico cuando se oculta el loader
}

function showLoaderCSV() {
    document.getElementById('loader-csv').style.display = 'block';
}

function hideLoaderCSV() {
    document.getElementById('loader-csv').style.display = 'none';
}

function makePrediction() {
    if (predictionChart) {
        predictionChart.destroy();
    }

    // Limpiar el contenido del resultado final
    document.getElementById('finalPrediction').innerText = '';
    document.getElementById('finalPrediction').style.color = 'black'; // Restablecer el color del texto a negro

    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const data = {
        'modelo': document.getElementById('modelo').value,
        'datos': {
            'TOTAL DE INFRAESTRUCTURA AFECTADA': document.getElementById('infraestructura').value,
            'CANTON': document.getElementById('canton').value,
            'EVENTO': document.getElementById('evento').value,
            'CAUSA': document.getElementById('causa').value,
            'CATEGORIA DEL EVENTO': document.getElementById('categoria').value,
            'MES': document.getElementById('mes').value
        }
    };

    showLoaderChart();  // Mostrar el loader antes de enviar la solicitud

    fetch('/predict/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }

        const resultados = data.resultados[0];
        const probabilidades = resultados.slice(0, 3).map(p => (p * 100).toFixed(2)); // Convertir a porcentaje y limitar a dos decimales
        const prediccionFinal = resultados[3];
        const labels = ['Rango 1', 'Rango 2', 'Rango 3'];
        const ctx = document.getElementById('predictionChart').getContext('2d');

        // Destruir el gráfico anterior si existe
        if (predictionChart) {
            predictionChart.destroy();
        }

        // Crear el nuevo gráfico de predicción
        predictionChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Probabilidades (%)',
                    data: probabilidades,
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(75, 192, 192, 0.2)'
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100, // Ajustar el máximo a 100%
                        ticks: {
                            callback: function(value) {
                                return value + '%'; // Añadir el símbolo de porcentaje a las etiquetas del eje Y
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.raw + '%'; // Añadir el símbolo de porcentaje a los tooltips
                            }
                        }
                    },
                    datalabels: {
                        display: true,
                        align: 'end',
                        anchor: 'end',
                        formatter: function(value) {
                            return value + '%'; // Mostrar porcentaje en las etiquetas de las barras
                        }
                    }
                }
            },
            plugins: [ChartDataLabels]
        });

        // Muestra el resultado final de la predicción
        const rangoFinal = ['Rango 1', 'Rango 2', 'Rango 3'][prediccionFinal - 1];
        document.getElementById('finalPrediction').innerText = `Rango más probable: ${rangoFinal}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('finalPrediction').innerText = error.message;
        document.getElementById('finalPrediction').style.color = 'red';
    })
    .finally(() => {
        hideLoaderChart();  // Ocultar el loader después de recibir la respuesta
    });
}

function uploadCSV() {
    // Limpiar el mensaje anterior y ocultar el enlace de descarga
    const messageElement = document.getElementById('upload-message');
    const downloadLink = document.getElementById('download-link');
    messageElement.innerText = '';
    messageElement.classList.remove('error');
    downloadLink.style.display = 'none';

    const form = document.getElementById('upload-csv-form');
    const formData = new FormData(form);
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    showLoaderCSV();

    fetch('/upload_csv/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la carga del archivo');
        }
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        downloadLink.href = url;
        downloadLink.download = 'processed_data.csv';
        downloadLink.style.display = 'block';
        downloadLink.click();
        window.URL.revokeObjectURL(url);
        messageElement.innerText = 'Archivo procesado y listo para descargar.';
    })
    .catch(error => {
        console.error('Error:', error);
        messageElement.innerText = 'Error al procesar el archivo.';
        messageElement.classList.add('error');
    })
    .finally(() => {
        hideLoaderCSV();  // Ocultar el loader después de recibir la respuesta
    });
}

document.addEventListener('DOMContentLoaded', function() {
    $('.select2').select2();
});
