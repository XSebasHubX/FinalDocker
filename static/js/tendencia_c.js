document.addEventListener('DOMContentLoaded', function() {
    // Inicialización de variables y elementos
    const periodoSelect = document.getElementById('periodoSelect');
    const graficosContainers = document.querySelectorAll('.chart-container');
    
    // Función para mostrar el loader
    function mostrarLoader(container) {
        container.innerHTML = `
            <div class="loader-container">
                <div class="loader"></div>
                <p>Cargando datos...</p>
            </div>
        `;
    }

    // Función para actualizar los gráficos de tendencias
    async function actualizarGraficos(periodo) {
        try {
            // Mostrar loader en todos los contenedores
            graficosContainers.forEach(container => mostrarLoader(container));

            // Construir URL con el nuevo período
            const currentUrl = new URL(window.location.href);
            currentUrl.searchParams.set('periodo', periodo);
            
            // Realizar petición AJAX
            const response = await fetch(currentUrl.toString(), {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }

            // Recargar página con nuevos datos
            window.location.href = currentUrl.toString();

        } catch (error) {
            console.error('Error al actualizar las tendencias:', error);
            graficosContainers.forEach(container => {
                container.innerHTML = `
                    <div class="error-message">
                        <p>Error al cargar las tendencias comparativas. Por favor, intente nuevamente.</p>
                    </div>
                `;
            });
        }
    }

    // Event listener para cambio de período
    if (periodoSelect) {
        periodoSelect.addEventListener('change', function(e) {
            actualizarGraficos(e.target.value);
        });

        // Establecer período inicial desde URL
        const urlParams = new URLSearchParams(window.location.search);
        const periodoActual = urlParams.get('periodo') || 'year';
        periodoSelect.value = periodoActual;
    }

    // Event listener para botón de actualizar
    const refreshBtn = document.querySelector('.refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            this.classList.add('rotating'); // Añadir animación de rotación
            const currentPeriodo = periodoSelect.value;
            actualizarGraficos(currentPeriodo).finally(() => {
                setTimeout(() => {
                    this.classList.remove('rotating');
                }, 1000);
            });
        });
    }

    // Animaciones de entrada para los contenedores
    graficosContainers.forEach((container, index) => {
        setTimeout(() => {
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 100 * (index + 1));
    });

    // Efectos hover para los contenedores
    graficosContainers.forEach(container => {
        container.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = 'var(--shadow-lg)';
            this.style.transition = 'all 0.3s ease';
        });

        container.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'var(--shadow-md)';
            this.style.transition = 'all 0.3s ease';
        });
    });

    // Animación al hacer scroll
    function animateOnScroll() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                    
                    // Animar gráficos si usan Plotly
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
            threshold: 0.1,
            rootMargin: '0px'
        });

        graficosContainers.forEach(chart => observer.observe(chart));
    }

    // Iniciar animaciones
    animateOnScroll();

    // Añadir animación de rotación al botón de refresh
    const style = document.createElement('style');
    style.textContent = `
        .rotating {
            animation: rotate 1s linear infinite;
        }
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
}); 