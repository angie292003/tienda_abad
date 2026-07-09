// ===============================
// DATOS DEL USUARIO
// ===============================

const rolInput = document.getElementById("rolUsuario");
const usuarioInput = document.getElementById("usuarioActivo");

let rolUsuario = rolInput ? rolInput.value.trim().toLowerCase() : "cliente";
const usuarioActivo = usuarioInput ? usuarioInput.value.trim() : "Usuario";

if (rolUsuario === "admin") {
  rolUsuario = "administrador";
}

// ===============================
// ELEMENTOS PRINCIPALES
// ===============================

const contenidoApp = document.getElementById("contenidoApp");
const tituloVista = document.getElementById("tituloVista");
const descripcionVista = document.getElementById("descripcionVista");
const btnMenu = document.getElementById("btnMenu");
const sidebar = document.getElementById("sidebar");

// ===============================
// RUTAS DEL SPA
// ===============================

const datosVistas = {
  "#/inicio": {
    titulo: "Panel principal",
    descripcion: "Resumen general de la tienda y sus operaciones.",
    tipo: "inicio",
    roles: ["administrador", "trabajador", "cliente"],
  },

  "#/productos": {
    titulo: "Productos",
    descripcion: "Gestión y consulta de productos registrados.",
    archivo: "productos.html",
    roles: ["administrador", "trabajador", "cliente"],
  },

  "#/ventas": {
    titulo: "Ventas",
    descripcion: "Registro y consulta de ventas realizadas.",
    archivo: "ventas.html",
    roles: ["administrador", "trabajador"],
  },

  "#/proveedores": {
    titulo: "Proveedores",
    descripcion: "Administración de proveedores de la tienda.",
    archivo: "proveedores.html",
    roles: ["administrador", "trabajador"],
  },

  "#/tiendas": {
    titulo: "Tiendas",
    descripcion: "Administración y ubicación de tiendas registradas.",
    archivo: "tiendas.html",
    roles: ["administrador", "trabajador"],
  },

  "#/usuarios": {
    titulo: "Usuarios",
    descripcion: "Administración de usuarios y roles del sistema.",
    archivo: "usuarios.html",
    roles: ["administrador"],
  },

  "#/reportes": {
    titulo: "Reportes",
    descripcion: "Resumen de ventas, productos e inventario.",
    archivo: "reportes.html",
    roles: ["administrador", "trabajador"],
  },

  "#/carrito": {
    titulo: "Carrito",
    descripcion: "Productos seleccionados para compra.",
    archivo: "carrito.html",
    roles: ["administrador", "trabajador", "cliente"],
  },

  "#/perfil": {
    titulo: "Mi perfil",
    descripcion: "Información del usuario autenticado.",
    archivo: "perfil.html",
    roles: ["administrador", "trabajador", "cliente"],
  },

  "#/configuracion": {
    titulo: "Configuración",
    descripcion: "Opciones generales del sistema.",
    archivo: "configuracion.html",
    roles: ["administrador"],
  },
};

// ===============================
// NAVEGACIÓN PRINCIPAL
// ===============================

function navegar() {
  let ruta = window.location.hash || "#/inicio";

  if (!datosVistas[ruta]) {
    ruta = "#/inicio";
    window.location.hash = ruta;
  }

  const vista = datosVistas[ruta];

  if (!tienePermiso(vista.roles)) {
    mostrarAccesoDenegado(ruta);
    return;
  }

  cambiarEncabezado(vista.titulo, vista.descripcion);
  marcarMenuActivo(ruta);

  if (vista.tipo === "inicio") {
    vistaInicio();
    return;
  }

  cargarVistaHTML(vista.archivo);
}

function tienePermiso(rolesPermitidos) {
  return rolesPermitidos.includes(rolUsuario);
}

function cambiarEncabezado(titulo, descripcion) {
  if (tituloVista) {
    tituloVista.textContent = titulo;
  }

  if (descripcionVista) {
    descripcionVista.textContent = descripcion;
  }
}

function marcarMenuActivo(ruta) {
  const enlaces = document.querySelectorAll(".sidebar-menu a");

  enlaces.forEach((enlace) => {
    enlace.classList.remove("active");

    if (enlace.getAttribute("href") === ruta) {
      enlace.classList.add("active");
    }
  });
}

function mostrarAccesoDenegado(ruta) {
  cambiarEncabezado(
    "Acceso denegado",
    "No tienes permiso para acceder a este módulo.",
  );

  if (!contenidoApp) return;

  contenidoApp.innerHTML = `
    <div class="card">
      <h2>Acceso denegado</h2>

      <p>
        Tu rol actual es <strong>${rolUsuario}</strong>, por lo tanto
        no puedes ingresar a esta sección del sistema.
      </p>

      <button class="action-btn" onclick="window.location.hash='#/inicio'">
        Volver al inicio
      </button>
    </div>
  `;
}

// ===============================
// CARGA DE VISTAS HTML
// ===============================

async function cargarVistaHTML(archivo) {
  if (!contenidoApp) return;

  try {
    contenidoApp.innerHTML = `
      <div class="card">
        <h2>Cargando módulo...</h2>
        <p>Espere un momento.</p>
      </div>
    `;

    const response = await fetch(`/views/home/${archivo}`);

    if (!response.ok) {
      throw new Error("No se pudo cargar la vista.");
    }

    const html = await response.text();

    contenidoApp.innerHTML = html;

    ejecutarScriptsDeVista(contenidoApp);

    ejecutarAccionesDespuesDeCargar(archivo);
  } catch (error) {
    contenidoApp.innerHTML = `
      <div class="card">
        <h2>Error al cargar la vista</h2>

        <p>
          No se pudo cargar el archivo
          <strong>${archivo}</strong>.
        </p>

        <p>
          Revisa que exista dentro de:
          <strong>interface/templates/home/${archivo}</strong>
        </p>
      </div>
    `;
  }
}

function ejecutarScriptsDeVista(contenedor) {
  const scripts = contenedor.querySelectorAll("script");

  scripts.forEach((script) => {
    const nuevoScript = document.createElement("script");

    Array.from(script.attributes).forEach((attr) => {
      nuevoScript.setAttribute(attr.name, attr.value);
    });

    nuevoScript.textContent = script.textContent;

    script.replaceWith(nuevoScript);
  });
}

function ejecutarAccionesDespuesDeCargar(archivo) {
  if (archivo === "carrito.html") {
    actualizarBadgeCarrito();
  }
}

// ===============================
// VISTA INICIO
// ===============================

function vistaInicio() {
  cambiarEncabezado(
    "Panel principal",
    "Resumen general de la tienda y sus operaciones.",
  );

  if (!contenidoApp) return;

  contenidoApp.innerHTML = `
    <section class="dashboard-grid">

      <div class="summary-card">
        <div class="summary-icon orange">
          🛍️
        </div>

        <div>
          <p>Ventas del día</p>
          <h3 id="ventasDia">S/ 0.00</h3>
          <span id="ventasDiaDetalle" class="positive">Calculando...</span>
        </div>
      </div>

      <div class="summary-card">
        <div class="summary-icon green">
          📦
        </div>

        <div>
          <p>Productos registrados</p>
          <h3 id="totalProductos">0</h3>
          <span id="productosDetalle" class="positive">Calculando...</span>
        </div>
      </div>

      <div class="summary-card">
        <div class="summary-icon blue">
          🧾
        </div>

        <div>
          <p>Ventas del mes</p>
          <h3 id="ventasMes">S/ 0.00</h3>
          <span id="ventasMesDetalle" class="positive">Calculando...</span>
        </div>
      </div>

      <div class="summary-card">
        <div class="summary-icon purple">
          👥
        </div>

        <div>
          <p>Ventas registradas</p>
          <h3 id="totalVentasRegistradas">0</h3>
          <span id="ventasRegistradasDetalle" class="positive">Calculando...</span>
        </div>
      </div>

    </section>

    <section class="home-layout">

      <div class="panel-card">
        <div class="panel-header">
          <h2>Productos más vendidos</h2>
          <a href="#/productos">Ver todos</a>
        </div>

        <div id="inicioMasVendidos">
          <div class="product-row">
            <span>⏳</span>

            <div>
              <strong>Cargando productos...</strong>
              <p>Consultando ventas y productos</p>
            </div>

            <b>...</b>
          </div>
        </div>
      </div>

      <div class="panel-card">
        <div class="panel-header">
          <h2>Acciones rápidas</h2>
          <span class="mini-text">Según tu rol</span>
        </div>

        <div class="quick-actions" id="accionesRapidasInicio">
          ${obtenerAccionesRapidasPorRol()}
        </div>
      </div>

    </section>

    <section class="alert-card">
      <h3>Calculando productos con bajo stock...</h3>

      <p>
        Revisando información del inventario desde la base de datos.
      </p>

      <a href="#/productos">Revisar productos</a>
    </section>
  `;

  cargarDatosInicio();
}

function obtenerAccionesRapidasPorRol() {
  if (rolUsuario === "administrador") {
    return `
      <a href="#/productos" class="quick-action">📦 Gestionar productos</a>
      <a href="#/ventas" class="quick-action">🧾 Registrar venta</a>
      <a href="#/proveedores" class="quick-action">🚚 Ver proveedores</a>
      <a href="#/tiendas" class="quick-action">🏪 Gestionar tiendas</a>
      <a href="#/usuarios" class="quick-action">👥 Gestionar usuarios</a>
      <a href="#/reportes" class="quick-action">📊 Ver reportes</a>
    `;
  }

  if (rolUsuario === "trabajador") {
    return `
      <a href="#/productos" class="quick-action">📦 Ver productos</a>
      <a href="#/ventas" class="quick-action">🧾 Registrar venta</a>
      <a href="#/proveedores" class="quick-action">🚚 Consultar proveedores</a>
      <a href="#/tiendas" class="quick-action">🏪 Ver tiendas</a>
    `;
  }

  return `
    <a href="#/productos" class="quick-action">📦 Ver catálogo</a>
    <a href="#/carrito" class="quick-action">🛒 Ver carrito</a>
    <a href="#/perfil" class="quick-action">👤 Mi perfil</a>
  `;
}

// ===============================
// DATOS REALES DEL INICIO
// ===============================

async function cargarDatosInicio() {
  const productos = await obtenerProductosInicio();
  const ventas = await obtenerVentasInicio();

  actualizarResumenInicio(productos, ventas);
  renderizarProductosMasVendidosInicio(productos, ventas);
}

async function obtenerProductosInicio() {
  try {
    const response = await fetch("/api/v1/productos");
    const data = await response.json();

    if (!data.ok) {
      return [];
    }

    return data.productos || [];
  } catch (error) {
    console.error("Error cargando productos para inicio:", error);
    return [];
  }
}

async function obtenerVentasInicio() {
  try {
    const response = await fetch("/api/v1/ventas");
    const data = await response.json();

    if (!data.ok) {
      return [];
    }

    return data.ventas || [];
  } catch (error) {
    console.error("Error cargando ventas para inicio:", error);
    return [];
  }
}

function actualizarResumenInicio(productos, ventas) {
  const ventasDiaElemento = document.getElementById("ventasDia");
  const ventasMesElemento = document.getElementById("ventasMes");
  const totalProductosElemento = document.getElementById("totalProductos");
  const totalVentasElemento = document.getElementById("totalVentasRegistradas");

  const ventasDiaDetalle = document.getElementById("ventasDiaDetalle");
  const productosDetalle = document.getElementById("productosDetalle");
  const ventasMesDetalle = document.getElementById("ventasMesDetalle");
  const ventasRegistradasDetalle = document.getElementById(
    "ventasRegistradasDetalle",
  );

  const hoy = new Date();

  const ventasDelDia = ventas.filter((venta) => {
    return esMismaFecha(parsearFechaVenta(venta.fecha), hoy);
  });

  const ventasDelMes = ventas.filter((venta) => {
    return esMismoMes(parsearFechaVenta(venta.fecha), hoy);
  });

  const totalDia = ventasDelDia.reduce((total, venta) => {
    return total + Number(venta.total || 0);
  }, 0);

  const totalMes = ventasDelMes.reduce((total, venta) => {
    return total + Number(venta.total || 0);
  }, 0);

  const productosActivos = productos.filter((producto) => {
    return producto.estado === true && Number(producto.stock || 0) > 0;
  });

  const productosBajoStock = productos.filter((producto) => {
    return Number(producto.stock || 0) <= Number(producto.stockMinimo || 0);
  });

  if (ventasDiaElemento) {
    ventasDiaElemento.textContent = `S/ ${totalDia.toFixed(2)}`;
  }

  if (ventasMesElemento) {
    ventasMesElemento.textContent = `S/ ${totalMes.toFixed(2)}`;
  }

  if (totalProductosElemento) {
    totalProductosElemento.textContent = productos.length;
  }

  if (totalVentasElemento) {
    totalVentasElemento.textContent = ventas.length;
  }

  if (ventasDiaDetalle) {
    ventasDiaDetalle.textContent = `${ventasDelDia.length} ventas registradas hoy`;
  }

  if (productosDetalle) {
    productosDetalle.textContent = `${productosActivos.length} activos · ${productosBajoStock.length} bajo stock`;
  }

  if (ventasMesDetalle) {
    ventasMesDetalle.textContent = `${ventasDelMes.length} ventas este mes`;
  }

  if (ventasRegistradasDetalle) {
    ventasRegistradasDetalle.textContent = "Historial total de ventas";
  }

  actualizarAlertaBajoStockInicio(productosBajoStock);
}

function actualizarAlertaBajoStockInicio(productosBajoStock) {
  const alertaTitulo = document.querySelector(".alert-card h3");
  const alertaTexto = document.querySelector(".alert-card p");

  if (alertaTitulo) {
    alertaTitulo.textContent = `${productosBajoStock.length} productos con bajo stock`;
  }

  if (alertaTexto) {
    if (productosBajoStock.length === 0) {
      alertaTexto.textContent =
        "No hay productos con bajo stock por el momento.";
    } else {
      alertaTexto.textContent =
        "Revisa los productos con inventario bajo para evitar problemas al momento de vender o atender pedidos.";
    }
  }
}

function renderizarProductosMasVendidosInicio(productos, ventas) {
  const contenedor = document.getElementById("inicioMasVendidos");

  if (!contenedor) return;

  if (!productos || productos.length === 0) {
    contenedor.innerHTML = `
      <div class="product-row">
        <span>📦</span>

        <div>
          <strong>Sin productos</strong>
          <p>No hay productos registrados todavía.</p>
        </div>

        <b>0</b>
      </div>
    `;
    return;
  }

  const productosConVentas = calcularVentasPorProducto(productos, ventas);

  const productosOrdenados = productosConVentas
    .sort((a, b) => {
      return Number(b.unidadesVendidas || 0) - Number(a.unidadesVendidas || 0);
    })
    .slice(0, 5);

  let html = "";

  productosOrdenados.forEach((producto) => {
    html += `
      <div class="product-row">
        <span>${obtenerIconoProductoInicio(producto.categoria)}</span>

        <div>
          <strong>${producto.nombre || "Producto sin nombre"}</strong>

          <p>
            ${producto.categoria || "Sin categoría"} ·
            ${producto.marca || "Sin marca"} ·
            S/ ${Number(producto.precioVenta || 0).toFixed(2)}
          </p>
        </div>

        <b>${producto.unidadesVendidas || 0}</b>
      </div>
    `;
  });

  contenedor.innerHTML = html;
}

function calcularVentasPorProducto(productos, ventas) {
  const mapaVentas = {};

  ventas.forEach((venta) => {
    const productosVenta = venta.productos || [];

    productosVenta.forEach((item) => {
      const productoId = item.productoId || item.id;

      if (!productoId) return;

      if (!mapaVentas[productoId]) {
        mapaVentas[productoId] = 0;
      }

      mapaVentas[productoId] += Number(item.cantidad || 0);
    });
  });

  return productos.map((producto) => {
    return {
      ...producto,
      unidadesVendidas: mapaVentas[producto.id] || 0,
    };
  });
}

function parsearFechaVenta(fecha) {
  if (!fecha) return null;

  const texto = String(fecha).trim();

  if (/^\d{4}-\d{2}-\d{2}/.test(texto)) {
    return new Date(texto);
  }

  if (/^\d{2}\/\d{2}\/\d{4}/.test(texto)) {
    const fechaSolo = texto.split(" ")[0];
    const partes = fechaSolo.split("/");

    const dia = Number(partes[0]);
    const mes = Number(partes[1]) - 1;
    const anio = Number(partes[2]);

    return new Date(anio, mes, dia);
  }

  const fechaConvertida = new Date(texto);

  if (isNaN(fechaConvertida.getTime())) {
    return null;
  }

  return fechaConvertida;
}

function esMismaFecha(fechaA, fechaB) {
  if (!fechaA || !fechaB) return false;

  return (
    fechaA.getFullYear() === fechaB.getFullYear() &&
    fechaA.getMonth() === fechaB.getMonth() &&
    fechaA.getDate() === fechaB.getDate()
  );
}

function esMismoMes(fechaA, fechaB) {
  if (!fechaA || !fechaB) return false;

  return (
    fechaA.getFullYear() === fechaB.getFullYear() &&
    fechaA.getMonth() === fechaB.getMonth()
  );
}

function obtenerIconoProductoInicio(categoria) {
  const texto = (categoria || "").toLowerCase();

  if (texto.includes("abarrote")) return "🍚";
  if (texto.includes("lácteo") || texto.includes("lacteo")) return "🥛";
  if (texto.includes("bebida")) return "🥤";
  if (texto.includes("limpieza")) return "🧼";
  if (texto.includes("aceite")) return "🛢️";

  return "📦";
}

// ===============================
// BUSCADOR GLOBAL
// ===============================

let productosBusquedaGlobal = [];

function crearPanelesGlobalesSiNoExisten() {
  const topActions = document.querySelector(".top-actions");

  if (!topActions) return;

  if (!document.getElementById("panelBusquedaGlobal")) {
    const panelBusqueda = document.createElement("div");
    panelBusqueda.className = "search-panel";
    panelBusqueda.id = "panelBusquedaGlobal";

    panelBusqueda.innerHTML = `
      <div class="search-box">
        <input
          type="text"
          id="inputBusquedaGlobal"
          placeholder="Buscar productos..."
        />

        <button id="btnEjecutarBusqueda">
          🔍
        </button>
      </div>

      <div id="resultadosBusquedaGlobal" class="search-results">
        <div class="search-empty">
          Escribe el nombre, marca o categoría de un producto.
        </div>
      </div>
    `;

    topActions.insertAdjacentElement("afterend", panelBusqueda);
  }

  if (!document.getElementById("panelNotificaciones")) {
    const panelNotificaciones = document.createElement("div");
    panelNotificaciones.className = "search-panel";
    panelNotificaciones.id = "panelNotificaciones";

    panelNotificaciones.innerHTML = `
      <div class="search-box">
        <strong>Notificaciones</strong>
      </div>

      <div id="listaNotificaciones" class="search-results">
        <div class="search-empty">
          Cargando notificaciones...
        </div>
      </div>
    `;

    topActions.insertAdjacentElement("afterend", panelNotificaciones);
  }
}

function iniciarBuscadorGlobal() {
  const btnBusqueda = document.getElementById("btnBusqueda");
  const panelBusqueda = document.getElementById("panelBusquedaGlobal");
  const inputBusqueda = document.getElementById("inputBusquedaGlobal");
  const btnEjecutarBusqueda = document.getElementById("btnEjecutarBusqueda");
  const resultadosBusqueda = document.getElementById(
    "resultadosBusquedaGlobal",
  );

  if (!btnBusqueda || !panelBusqueda || !inputBusqueda || !resultadosBusqueda) {
    return;
  }

  btnBusqueda.addEventListener("click", async () => {
    panelBusqueda.classList.toggle("open");

    cerrarPanelNotificaciones();

    if (panelBusqueda.classList.contains("open")) {
      inputBusqueda.focus();

      if (productosBusquedaGlobal.length === 0) {
        await cargarProductosBusquedaGlobal();
      }
    }
  });

  inputBusqueda.addEventListener("input", () => {
    renderizarResultadosBusqueda(inputBusqueda.value);
  });

  btnEjecutarBusqueda.addEventListener("click", () => {
    renderizarResultadosBusqueda(inputBusqueda.value);
  });
}

async function cargarProductosBusquedaGlobal() {
  const resultadosBusqueda = document.getElementById(
    "resultadosBusquedaGlobal",
  );

  if (!resultadosBusqueda) return;

  resultadosBusqueda.innerHTML = `
    <div class="search-empty">
      Cargando productos...
    </div>
  `;

  try {
    const response = await fetch("/api/v1/productos");
    const data = await response.json();

    if (!data.ok) {
      resultadosBusqueda.innerHTML = `
        <div class="search-empty">
          No se pudieron cargar los productos.
        </div>
      `;
      return;
    }

    productosBusquedaGlobal = data.productos || [];

    resultadosBusqueda.innerHTML = `
      <div class="search-empty">
        Escribe el nombre, marca o categoría de un producto.
      </div>
    `;
  } catch (error) {
    resultadosBusqueda.innerHTML = `
      <div class="search-empty">
        Error de conexión con productos.
      </div>
    `;
  }
}

function renderizarResultadosBusqueda(texto) {
  const resultadosBusqueda = document.getElementById(
    "resultadosBusquedaGlobal",
  );

  if (!resultadosBusqueda) return;

  const busqueda = texto.toLowerCase().trim();

  if (!busqueda) {
    resultadosBusqueda.innerHTML = `
      <div class="search-empty">
        Escribe el nombre, marca o categoría de un producto.
      </div>
    `;
    return;
  }

  const resultados = productosBusquedaGlobal
    .filter((producto) => {
      return (
        (producto.nombre || "").toLowerCase().includes(busqueda) ||
        (producto.marca || "").toLowerCase().includes(busqueda) ||
        (producto.categoria || "").toLowerCase().includes(busqueda)
      );
    })
    .slice(0, 8);

  if (resultados.length === 0) {
    resultadosBusqueda.innerHTML = `
      <div class="search-empty">
        No se encontraron productos con "${texto}".
      </div>
    `;
    return;
  }

  let html = "";

  resultados.forEach((producto) => {
    const estadoReal = Number(producto.stock) <= 0 ? false : producto.estado;

    html += `
      <div class="search-item producto-buscado" data-id="${producto.id}">
        <strong>${producto.nombre || "Producto sin nombre"}</strong>

        <span>
          ${producto.categoria || "Sin categoría"} ·
          ${producto.marca || "Sin marca"} ·
          S/ ${Number(producto.precioVenta || 0).toFixed(2)} ·
          Stock: ${producto.stock}
          ${estadoReal ? "" : " · Inactivo"}
        </span>
      </div>
    `;
  });

  resultadosBusqueda.innerHTML = html;

  document.querySelectorAll(".producto-buscado").forEach((item) => {
    item.addEventListener("click", () => {
      const productoId = item.getAttribute("data-id");
      const producto = productosBusquedaGlobal.find((p) => p.id === productoId);

      if (!producto) return;

      localStorage.setItem("busquedaProductosPendiente", producto.nombre || "");

      window.location.hash = "#/productos";

      cerrarPanelBusqueda();
    });
  });
}

function cerrarPanelBusqueda() {
  const panelBusqueda = document.getElementById("panelBusquedaGlobal");

  if (panelBusqueda) {
    panelBusqueda.classList.remove("open");
  }
}

// ===============================
// NOTIFICACIONES
// ===============================

function iniciarNotificacionesGlobales() {
  const btnNotificaciones = document.getElementById("btnNotificaciones");
  const panelNotificaciones = document.getElementById("panelNotificaciones");

  if (!btnNotificaciones || !panelNotificaciones) {
    return;
  }

  btnNotificaciones.addEventListener("click", async () => {
    panelNotificaciones.classList.toggle("open");

    cerrarPanelBusqueda();

    if (panelNotificaciones.classList.contains("open")) {
      await cargarNotificacionesStock();
    }
  });

  actualizarBadgeNotificaciones();
}

async function cargarNotificacionesStock() {
  const listaNotificaciones = document.getElementById("listaNotificaciones");

  if (!listaNotificaciones) return;

  listaNotificaciones.innerHTML = `
    <div class="search-empty">
      Cargando notificaciones...
    </div>
  `;

  try {
    const response = await fetch("/api/v1/productos");
    const data = await response.json();

    if (!data.ok) {
      listaNotificaciones.innerHTML = `
        <div class="search-empty">
          No se pudieron cargar las notificaciones.
        </div>
      `;
      return;
    }

    const productos = data.productos || [];

    const sinStock = productos.filter((producto) => {
      return Number(producto.stock) <= 0;
    });

    const bajoStock = productos.filter((producto) => {
      return (
        Number(producto.stock) > 0 &&
        Number(producto.stock) <= Number(producto.stockMinimo)
      );
    });

    let html = "";

    sinStock.forEach((producto) => {
      html += `
        <div class="notification-item notification-danger">
          <strong>⛔ ${producto.nombre}</strong>
          <p>Producto sin stock. Debe estar inactivo.</p>
        </div>
      `;
    });

    bajoStock.forEach((producto) => {
      html += `
        <div class="notification-item notification-warning">
          <strong>⚠ ${producto.nombre}</strong>
          <p>
            Stock bajo: ${producto.stock}.
            Stock mínimo: ${producto.stockMinimo}.
          </p>
        </div>
      `;
    });

    if (!html) {
      html = `
        <div class="search-empty">
          No hay notificaciones pendientes.
        </div>
      `;
    }

    listaNotificaciones.innerHTML = html;
  } catch (error) {
    listaNotificaciones.innerHTML = `
      <div class="search-empty">
        Error de conexión con productos.
      </div>
    `;
  }
}

async function actualizarBadgeNotificaciones() {
  const btnNotificaciones = document.getElementById("btnNotificaciones");

  if (!btnNotificaciones) return;

  try {
    const response = await fetch("/api/v1/productos");
    const data = await response.json();

    if (!data.ok) return;

    const productos = data.productos || [];

    const cantidad = productos.filter((producto) => {
      return Number(producto.stock) <= Number(producto.stockMinimo);
    }).length;

    let badge = btnNotificaciones.querySelector(".badge-count");

    if (!badge) {
      badge = document.createElement("span");
      badge.className = "badge-count";
      btnNotificaciones.appendChild(badge);
    }

    if (cantidad > 0) {
      badge.textContent = cantidad;
      badge.style.display = "flex";
    } else {
      badge.style.display = "none";
    }
  } catch (error) {
    console.error("No se pudo actualizar notificaciones", error);
  }
}

function cerrarPanelNotificaciones() {
  const panelNotificaciones = document.getElementById("panelNotificaciones");

  if (panelNotificaciones) {
    panelNotificaciones.classList.remove("open");
  }
}

// ===============================
// CARRITO
// ===============================

function iniciarBotonCarrito() {
  const btnCarrito = document.getElementById("btnCarrito");

  if (!btnCarrito) return;

  btnCarrito.addEventListener("click", () => {
    window.location.hash = "#/carrito";
  });

  actualizarBadgeCarrito();
}

function actualizarBadgeCarrito() {
  const btnCarrito = document.getElementById("btnCarrito");

  if (!btnCarrito) return;

  const carrito = JSON.parse(localStorage.getItem("carrito")) || [];

  const cantidad = carrito.reduce((total, item) => {
    return total + Number(item.cantidad || 0);
  }, 0);

  let badge = btnCarrito.querySelector(".badge-count");

  if (!badge) {
    badge = document.createElement("span");
    badge.className = "badge-count";
    btnCarrito.appendChild(badge);
  }

  if (cantidad > 0) {
    badge.textContent = cantidad;
    badge.style.display = "flex";
  } else {
    badge.style.display = "none";
  }
}

// ===============================
// PERMISOS VISUALES DEL MENÚ
// ===============================

function aplicarPermisosVisuales() {
  const enlaces = document.querySelectorAll(".sidebar-menu a");

  enlaces.forEach((enlace) => {
    const ruta = enlace.getAttribute("href");
    const vista = datosVistas[ruta];

    if (!vista) return;

    if (!tienePermiso(vista.roles)) {
      enlace.style.display = "none";
    }
  });
}

// ===============================
// MENÚ RESPONSIVE
// ===============================

function iniciarMenuResponsive() {
  if (!btnMenu || !sidebar) return;

  btnMenu.addEventListener("click", () => {
    sidebar.classList.toggle("open");
  });

  document.querySelectorAll(".sidebar-menu a").forEach((enlace) => {
    enlace.addEventListener("click", () => {
      sidebar.classList.remove("open");
    });
  });
}

// ===============================
// EVENTOS GLOBALES
// ===============================

window.addEventListener("hashchange", navegar);

document.addEventListener("DOMContentLoaded", () => {
  crearPanelesGlobalesSiNoExisten();

  iniciarFechaHoraSistema();
  cargarTiendasTopbar();

  aplicarPermisosVisuales();
  iniciarMenuResponsive();
  iniciarBuscadorGlobal();
  iniciarNotificacionesGlobales();
  iniciarBotonCarrito();

  navegar();
});

// ===============================
// TIENDA ACTIVA Y FECHA/HORA REAL
// ===============================

let tiendasTopbar = [];

function iniciarFechaHoraSistema() {
  const fechaHoraSistema = document.getElementById("fechaHoraSistema");

  if (!fechaHoraSistema) return;

  function actualizarFechaHora() {
    const ahora = new Date();

    const fecha = ahora.toLocaleDateString("es-PE", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });

    const hora = ahora.toLocaleTimeString("es-PE", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });

    fechaHoraSistema.textContent = `${fecha} · ${hora}`;
  }

  actualizarFechaHora();

  setInterval(actualizarFechaHora, 1000);
}

async function cargarTiendasTopbar() {
  const selector = document.getElementById("selectorTiendaActiva");
  const detalle = document.getElementById("ubicacionTiendaDetalle");

  if (!selector || !detalle) return;

  selector.innerHTML = `
    <option value="">
      Cargando tiendas...
    </option>
  `;

  try {
    const response = await fetch("/api/v1/tiendas");
    const data = await response.json();

    if (!response.ok || !data.ok) {
      selector.innerHTML = `
        <option value="">
          No se pudieron cargar tiendas
        </option>
      `;

      detalle.textContent = "Error al consultar tiendas.";
      return;
    }

    tiendasTopbar = data.tiendas || [];

    if (tiendasTopbar.length === 0) {
      selector.innerHTML = `
        <option value="">
          No hay tiendas registradas
        </option>
      `;

      detalle.textContent = "Registra una tienda en el módulo Tiendas.";
      return;
    }

    renderizarSelectorTiendasTopbar();
  } catch (error) {
    selector.innerHTML = `
      <option value="">
        Error de conexión
      </option>
    `;

    detalle.textContent = "No se pudo conectar con tiendas.";
  }
}

function renderizarSelectorTiendasTopbar() {
  const selector = document.getElementById("selectorTiendaActiva");

  if (!selector) return;

  const tiendaGuardadaId = localStorage.getItem("tiendaActivaId");

  const tiendasActivas = tiendasTopbar.filter((tienda) => {
    return (tienda.estado || "Activa") === "Activa";
  });

  const tiendasParaMostrar =
    tiendasActivas.length > 0 ? tiendasActivas : tiendasTopbar;

  selector.innerHTML = "";

  tiendasParaMostrar.forEach((tienda) => {
    selector.innerHTML += `
      <option value="${tienda.id}">
        ${tienda.nombre || "Tienda sin nombre"}
      </option>
    `;
  });

  const existeGuardada = tiendasParaMostrar.some((tienda) => {
    return tienda.id === tiendaGuardadaId;
  });

  if (tiendaGuardadaId && existeGuardada) {
    selector.value = tiendaGuardadaId;
  } else {
    selector.value = tiendasParaMostrar[0].id;
    localStorage.setItem("tiendaActivaId", tiendasParaMostrar[0].id);
  }

  actualizarTiendaActivaTopbar(selector.value);

  selector.addEventListener("change", () => {
    localStorage.setItem("tiendaActivaId", selector.value);
    actualizarTiendaActivaTopbar(selector.value);
  });
}

function actualizarTiendaActivaTopbar(tiendaId) {
  const detalle = document.getElementById("ubicacionTiendaDetalle");

  if (!detalle) return;

  const tienda = tiendasTopbar.find((item) => item.id === tiendaId);

  if (!tienda) {
    detalle.textContent = "Seleccione una tienda.";
    return;
  }

  const direccion = tienda.direccion || "Sin dirección";
  const categoria = tienda.categoria || "Sin categoría";
  const estado = tienda.estado || "Activa";

  detalle.textContent = `${direccion} · ${categoria} · ${estado}`;
}
