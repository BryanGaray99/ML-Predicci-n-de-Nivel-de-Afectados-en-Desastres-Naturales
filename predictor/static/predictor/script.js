// predictor/static/predictor/script.js

let predictionChart = null;  // Definir la variable predictionChart a nivel global

function showLoader() {
    document.getElementById('loader').style.display = 'block';
    document.getElementById('predictionChart').style.display = 'none'; // Ocultar el gráfico cuando se muestra el loader
}

function hideLoader() {
    document.getElementById('loader').style.display = 'none';
    document.getElementById('predictionChart').style.display = 'block'; // Mostrar el gráfico cuando se oculta el loader
}

function makePrediction() {
    if (predictionChart) {
        predictionChart.destroy();
    }

    // Limpiar el contenido del resultado final
    document.getElementById('finalPrediction').innerText = '';

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

    showLoader();  // Mostrar el loader antes de enviar la solicitud

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
        alert('Error al obtener la predicción.');
    })
    .finally(() => {
        hideLoader();  // Ocultar el loader después de recibir la respuesta
    });
}

document.addEventListener('DOMContentLoaded', function() {
    $('.select2').select2();
});
