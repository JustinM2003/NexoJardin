// Manejo de modales y formularios para productos y categorías

// Función para actualizar el nombre del archivo en el modal de agregar
function updateFileName(input) {
    const fileNameDisplay = document.getElementById('file-name-display');
    const uploadBox = input.parentElement.querySelector('.image-upload-box');
    const uploadIcon = uploadBox.querySelector('.upload-icon');
    const btnEliminar = document.getElementById('btn-eliminar-imagen');
    
    if (input.files && input.files[0]) {
        const fileName = input.files[0].name;
        // Limpiar completamente el contenido antes de agregar el nuevo
        fileNameDisplay.innerHTML = '';
        fileNameDisplay.innerHTML = `Archivo seleccionado:<br><strong>${fileName}</strong>`;
        uploadBox.style.borderColor = '#28a745';
        uploadBox.style.backgroundColor = '#f8fff9';
        uploadIcon.textContent = '✅';
        uploadIcon.style.color = '#28a745';
        
        // Mostrar botón de eliminar
        if (btnEliminar) {
            btnEliminar.style.display = 'block';
        }
    } else {
        // Limpiar completamente el contenido antes de restaurar el original
        fileNameDisplay.innerHTML = '';
        fileNameDisplay.innerHTML = 'Haz clic para seleccionar una imagen<br>o arrastra y suelta aquí';
        uploadBox.style.borderColor = '#ccc';
        uploadBox.style.backgroundColor = '#f9f9f9';
        uploadIcon.textContent = '📁';
        uploadIcon.style.color = '#666';
        
        // Ocultar botón de eliminar
        if (btnEliminar) {
            btnEliminar.style.display = 'none';
        }
    }
}

// Función para actualizar el nombre del archivo en el modal de editar
function updateFileNameEdit(input) {
    const fileNameDisplay = document.getElementById('file-name-display-edit');
    const uploadBox = input.parentElement.querySelector('.image-upload-box');
    const uploadIcon = uploadBox?.querySelector('.upload-icon');
    const btnEliminar = document.getElementById('btn-eliminar-imagen-edit');
    const eliminarImagenHidden = document.getElementById('eliminar_imagen_hidden');
    
    if (input.files && input.files[0]) {
        const fileName = input.files[0].name;
        
        // Desmarcar eliminación si se selecciona nueva imagen
        if (eliminarImagenHidden) {
            eliminarImagenHidden.value = 'false';
        }
        
        if (fileNameDisplay) {
            fileNameDisplay.innerHTML = `Nuevo archivo:<br><strong>${fileName}</strong>`;
        }
        
        if (uploadBox) {
            uploadBox.style.borderColor = '#28a745';
            uploadBox.style.backgroundColor = '#f8fff9';
        }
        
        if (uploadIcon) {
            uploadIcon.textContent = '✅';
            uploadIcon.style.color = '#28a745';
        }
        
        // Mostrar botón de eliminar
        if (btnEliminar) {
            btnEliminar.style.display = 'block';
        }
    } else {
        // Verificar si está marcado para eliminar
        const eliminarMarcado = eliminarImagenHidden && eliminarImagenHidden.value === 'true';
        
        if (eliminarMarcado) {
            // Mantener estado de eliminación
            if (fileNameDisplay) {
                fileNameDisplay.innerHTML = 'Imagen eliminada<br><span style="color: #dc3545; font-size: 0.8em;">Se eliminará al guardar</span>';
            }
            
            if (uploadBox) {
                uploadBox.style.borderColor = '#dc3545';
                uploadBox.style.backgroundColor = '#fff5f5';
            }
            
            if (uploadIcon) {
                uploadIcon.textContent = '🗑️';
                uploadIcon.style.color = '#dc3545';
            }
        } else {
            // Estado normal sin imagen
            if (fileNameDisplay) {
                fileNameDisplay.innerHTML = 'Haz clic para seleccionar una imagen';
            }
            
            if (uploadBox) {
                uploadBox.style.borderColor = '#ccc';
                uploadBox.style.backgroundColor = '#f9f9f9';
            }
            
            if (uploadIcon) {
                uploadIcon.textContent = '📁';
                uploadIcon.style.color = '#666';
            }
        }
        
        // Ocultar botón de eliminar
        if (btnEliminar) {
            btnEliminar.style.display = 'none';
        }
    }
}

// Función para resetear el estado del upload de archivo
function resetFileUpload() {
    const fileInput = document.getElementById('id_imagen');
    const fileNameDisplay = document.getElementById('file-name-display');
    const uploadBox = document.querySelector('.image-upload-box');
    const uploadIcon = uploadBox?.querySelector('.upload-icon');
    const btnEliminar = document.getElementById('btn-eliminar-imagen');
    
    if (fileInput) {
        fileInput.value = '';
    }
    
    if (fileNameDisplay) {
        fileNameDisplay.innerHTML = 'Haz clic para seleccionar una imagen<br>o arrastra y suelta aquí';
    }
    
    if (uploadBox) {
        uploadBox.style.borderColor = '#ccc';
        uploadBox.style.backgroundColor = '#f9f9f9';
    }
    
    if (uploadIcon) {
        uploadIcon.textContent = '📁';
        uploadIcon.style.color = '#666';
    }
    
    // Ocultar botón de eliminar
    if (btnEliminar) {
        btnEliminar.style.display = 'none';
    }
}

// Función para eliminar imagen en modal de agregar
function eliminarImagen() {
    const fileInput = document.getElementById('id_imagen');
    if (fileInput) {
        fileInput.value = '';
        // Disparar el evento change para actualizar la UI
        const event = new Event('change', { bubbles: true });
        fileInput.dispatchEvent(event);
    }
}

// Función para eliminar imagen en modal de editar
function eliminarImagenEdit() {
    const fileInput = document.getElementById('id_imagen_edit');
    const fileNameDisplay = document.getElementById('file-name-display-edit');
    const uploadBox = document.querySelector('#modalEditarProducto .image-upload-box');
    const uploadIcon = uploadBox?.querySelector('.upload-icon');
    const btnEliminar = document.getElementById('btn-eliminar-imagen-edit');
    const eliminarImagenHidden = document.getElementById('eliminar_imagen_hidden');
    
    if (fileInput) {
        fileInput.value = '';
    }
    
    // Marcar que se debe eliminar la imagen
    if (eliminarImagenHidden) {
        eliminarImagenHidden.value = 'true';
    }
    
    if (fileNameDisplay) {
        fileNameDisplay.innerHTML = 'Imagen eliminada<br><span style="color: #dc3545; font-size: 0.8em;">Se eliminará al guardar</span>';
    }
    
    if (uploadBox) {
        uploadBox.style.borderColor = '#dc3545';
        uploadBox.style.backgroundColor = '#fff5f5';
    }
    
    if (uploadIcon) {
        uploadIcon.textContent = '🗑️';
        uploadIcon.style.color = '#dc3545';
    }
    
    // Ocultar botón de eliminar
    if (btnEliminar) {
        btnEliminar.style.display = 'none';
    }
}

// Función para restaurar imagen en modal de editar
function restaurarImagenEdit() {
    const fileInput = document.getElementById('id_imagen_edit');
    const fileNameDisplay = document.getElementById('file-name-display-edit');
    const uploadBox = document.querySelector('#modalEditarProducto .image-upload-box');
    const uploadIcon = uploadBox?.querySelector('.upload-icon');
    const btnEliminar = document.getElementById('btn-eliminar-imagen-edit');
    const btnRestaurar = document.getElementById('btn-restaurar-imagen-edit');
    const eliminarImagenHidden = document.getElementById('eliminar_imagen_hidden');
    
    // Desmarcar eliminación
    if (eliminarImagenHidden) {
        eliminarImagenHidden.value = 'false';
    }
    
    // Restaurar el estado original
    if (fileNameDisplay) {
        fileNameDisplay.innerHTML = 'Imagen actual<br>Haz clic o arrastra para cambiar';
    }
    
    if (uploadBox) {
        uploadBox.style.borderColor = '#ccc';
        uploadBox.style.backgroundColor = '#f9f9f9';
    }
    
    if (uploadIcon) {
        uploadIcon.textContent = '📁';
        uploadIcon.style.color = '#666';
    }
    
    // Mostrar botón de eliminar y ocultar botón de restaurar
    if (btnEliminar) {
        btnEliminar.style.display = 'block';
    }
    if (btnRestaurar) {
        btnRestaurar.style.display = 'none';
    }
}

// Función para manejar drag and drop
function setupDragAndDrop() {
    const uploadBoxes = document.querySelectorAll('.image-upload-box');
    
    uploadBoxes.forEach(uploadBox => {
        // Prevenir comportamiento por defecto
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadBox.addEventListener(eventName, preventDefaults, false);
        });
        
        // Destacar zona de drop
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadBox.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadBox.addEventListener(eventName, unhighlight, false);
        });
        
        // Manejar drop
        uploadBox.addEventListener('drop', handleDrop, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function highlight(e) {
        e.currentTarget.style.borderColor = '#007bff';
        e.currentTarget.style.backgroundColor = '#e3f2fd';
    }
    
    function unhighlight(e) {
        e.currentTarget.style.borderColor = '#ccc';
        e.currentTarget.style.backgroundColor = '#f9f9f9';
    }
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            // Buscar el input de imagen más cercano o el del modal activo
            let fileInput = null;
            
            // Si estamos en el modal de edición, usar el input de edición
            const modalEditarVisible = document.getElementById('modalEditarProducto')?.style.display === 'flex';
            if (modalEditarVisible) {
                fileInput = document.getElementById('id_imagen_edit');
            } else {
                // Si no, usar el input del modal de agregar
                fileInput = document.getElementById('id_imagen');
            }
            
            if (fileInput) {
                fileInput.files = files;
                // Disparar el evento change
                const event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        }
    }
}

// Función global para recargar categorías
window.recargarCategorias = async function(tipo = null) {
    try {
        // Detectar el tipo desde la URL si no se especifica
        if (!tipo) {
            const currentPath = window.location.pathname;
            if (currentPath.includes('plantas')) {
                tipo = 'planta';
            } else if (currentPath.includes('materiales')) {
                tipo = 'material';
            }
        }
        
        let url = '/agregar-categoria/';
        if (tipo) {
            url += `?tipo=${tipo}`;
        }
        
        const response = await fetch(url, {
            method: 'GET',
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        if (response.ok) {
            const result = await response.json();
            if (result.categorias) {
                actualizarListaCategorias(result.categorias);
            }
        }
    } catch (error) {
        console.error('Error al recargar categorías:', error);
    }
};

// Función para actualizar la lista de categorías en el DOM
function actualizarListaCategorias(categorias) {
    const lista = document.querySelector('.lista-categorias');
    if (lista) {
        lista.innerHTML = '';
        // Obtener el token CSRF del DOM
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
        categorias.forEach(cat => {
            const item = document.createElement('li');
            item.className = 'item-categoria';
            item.innerHTML = `
                <span>${cat.nombre}</span>
                <form class="form-eliminar-categoria" action="/eliminar_categoria/${cat.id}/" method="post">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
                    <button type="submit" class="btn-eliminar-categoria">Eliminar</button>
                </form>
            `;
            lista.appendChild(item);
        });
        
        // Eliminar posibles duplicados de eventos
        lista.querySelectorAll('.form-eliminar-categoria').forEach(form => {
            form.onsubmit = null;
            form.addEventListener('submit', async function(e) {
                e.preventDefault();
                const data = new FormData(form);
                
                // Detectar el tipo desde la URL actual
                const currentPath = window.location.pathname;
                let tipo = null;
                if (currentPath.includes('plantas')) {
                    tipo = 'planta';
                } else if (currentPath.includes('materiales')) {
                    tipo = 'material';
                }
                
                if (tipo) {
                    data.append('tipo', tipo);
                }
                
                const response = await fetch(form.getAttribute('action'), {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken
                    },
                    body: data
                });
                if (response.ok) {
                    const result = await response.json();
                    // Actualizar la lista SIEMPRE, aunque no venga la clave categorias
                    if (result.categorias) {
                        actualizarListaCategorias(result.categorias);
                    } else if (Array.isArray(result)) {
                        actualizarListaCategorias(result);
                    } else {
                        // Si no viene nada, forzar recarga de la lista desde backend
                        window.recargarCategorias(tipo);
                    }
                }
            });
        });
    }
    
    // Actualizar el <select> de categorías en los formularios de productos
    document.querySelectorAll('select[name="categoria"]').forEach(select => {
        const valorSeleccionado = select.value;
        select.innerHTML = '<option value="">---------</option>';
        categorias.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.textContent = cat.nombre;
            if (cat.id == valorSeleccionado) option.selected = true;
            select.appendChild(option);
        });
    });
    
    // También actualizar selects en modales que puedan estar abiertos
    actualizarSelectsCategoriaModales(categorias);
}

// Función para actualizar selects de categorías en modales
function actualizarSelectsCategoriaModales(categorias) {
    // Detectar el tipo de página actual para filtrar correctamente
    const currentPath = window.location.pathname;
    let tipoActual = null;
    if (currentPath.includes('plantas')) {
        tipoActual = 'planta';
    } else if (currentPath.includes('materiales')) {
        tipoActual = 'material';
    }
    
    // Solo actualizar select en modal de edición si no está ya cargado desde el servidor
    const selectEditarProducto = document.querySelector('#modalEditarProducto select[name="categoria"]');
    const modalEditarVisible = document.getElementById('modalEditarProducto')?.style.display === 'flex';
    
    if (selectEditarProducto && !modalEditarVisible) {
        // Solo actualizar si el modal no está visible
        actualizarSelectConFiltro(selectEditarProducto, categorias, tipoActual);
    }
    
    // Actualizar select en modal de agregar producto
    const selectAgregarProducto = document.querySelector('#modalProducto select[name="categoria"]');
    if (selectAgregarProducto) {
        actualizarSelectConFiltro(selectAgregarProducto, categorias, tipoActual);
    }
    
    // Actualizar select en modal de eliminar categorías
    const selectEliminarCategoria = document.querySelector('#modalEliminarCategoria select[name="categoria_id"]');
    if (selectEliminarCategoria) {
        const valorSeleccionado = selectEliminarCategoria.value;
        selectEliminarCategoria.innerHTML = '<option value="">Selecciona categoría</option>';
        categorias.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.id;
            option.textContent = cat.nombre;
            if (cat.id == valorSeleccionado) option.selected = true;
            selectEliminarCategoria.appendChild(option);
        });
    }
}

// Función auxiliar para actualizar un select con filtro de tipo
function actualizarSelectConFiltro(select, categorias, tipoFiltro) {
    const valorSeleccionado = select.value;
    select.innerHTML = '<option value="">---------</option>';
    
    // Si tenemos un tipo de filtro, usar solo las categorías que ya están en la página
    // En lugar de filtrar por tipo aquí, preservar el comportamiento original del backend
    categorias.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat.id;
        option.textContent = cat.nombre;
        if (cat.id == valorSeleccionado) option.selected = true;
        select.appendChild(option);
    });
}

// FUNCIONES PARA FILTROS PERSONALIZADOS
function toggleDropdown(tipo) {
    // Cerrar todos los dropdowns
    document.querySelectorAll('.custom-dropdown').forEach(dropdown => {
        dropdown.classList.remove('active');
    });
    
    // Abrir el dropdown seleccionado
    const dropdown = document.getElementById(`dropdown-${tipo}`);
    if (dropdown) {
        dropdown.classList.add('active');
    }
}

function setFiltro(tipo, valor) {
    const url = new URL(window.location);
    
    // Limpiar el parámetro
    url.searchParams.delete(tipo);
    
    // Agregar el nuevo valor si no está vacío
    if (valor) {
        url.searchParams.set(tipo, valor);
    }
    
    // Cerrar dropdown
    document.querySelectorAll('.custom-dropdown').forEach(dropdown => {
        dropdown.classList.remove('active');
    });
    
    // Actualizar la página
    window.location.href = url.toString();
}

function setFiltroOrden(valor, texto) {
    const url = new URL(window.location);
    
    // Limpiar el parámetro
    url.searchParams.delete('orden_precio');
    
    // Agregar el nuevo valor si no está vacío
    if (valor) {
        url.searchParams.set('orden_precio', valor);
    }
    
    // Actualizar el texto del botón
    const ordenSelected = document.getElementById('orden-selected');
    if (ordenSelected) {
        ordenSelected.textContent = texto;
    }
    
    // Cerrar dropdown
    document.querySelectorAll('.custom-dropdown').forEach(dropdown => {
        dropdown.classList.remove('active');
    });
    
    // Actualizar la página
    window.location.href = url.toString();
}

// Función para inicializar los textos de los filtros según la URL actual
function inicializarFiltros() {
    const url = new URL(window.location);
    
    // Inicializar filtro de tipo
    const tipoParam = url.searchParams.get('tipo');
    const tipoSelected = document.getElementById('tipo-selected');
    if (tipoSelected) {
        if (tipoParam === 'planta') {
            tipoSelected.textContent = 'plantas';
        } else if (tipoParam === 'material') {
            tipoSelected.textContent = 'materiales';
        } else {
            tipoSelected.textContent = 'tipo';
        }
    }
    
    // Inicializar filtro de categoría
    const categoriaParam = url.searchParams.get('categoria');
    const categoriaSelected = document.getElementById('categoria-selected');
    if (categoriaSelected && categoriaParam) {
        // Buscar el nombre de la categoría seleccionada
        const dropdownItems = document.querySelectorAll('#dropdown-categoria .dropdown-item');
        dropdownItems.forEach(item => {
            if (item.getAttribute('onclick') && item.getAttribute('onclick').includes(`'${categoriaParam}'`)) {
                categoriaSelected.textContent = item.textContent.toLowerCase();
            }
        });
    }
    
    // Inicializar filtro de orden
    const ordenParam = url.searchParams.get('orden_precio');
    const ordenSelected = document.getElementById('orden-selected');
    if (ordenSelected) {
        if (ordenParam === 'menor') {
            ordenSelected.textContent = 'precio, menor a mayor';
        } else if (ordenParam === 'mayor') {
            ordenSelected.textContent = 'precio, mayor a menor';
        } else {
            ordenSelected.textContent = 'características';
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Carrusel de productos destacados (home)
    const carruselTrack = document.getElementById('carruselTrack');
    const carruselItems = carruselTrack ? carruselTrack.querySelectorAll('.carrusel-item') : [];
    let carruselIndex = 0;
    const itemsToShow = 4; // Siempre mostrar 4 en desktop
    function updateCarrusel() {
        if (!carruselTrack || carruselItems.length === 0) return;
        const style = window.getComputedStyle(carruselTrack);
        let gap = parseInt(style.gap) || 32;
        const itemWidth = carruselItems[0].getBoundingClientRect().width + gap;
        // Limitar el máximo a 10 productos desplazables
        const maxIndex = Math.max(0, Math.min(carruselItems.length - itemsToShow, 10 - itemsToShow));
        if (carruselIndex > maxIndex) carruselIndex = maxIndex;
        carruselTrack.style.transform = `translateX(-${carruselIndex * itemWidth}px)`;
    }

    window.moverCarrusel = function(direccion) {
        if (!carruselTrack || carruselItems.length === 0) return;
        const maxIndex = Math.max(0, Math.min(carruselItems.length - itemsToShow, 10 - itemsToShow));
        carruselIndex += direccion;
        if (carruselIndex < 0) carruselIndex = 0;
        if (carruselIndex > maxIndex) carruselIndex = maxIndex;
        updateCarrusel();
    };

    // Inicializar carrusel si existe
    if (carruselTrack && carruselItems.length > 0) {
        updateCarrusel();
        window.addEventListener('resize', updateCarrusel);
    }

    // Inicializar drag and drop para upload de imágenes
    setupDragAndDrop();

    // Inicializar filtros personalizados
    inicializarFiltros();

    // Cerrar dropdowns al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.custom-dropdown')) {
            document.querySelectorAll('.custom-dropdown').forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        }
    });

    // Modal Eliminar Producto
    window.abrirModalEliminarProducto = function(productoId, productoNombre) {
        const modal = document.getElementById('modalConfirmarEliminarProducto');
        const texto = document.getElementById('textoConfirmarEliminarProducto');
        texto.textContent = `¿Seguro que deseas eliminar el producto "${productoNombre}"?`;
        modal.style.display = 'flex';
        // Guardar el id en el formulario
        const form = document.getElementById('formConfirmarEliminarProducto');
        form.setAttribute('action', `/eliminar/${productoId}/`);
        // Cerrar modal
        document.getElementById('closeModalConfirmarEliminarProductoBtn').onclick = function() {
            modal.style.display = 'none';
        };
        document.getElementById('cancelarModalConfirmarEliminarProducto').onclick = function(e) {
            e.preventDefault();
            modal.style.display = 'none';
        };
        // Submit AJAX
        form.onsubmit = async function(e) {
            e.preventDefault();
            const data = new FormData(form);
            const resp = await fetch(form.getAttribute('action'), {
                method: 'POST',
                headers: { 'X-Requested-With': 'XMLHttpRequest' },
                body: data
            });
            if (resp.ok) {
                modal.style.display = 'none';
                form.reset();
                location.reload();
            }
        };
    };

    // Modal Editar Producto
    window.abrirModalEditarProducto = async function(productoId) {
        const modal = document.getElementById('modalEditarProducto');
        const content = document.getElementById('modalEditarProductoContent');
        modal.style.display = 'flex';
        content.innerHTML = '<div style="text-align:center;padding:2em;">Cargando...</div>';
        
        const response = await fetch(`/editar/${productoId}/`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        if (response.ok) {
            const html = await response.text();
            content.innerHTML = html;
            
            // Reinicializar drag and drop para el nuevo contenido del modal
            setupDragAndDrop();
            
            // No recargar categorías aquí porque el HTML ya viene con las categorías filtradas correctamente
            
            // Cerrar modal
            const cancelarBtn = document.getElementById('cancelarModalEditarProducto');
            if (cancelarBtn) {
                cancelarBtn.onclick = function(e) {
                    e.preventDefault();
                    modal.style.display = 'none';
                };
            }
            // Submit AJAX
            const form = document.getElementById('formEditarProducto');
            if (form) {
                form.onsubmit = async function(e) {
                    e.preventDefault();
                    const data = new FormData(form);
                    const resp = await fetch(form.getAttribute('data-url'), {
                        method: 'POST',
                        headers: { 'X-Requested-With': 'XMLHttpRequest' },
                        body: data
                    });
                    if (resp.ok) {
                        document.getElementById('mensajeExitoEditarProducto').style.display = 'block';
                        modal.style.display = 'none';
                        document.getElementById('mensajeExitoEditarProducto').style.display = 'none';
                        form.reset();
                        location.reload();
                    }
                };
            }
        } else {
            content.innerHTML = '<div style="color:red;text-align:center;padding:2em;">Error al cargar el formulario.</div>';
        }
        // Cerrar con X
        content.querySelectorAll('.modal-close').forEach(function(btn) {
            btn.onclick = function() {
                modal.style.display = 'none';
            };
        });
    };
    
    // Modal Producto
    document.getElementById('openModalProductoBtn').onclick = async function() {
      // No recargar categorías aquí porque el modal ya viene con las categorías correctas del template
      document.getElementById('modalProducto').style.display = 'flex';
    }
    document.getElementById('closeModalProductoBtn').onclick = function() {
      // Limpiar el estado del archivo al cerrar
      resetFileUpload();
      document.getElementById('modalProducto').style.display = 'none';
    }
    document.getElementById('cancelarModalProducto').onclick = function(e) {
      e.preventDefault();
      // Limpiar el estado del archivo al cancelar
      resetFileUpload();
      document.getElementById('modalProducto').style.display = 'none';
    }
    document.getElementById('formProducto').onsubmit = async function(e) {
      e.preventDefault();
      const form = e.target;
      const data = new FormData(form);
      const response = await fetch(form.getAttribute('data-url'), {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: data
      });
      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          document.getElementById('modalProducto').style.display = 'none';
          form.reset();
          resetFileUpload();
          location.reload();
        } else {
          const mensajeError = document.getElementById('mensajeErrorProducto');
          mensajeError.textContent = 'Completa todos los campos obligatorios correctamente.';
          mensajeError.style.display = 'block';
        }
      } else {
        const mensajeError = document.getElementById('mensajeErrorProducto');
        mensajeError.textContent = 'Error al guardar el producto.';
        mensajeError.style.display = 'block';
      }
    }
    
    // Modal Categoría
    document.getElementById('openModalCategoriaBtn').onclick = function() {
      // Limpiar mensajes al abrir
      document.getElementById('mensajeErrorCategoria').style.display = 'none';
      document.getElementById('modalCategoria').style.display = 'flex';
    }
    document.getElementById('closeModalCategoriaBtn').onclick = function() {
      // Limpiar mensajes al cerrar
      document.getElementById('mensajeErrorCategoria').style.display = 'none';
      document.getElementById('modalCategoria').style.display = 'none';
    }
    document.getElementById('cancelarModalCategoria').onclick = function(e) {
      e.preventDefault();
      // Limpiar mensajes al cancelar
      document.getElementById('mensajeErrorCategoria').style.display = 'none';
      document.getElementById('modalCategoria').style.display = 'none';
    }
    document.getElementById('formCategoria').onsubmit = async function(e) {
      e.preventDefault();
      const form = e.target;
      
      // Validación del lado del cliente
      const nombreInput = document.getElementById('id_nombre_categoria');
      if (!nombreInput.value.trim()) {
        const mensajeError = document.getElementById('mensajeErrorCategoria');
        mensajeError.textContent = 'El nombre de la categoría es obligatorio.';
        mensajeError.style.display = 'block';
        nombreInput.focus();
        return;
      }
      
      const data = new FormData(form);
      
      // Ocultar mensajes previos
      document.getElementById('mensajeErrorCategoria').style.display = 'none';
      
      const response = await fetch(form.getAttribute('data-url'), {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
        body: data
      });
      if (response.ok) {
        const result = await response.json();
        if (result.success) {
          document.getElementById('mensajeExitoCategoria').style.display = 'block';
          document.getElementById('modalCategoria').style.display = 'none';
          setTimeout(() => {
            document.getElementById('mensajeExitoCategoria').style.display = 'none';
          }, 3000);
          form.reset();
          // Actualizar la lista y el select inmediatamente
          if (result.categorias && Array.isArray(result.categorias)) {
            actualizarListaCategorias(result.categorias);
          }
        } else {
          const mensajeError = document.getElementById('mensajeErrorCategoria');
          mensajeError.textContent = 'Error al agregar la categoría. Verifica que el nombre no esté duplicado.';
          mensajeError.style.display = 'block';
        }
      } else {
        const mensajeError = document.getElementById('mensajeErrorCategoria');
        mensajeError.textContent = 'Error al guardar la categoría.';
        mensajeError.style.display = 'block';
      }
    }
    
    // Modal Eliminar Categoría
    document.getElementById('openModalEliminarCategoriaBtn').onclick = async function() {
        // Limpiar mensajes al abrir
        document.getElementById('mensajeErrorEliminarCategoria').style.display = 'none';
        // Recargar categorías antes de abrir el modal para tener la lista actualizada
        await window.recargarCategorias();
        document.getElementById('modalEliminarCategoria').style.display = 'flex';
    }
    document.getElementById('closeModalEliminarCategoriaBtn').onclick = function() {
        // Limpiar mensajes al cerrar
        document.getElementById('mensajeErrorEliminarCategoria').style.display = 'none';
        document.getElementById('modalEliminarCategoria').style.display = 'none';
    }
    document.getElementById('cancelarModalEliminarCategoria').onclick = function(e) {
        e.preventDefault();
        // Limpiar mensajes al cancelar
        document.getElementById('mensajeErrorEliminarCategoria').style.display = 'none';
        document.getElementById('modalEliminarCategoria').style.display = 'none';
    }
    document.getElementById('formEliminarCategoria').onsubmit = async function(e) {
        e.preventDefault();
        const form = e.target;
        
        // Validación del lado del cliente
        const categoriaSelect = document.getElementById('id_categoria_eliminar');
        if (!categoriaSelect.value) {
            const mensajeError = document.getElementById('mensajeErrorEliminarCategoria');
            mensajeError.textContent = 'Debes seleccionar una categoría para eliminar.';
            mensajeError.style.display = 'block';
            categoriaSelect.focus();
            return;
        }
        
        const data = new FormData(form);
        
        // Ocultar mensajes previos
        document.getElementById('mensajeErrorEliminarCategoria').style.display = 'none';
        
        // Detectar el tipo desde la URL actual
        const currentPath = window.location.pathname;
        let tipo = null;
        if (currentPath.includes('plantas')) {
            tipo = 'planta';
        } else if (currentPath.includes('materiales')) {
            tipo = 'material';
        }
        
        if (tipo) {
            data.append('tipo', tipo);
        }
        
        const response = await fetch(form.getAttribute('action'), {
            method: 'POST',
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            body: data
        });
        if (response.ok) {
            const result = await response.json();
            document.getElementById('mensajeExitoEliminarCategoria').style.display = 'block';
            document.getElementById('modalEliminarCategoria').style.display = 'none';
            setTimeout(() => {
                document.getElementById('mensajeExitoEliminarCategoria').style.display = 'none';
            }, 3000);
            form.reset();
            // Actualizar la lista y el select inmediatamente
            if (result.categorias && Array.isArray(result.categorias)) {
                actualizarListaCategorias(result.categorias);
            }
        } else {
            const mensajeError = document.getElementById('mensajeErrorEliminarCategoria');
            mensajeError.textContent = 'Error al eliminar la categoría. Puede que esté siendo utilizada por productos.';
            mensajeError.style.display = 'block';
        }
    }
});
