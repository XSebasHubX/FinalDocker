document.addEventListener('DOMContentLoaded', function() {
    // Inicialización de variables y elementos
    const periodoSelect = document.getElementById('periodoSelect');
    const graficosContainers = document.querySelectorAll('.grafico-container');
    
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
});
