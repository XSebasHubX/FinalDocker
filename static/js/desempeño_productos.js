document.addEventListener('DOMContentLoaded', function() {
    // Inicialización de variables y elementos
    const periodoSelect = document.getElementById('periodoSelect');
    const graficosContainers = document.querySelectorAll('.chart-container');
    
    // Función para mostrar un loader mientras se cargan los datos
    function mostrarLoader(container) {
        container.innerHTML = `
            <div class="loader-container">
                <div class="loader"></div>
                <p>Cargando datos...</p>
            </div>
        `;
    }

    // Función principal para actualizar los gráficos
    async function actualizarGraficos(periodo) {
        try {
            // Mostrar loader en todos los contenedores de gráficos
            graficosContainers.forEach(container => mostrarLoader(container));

            // Construir la URL con el nuevo período
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('periodo', periodo);
            
            // Realizar la petición al servidor
            const response = await fetch(currentUrl.toString(), {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }

            // Recargar la página con los nuevos datos
            window.location.href = currentUrl.toString();

        } catch (error) {
            console.error('Error al actualizar los gráficos:', error);
            // Mostrar mensaje de error al usuario
            graficosContainers.forEach(container => {
                container.innerHTML = `
                    <div class="error-message">
                        <p>Error al cargar los datos. Por favor, intente nuevamente.</p>
                    </div>
                `;
            });
        }
    }

    // Event listener para el cambio de período
    if (periodoSelect) {
        periodoSelect.addEventListener('change', function(e) {
            actualizarGraficos(e.target.value);
        });

        // Establecer el período inicial
        const urlParams = new URLSearchParams(window.location.search);
        const periodoActual = urlParams.get('periodo') || 'year';
        periodoSelect.value = periodoActual;
    }

    // Función para el botón de actualizar
    const refreshBtn = document.querySelector('.refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            const currentPeriodo = periodoSelect.value;
            actualizarGraficos(currentPeriodo);
        });
    }

    // Animaciones de entrada para los contenedores
    graficosContainers.forEach((container, index) => {
        setTimeout(() => {
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 100 * (index + 1));
    });

    // Efecto hover en los contenedores
    graficosContainers.forEach(container => {
        container.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });

        container.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.transition = 'transform 0.3s ease';
        });
    });

    // Función para animar las gráficas al entrar en el viewport
    function animateOnScroll() {
        const charts = document.querySelectorAll('.chart-container');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                    // Trigger Plotly animation if available
                    const plotlyGraph = entry.target.querySelector('.plotly-graph-div');
                    if (plotlyGraph && plotlyGraph._Plotly) {
                        plotlyGraph._Plotly.animate(plotlyGraph, {
                            data: plotlyGraph.data,
                            layout: plotlyGraph.layout,
                            config: {
                                duration: 1000,
                                easing: 'cubic-in-out'
                            }
                        });
                    }
                }
            });
        }, {
            threshold: 0.1
        });

        charts.forEach(chart => observer.observe(chart));
    }

    // Iniciar animaciones
    animateOnScroll();
}); 