// Búsqueda en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('#search-input') || document.querySelector('.search-form input');
    const searchForm = document.querySelector('.search-form');
    
    // Verificar que los elementos existen
    if (!searchInput || !searchForm) {
        console.error('Elementos de búsqueda no encontrados');
        return;
    }

    // Preservar valor de búsqueda si viene de URL
    const urlParams = new URLSearchParams(window.location.search);
    const queryParam = urlParams.get('q');
    if (queryParam) {
        searchInput.value = queryParam;
    }
    let searchTimeout;
    let searchDropdown;

    // Crear el dropdown si no existe
    function createDropdown() {
        if (!searchDropdown) {
            searchDropdown = document.createElement('div');
            searchDropdown.className = 'search-dropdown';
            searchForm.appendChild(searchDropdown);
        }
        return searchDropdown;
    }

    // Realizar búsqueda
    function realizarBusqueda(query) {
        if (query.length < 1) {
            hideDropdown();
            return;
        }

        console.log('Buscando:', query); // Debug

        fetch(`/api/buscar/?q=${encodeURIComponent(query)}`)
            .then(response => {
                console.log('Respuesta recibida:', response.status); // Debug
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Datos recibidos:', data); // Debug
                mostrarResultados(data.productos);
            })
            .catch(error => {
                console.error('Error en la búsqueda:', error);
                const dropdown = createDropdown();
                dropdown.innerHTML = '<div class="no-results">Error en la búsqueda</div>';
                dropdown.classList.add('show');
            });
    }

    // Mostrar resultados
    function mostrarResultados(productos) {
        const dropdown = createDropdown();
        
        if (productos.length === 0) {
            dropdown.innerHTML = '<div class="no-results">No se encontraron productos</div>';
        } else {
            const resultadosHTML = productos.map(producto => `
                <a href="/producto/${producto.id}/" class="search-result-item">
                    <img src="${producto.imagen_url}" alt="${producto.nombre}" class="search-result-img">
                    <div class="search-result-info">
                        <div class="search-result-name">${producto.nombre}</div>
                        <div class="search-result-price">$${formatearPrecio(producto.precio)}</div>
                    </div>
                </a>
            `).join('');
            
            dropdown.innerHTML = resultadosHTML;
        }
        
        dropdown.classList.add('show');
    }

    // Ocultar dropdown
    function hideDropdown() {
        if (searchDropdown) {
            searchDropdown.classList.remove('show');
            // Limpiar contenido para liberar memoria
            searchDropdown.innerHTML = '';
        }
    }

    // Formatear precio
    function formatearPrecio(precio) {
        return new Intl.NumberFormat('es-CL').format(precio);
    }

    // Event listeners
    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.trim();
        
        // Limpiar timeout anterior para evitar peticiones innecesarias
        clearTimeout(searchTimeout);
        
        // Si el campo está vacío, ocultar dropdown inmediatamente
        if (query.length === 0) {
            hideDropdown();
            return;
        }
        
        // Establecer nuevo timeout para evitar demasiadas peticiones
        searchTimeout = setTimeout(() => {
            realizarBusqueda(query);
        }, 300);
    });

    // Ocultar dropdown al hacer click fuera
    document.addEventListener('click', function(e) {
        if (!searchForm.contains(e.target)) {
            hideDropdown();
            // No limpiar el campo si estamos en la página "Ver Todo" con una búsqueda activa
            const urlParams = new URLSearchParams(window.location.search);
            const queryParam = urlParams.get('q');
            if (!queryParam || window.location.pathname !== '/ver-todo/') {
                searchInput.value = '';
            }
        }
    });

    // Manejar envío del formulario (Enter)
    searchForm.addEventListener('submit', function(e) {
        const query = searchInput.value.trim();
        if (query.length > 0) {
            // Permitir que el formulario se envíe normalmente para ir a "Ver Todo"
            return true;
        } else {
            // Si no hay texto, prevenir envío
            e.preventDefault();
        }
    });

    // Mostrar dropdown al hacer focus en el input (si ya hay texto)
    searchInput.addEventListener('focus', function(e) {
        const query = e.target.value.trim();
        if (query.length >= 1) {
            realizarBusqueda(query);
        }
    });

    // Limpiar campo al presionar Escape
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            e.target.value = '';
            hideDropdown();
        }
    });
});
