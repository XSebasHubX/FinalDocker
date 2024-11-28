document.addEventListener('DOMContentLoaded', function() {
    // Función para ordenar la tabla
    function sortTable(n) {
        var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
        table = document.querySelector(".table");
        switching = true;
        dir = "asc";
        
        while (switching) {
            switching = false;
            rows = table.rows;
            
            for (i = 1; i < (rows.length - 1); i++) {
                shouldSwitch = false;
                x = rows[i].getElementsByTagName("TD")[n];
                y = rows[i + 1].getElementsByTagName("TD")[n];
                
                if (dir == "asc") {
                    if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                } else if (dir == "desc") {
                    if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                        shouldSwitch = true;
                        break;
                    }
                }
            }
            
            if (shouldSwitch) {
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
                switchcount++;
            } else {
                if (switchcount == 0 && dir == "asc") {
                    dir = "desc";
                    switching = true;
                }
            }
        }
    }

    // Agregar eventos de click a los encabezados de la tabla
    document.querySelectorAll('th').forEach((header, index) => {
        header.addEventListener('click', () => {
            sortTable(index);
        });
        header.style.cursor = 'pointer';
    });

    // Función para buscar en la tabla
    function searchTable() {
        let input = document.getElementById("searchInput");
        let filter = input.value.toUpperCase();
        let table = document.querySelector(".table");
        let tr = table.getElementsByTagName("tr");

        for (let i = 1; i < tr.length; i++) {
            let found = false;
            let td = tr[i].getElementsByTagName("td");
            
            for (let j = 0; j < td.length; j++) {
                let cell = td[j];
                if (cell) {
                    let textValue = cell.textContent || cell.innerText;
                    if (textValue.toUpperCase().indexOf(filter) > -1) {
                        found = true;
                        break;
                    }
                }
            }
            
            tr[i].style.display = found ? "" : "none";
        }
    }

    // Agregar campo de búsqueda al DOM
    const searchDiv = document.createElement('div');
    searchDiv.className = 'mb-3';
    searchDiv.innerHTML = `
        <input type="text" id="searchInput" class="form-control" placeholder="Buscar en el inventario...">
    `;
    document.querySelector('.container').insertBefore(searchDiv, document.querySelector('.table-container'));

    // Agregar evento de búsqueda
    document.getElementById('searchInput').addEventListener('keyup', searchTable);
}); 