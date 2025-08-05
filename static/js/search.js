// Búsqueda en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('#search-input') || document.querySelector('.search-form input');
    const searchInputMobile = document.querySelector('#search-input-mobile');
    const searchInputMobileInline = document.querySelector('#search-input-mobile-inline');
    const searchForm = document.querySelector('.search-form');
    const searchFormMobile = document.querySelector('.search-form-mobile');
    const searchFormMobileInline = document.querySelector('.search-form-mobile-inline');
    const superior = document.querySelector('.superior');
    const searchIconDesktop = document.querySelector('#search-icon-desktop');
    const searchCloseDesktop = document.querySelector('#search-close-desktop');
    const searchCloseMobileInline = document.querySelector('#search-close-mobile-inline');
    
    // Desactivar autocompletado del navegador
    if (searchInput) {
        searchInput.setAttribute('autocomplete', 'off');
    }
    if (searchInputMobile) {
        searchInputMobile.setAttribute('autocomplete', 'off');
    }
    if (searchInputMobileInline) {
        searchInputMobileInline.setAttribute('autocomplete', 'off');
    }
    
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
        if (searchInputMobile) {
            searchInputMobile.value = queryParam;
        }
        if (searchInputMobileInline) {
            searchInputMobileInline.value = queryParam;
        }
        if (isDesktop()) {
            expandSearch();
        } else {
            expandSearchMobile();
        }
    }
    let searchTimeout;
    let searchDropdown;
    let searchDropdownMobile;

    // Crear el dropdown si no existe
    function createDropdown() {
        if (!searchDropdown) {
            searchDropdown = document.createElement('div');
            searchDropdown.className = 'search-dropdown';
            searchForm.appendChild(searchDropdown);
        }
        return searchDropdown;
    }

    // Crear el dropdown móvil si no existe
    function createDropdownMobile() {
        if (!searchDropdownMobile) {
            // Primero intentar encontrar el dropdown móvil inline
            searchDropdownMobile = document.querySelector('#search-dropdown-mobile-inline');
            
            // Si no existe, buscar el dropdown móvil normal
            if (!searchDropdownMobile) {
                searchDropdownMobile = document.querySelector('#search-dropdown-mobile');
            }
        }
        return searchDropdownMobile;
    }

    // Funciones para manejar la expansión de búsqueda en desktop
    function expandSearch() {
        if (window.innerWidth > 1024 && superior) {
            superior.classList.add('search-active');
            searchInput.focus();
        }
    }

    function collapseSearch() {
        if (superior) {
            superior.classList.remove('search-active');
        }
        hideDropdown();
        // Limpiar el input al colapsar
        searchInput.value = '';
    }

    // Funciones para manejar la expansión de búsqueda en móvil/tablet
    function expandSearchMobile() {
        if (window.innerWidth <= 1024 && superior) {
            superior.classList.add('search-active-mobile');
            searchInputMobileInline.focus();
        }
    }

    function collapseSearchMobile() {
        if (superior) {
            superior.classList.remove('search-active-mobile');
        }
        hideDropdown();
        // Limpiar el input al colapsar
        if (searchInputMobileInline) {
            searchInputMobileInline.value = '';
        }
    }

    function isDesktop() {
        return window.innerWidth > 1024;
    }

    // Realizar búsqueda
    function realizarBusqueda(query, isMobile = false) {
        if (query.length < 1) {
            hideDropdown(isMobile);
            return;
        }

        fetch(`/api/buscar/?q=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                mostrarResultados(data.productos, isMobile);
            })
            .catch(error => {
                console.error('Error en la búsqueda:', error);
                const dropdown = isMobile ? createDropdownMobile() : createDropdown();
                if (dropdown) {
                    dropdown.innerHTML = '<div class="no-results">Error en la búsqueda</div>';
                    dropdown.classList.add('show');
                }
            });
    }

    // Mostrar resultados
    function mostrarResultados(productos, isMobile = false) {
        const dropdown = isMobile ? createDropdownMobile() : createDropdown();
        
        if (!dropdown) return;
        
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
    function hideDropdown(isMobile = false) {
        const dropdown = isMobile ? searchDropdownMobile : searchDropdown;
        if (dropdown) {
            dropdown.classList.remove('show');
            dropdown.innerHTML = '';
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

    // Event listener para búsqueda móvil (si existe)
    if (searchInputMobile) {
        searchInputMobile.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            
            // Limpiar timeout anterior
            clearTimeout(searchTimeout);
            
            // Si el campo está vacío, ocultar dropdown
            if (query.length === 0) {
                hideDropdown(true);
                return;
            }
            
            // Establecer nuevo timeout para búsqueda móvil
            searchTimeout = setTimeout(() => {
                realizarBusqueda(query, true);
            }, 300);
        });

        // Sincronizar formularios al enviar
        if (searchFormMobile) {
            searchFormMobile.addEventListener('submit', function(e) {
                const query = searchInputMobile.value.trim();
                if (query.length > 0) {
                    return true;
                } else {
                    e.preventDefault();
                }
            });
        }
    }

    // Event listener para búsqueda móvil inline (nuevo)
    if (searchInputMobileInline) {
        searchInputMobileInline.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            
            // Limpiar timeout anterior
            clearTimeout(searchTimeout);
            
            // Si el campo está vacío, ocultar dropdown
            if (query.length === 0) {
                hideDropdown(true);
                return;
            }
            
            // Establecer nuevo timeout para búsqueda móvil
            searchTimeout = setTimeout(() => {
                realizarBusqueda(query, true);
            }, 300);
        });

        // Sincronizar formularios al enviar
        if (searchFormMobileInline) {
            searchFormMobileInline.addEventListener('submit', function(e) {
                const query = searchInputMobileInline.value.trim();
                if (query.length > 0) {
                    return true;
                } else {
                    e.preventDefault();
                }
            });
        }
    }

    // Ocultar dropdown al hacer click fuera
    document.addEventListener('click', function(e) {
        const isClickInsideDesktopSearch = searchForm.contains(e.target) || 
            (searchIconDesktop && searchIconDesktop.contains(e.target)) ||
            (searchCloseDesktop && searchCloseDesktop.contains(e.target));
            
        const isClickInsideMobileSearch = (searchFormMobileInline && searchFormMobileInline.contains(e.target)) ||
            (searchCloseMobileInline && searchCloseMobileInline.contains(e.target));

        if (!isClickInsideDesktopSearch && !isClickInsideMobileSearch) {
            if (isDesktop()) {
                collapseSearch();
            } else {
                collapseSearchMobile();
                hideDropdown();
                // No limpiar el campo si estamos en la página "Ver Todo" con una búsqueda activa
                const urlParams = new URLSearchParams(window.location.search);
                const queryParam = urlParams.get('q');
                if (!queryParam || window.location.pathname !== '/ver-todo/') {
                    if (searchInput) {
                        searchInput.value = '';
                    }
                }
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

    // Event listener para el icono de búsqueda de desktop
    if (searchIconDesktop) {
        searchIconDesktop.addEventListener('click', function(e) {
            e.preventDefault();
            if (isDesktop()) {
                expandSearch();
            }
        });
    }

    // Event listener para el botón de cerrar búsqueda de desktop
    if (searchCloseDesktop) {
        searchCloseDesktop.addEventListener('click', function(e) {
            e.preventDefault();
            if (isDesktop()) {
                collapseSearch();
            }
        });
    }

    // Event listener para el botón de cerrar búsqueda móvil/tablet
    if (searchCloseMobileInline) {
        searchCloseMobileInline.addEventListener('click', function(e) {
            e.preventDefault();
            if (!isDesktop()) {
                collapseSearchMobile();
            }
        });
    }

    // Event listeners para búsqueda móvil inline
    if (searchInputMobileInline) {
        searchInputMobileInline.addEventListener('input', function(e) {
            if (!isDesktop()) {
                const query = e.target.value.trim();
                if (query.length >= 1) {
                    realizarBusqueda(query);
                } else {
                    hideDropdown();
                }
            }
        });

        searchInputMobileInline.addEventListener('focus', function(e) {
            if (!isDesktop()) {
                expandSearchMobile();
            }
            const query = e.target.value.trim();
            if (query.length >= 1) {
                realizarBusqueda(query);
            }
        });

        searchInputMobileInline.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                e.target.value = '';
                if (!isDesktop()) {
                    collapseSearchMobile();
                } else {
                    hideDropdown();
                }
            }
        });
    }

    // Event listener para el formulario móvil inline
    if (searchFormMobileInline) {
        searchFormMobileInline.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = searchInputMobileInline.value.trim();
            if (query) {
                window.location.href = `/ver-todo/?q=${encodeURIComponent(query)}`;
            }
        });
    }

    // Mostrar dropdown al hacer focus en el input (si ya hay texto)
    searchInput.addEventListener('focus', function(e) {
        if (isDesktop()) {
            expandSearch();
        }
        const query = e.target.value.trim();
        if (query.length >= 1) {
            realizarBusqueda(query);
        }
    });

    // Limpiar campo al presionar Escape
    searchInput.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            e.target.value = '';
            if (isDesktop()) {
                collapseSearch();
            } else {
                hideDropdown();
            }
        }
    });

    // Manejar cambios de tamaño de ventana
    window.addEventListener('resize', function() {
        if (!isDesktop() && superior) {
            collapseSearch();
        }
    });
});
