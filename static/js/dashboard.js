// Configuración del tema profesional
const themeConfig = {
    colors: {
        primary: ['#000000', '#1a1a1a', '#333333', '#4d4d4d', '#666666'],
        accent: '#FF0000',
        background: '#FFFFFF',
        text: '#2D3436',
        grid: 'rgba(0, 0, 0, 0.05)'
    },
    fonts: {
        primary: "'Roboto', sans-serif"
    },
    animation: {
        duration: 2000,
        easing: 'easeOutQuart'
    }
};

// Inicialización de gráficas
document.addEventListener('DOMContentLoaded', function() {
    // 1. Gráfica de Ventas por Minorista (Mixed Chart)
    new Chart(document.getElementById('chartCompVentMinor'), {
        type: 'bar',
        data: {
            labels: dataCompVentMinor.map(item => item.Retailer),
            datasets: [
                {
                    type: 'bar',
                    label: 'Ventas Totales',
                    data: dataCompVentMinor.map(item => item.Ventas_Totales),
                    backgroundColor: themeConfig.colors.primary[0],
                    borderRadius: 6,
                    barPercentage: 0.5,
                    order: 2
                },
                {
                    type: 'line',
                    label: 'Tendencia',
                    data: dataCompVentMinor.map(item => item.Ventas_Totales),
                    borderColor: themeConfig.colors.accent,
                    borderWidth: 2,
                    pointStyle: 'circle',
                    pointRadius: 4,
                    pointBackgroundColor: themeConfig.colors.background,
                    tension: 0.4,
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    position: 'top',
                    align: 'end',
                    labels: {
                        boxWidth: 12,
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.95)',
                    titleFont: {
                        size: 13,
                        weight: 600
                    },
                    bodyFont: {
                        size: 12
                    },
                    padding: 12,
                    cornerRadius: 4,
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${new Intl.NumberFormat('es-ES', {
                                style: 'currency',
                                currency: 'USD',
                                minimumFractionDigits: 0
                            }).format(context.parsed.y)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: themeConfig.colors.grid,
                        drawBorder: false
                    },
                    ticks: {
                        font: {
                            size: 11
                        },
                        callback: value => new Intl.NumberFormat('es-ES', {
                            style: 'currency',
                            currency: 'USD',
                            notation: 'compact'
                        }).format(value)
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            size: 11
                        }
                    }
                }
            }
        }
    });

    // 2. Gráfica de Distribución Mensual (Area Stacked)
    new Chart(document.getElementById('chartDistVentMes'), {
        type: 'line',
        data: {
            labels: dataDistVentMes.map(item => item.Mes),
            datasets: [{
                label: 'Ventas Mensuales',
                data: dataDistVentMes.map(item => item.Ventas_Totales),
                fill: true,
                backgroundColor: createGradient(['rgba(0,0,0,0.2)', 'rgba(0,0,0,0)'], 'chartDistVentMes'),
                borderColor: themeConfig.colors.primary[0],
                borderWidth: 2,
                tension: 0.3,
                pointBackgroundColor: themeConfig.colors.background,
                pointBorderColor: themeConfig.colors.primary[0],
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(0, 0, 0, 0.95)',
                    titleMarginBottom: 10,
                    padding: 12,
                    cornerRadius: 4
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: themeConfig.colors.grid
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });

    // 3. Gráfica de Ventas por Región (Radar Chart)
    new Chart(document.getElementById('chartVenRegTotal'), {
        type: 'radar',
        data: {
            labels: dataVenRegTotal.map(item => item.Region),
            datasets: [{
                label: 'Ventas por Región',
                data: dataVenRegTotal.map(item => item.Ventas_Totales),
                backgroundColor: 'rgba(0, 0, 0, 0.1)',
                borderColor: themeConfig.colors.primary[0],
                borderWidth: 2,
                pointBackgroundColor: themeConfig.colors.background,
                pointBorderColor: themeConfig.colors.primary[0],
                pointHoverBackgroundColor: themeConfig.colors.accent,
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    angleLines: {
                        color: themeConfig.colors.grid
                    },
                    grid: {
                        color: themeConfig.colors.grid
                    },
                    pointLabels: {
                        font: {
                            size: 11
                        }
                    },
                    ticks: {
                        backdropColor: 'transparent',
                        callback: value => new Intl.NumberFormat('es-ES', {
                            style: 'currency',
                            currency: 'USD',
                            notation: 'compact'
                        }).format(value)
                    }
                }
            }
        }
    });
});

// Función auxiliar para crear gradientes
function createGradient(colorStops, chartId) {
    const ctx = document.getElementById(chartId).getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    colorStops.forEach((color, index) => {
        gradient.addColorStop(index / (colorStops.length - 1), color);
    });
    return gradient;
}

// Animación de números
document.querySelectorAll('.metric-value').forEach(el => {
    const value = parseFloat(el.dataset.value);
    animateValue(el, 0, value, 2000);
});

function animateValue(obj, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const current = Math.floor(progress * (end - start) + start);
        obj.textContent = new Intl.NumberFormat('es-ES', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0
        }).format(current);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

// Manejo de responsive
window.addEventListener('resize', () => {
    if (Chart.instances.length > 0) {
        Chart.instances.forEach(chart => chart.resize());
    }
});

// Función para formatear números grandes
function formatNumber(number) {
    if (number >= 1000000) {
        return (number / 1000000).toFixed(1) + 'M';
    } else if (number >= 1000) {
        return (number / 1000).toFixed(1) + 'K';
    }
    return number.toString();
} 