# 8. Guía de usuario

Esta guía explica el uso de las pantallas principales de la aplicación móvil Lumen en su estado actual. La aplicación se organiza en cuatro pestañas principales en la navegación inferior: **Home**, **Productos**, **Scan** y **Configuración**, más una pantalla de **Estadísticas** accesible desde Home.

> **Nota sobre persistencia:** En el estado actual la aplicación trabaja con datos de demostración y stores en memoria. Los cambios realizados en categorías, preferencias o productos no persisten entre sesiones.

---

## 8.1. Inicio de sesión

Al abrir la aplicación, el usuario accede a la pantalla de login. Debe introducir **email** y **contraseña**. Si las credenciales son correctas, Firebase Auth valida al usuario y redirige a la zona principal. Si falla, se muestra un mensaje de error indicando que las credenciales no son válidas.

La sesión se mantiene mediante AsyncStorage gracias a la persistencia de Firebase Auth. Al cerrar la aplicación y volver a abrirla, el usuario permanece autenticado.

Pendiente de insertar captura de pantalla de Login.

**Acciones disponibles:**
- Introducir email y contraseña
- Iniciar sesión
- Cerrar sesión (desde Configuración)

> El registro de nuevos usuarios no está implementado. Las credenciales deben crearse previamente en Firebase Console.

---

## 8.2. Pantalla Home

La pantalla Home muestra un resumen general de la actividad financiera.

Pendiente de insertar captura de pantalla de Home.

**Secciones:**
- **Tarjetas resumen:** muestran ingresos, gastos y beneficios totales.
- **Últimas actualizaciones:** lista de movimientos recientes.
- **Tarjeta de análisis:** incluye un botón para acceder a la pantalla de Estadísticas.

**Acciones disponibles:**
- Navegar a Estadísticas pulsando el botón de análisis.
- Acceder a las demás pestañas mediante la navegación inferior.

> Los datos mostrados son de demostración. En una versión con backend, se cargarían desde la API Go.

---

## 8.3. Estadísticas

Accesible desde Home. Presenta métricas financieras con valores demostrativos.

Pendiente de insertar captura de pantalla de Estadísticas.

**Indicadores:**
- **Ingresos:** suma total de ingresos.
- **Beneficios:** diferencia entre ingresos y gastos.
- **Variación:** cambio porcentual respecto al periodo anterior.

> Los datos son ilustrativos. La pantalla sirve para validar la presentación visual de estadísticas.

---

## 8.4. Consulta de productos

En la pestaña **Productos**, el usuario puede consultar una lista de productos registrados como datos de demostración.

Pendiente de insertar captura de pantalla de Productos.

**Funcionalidades:**
- **Búsqueda:** buscar por nombre, marca, precio, categoría o fecha.
- **Filtros:** filtrar por categoría, marca y rango de precio.
- **Listado:** cada producto muestra nombre, marca, precio y categoría.

Al seleccionar un producto, se abre una pantalla de detalle:

Pendiente de insertar captura de pantalla de Detalle de producto.

**Detalle de producto:**
- Nombre, marca, precio, categoría, fecha e identificador.
- Información completa del producto seleccionado.

> Los productos provienen de datos estáticos definidos en `src/assets/data/productData.ts`. No hay conexión con backend real.

---

## 8.5. Escaneo y registro de facturas

En la pestaña **Scan**, el usuario puede elegir entre dos modos: **foto** y **manual**.

Pendiente de insertar captura de pantalla de Scan en modo foto.

### 8.5.1. Modo foto

1. Al acceder por primera vez, la aplicación solicita **permiso de cámara**.
2. Una vez concedido, se abre el visor de la cámara.
3. El usuario encuadra la factura y pulsa el botón de captura.
4. Se muestra una **previsualización** de la imagen tomada.
5. El usuario puede **confirmar el envío** o **repetir la foto**.
6. Al confirmar, la imagen se envía mediante HTTP a `/api/factura`.
7. El resultado se refleja en el servicio local de facturas con uno de estos estados:
   - **Success:** factura procesada correctamente.
   - **Incomplete:** faltan campos por detectar.
   - **Error:** no se pudo procesar.

> En el estado actual, este flujo usa una URL local de prototipo y el resultado visible se apoya en el store local de facturas. La integración final con el backend Go se documenta como pendiente técnico en el capítulo 9.

Pendiente de insertar captura de pantalla de Scan en modo manual.

### 8.5.2. Modo manual

1. Seleccionar una factura existente de la lista.
2. Añadir un producto introduciendo:
   - **Nombre** del producto.
   - **Importe** total.
   - **Comercio** (opcional).
   - **Categoría** (seleccionable).
3. El producto se vincula a la factura seleccionada.

> El envío HTTP actual tiene una IP fija hardcodeada en `src/hooks/useScanCamera.tsx`. Para cambiar de entorno debe editarse directamente ese archivo. La variable `EXPO_PUBLIC_API_BASE_URL` está definida en `api.ts` pero el hook de scan aún no la utiliza.

---

## 8.6. Revisión de facturas

Desde el listado de facturas o tras escanear, el usuario puede abrir el detalle de una factura.

Pendiente de insertar captura de pantalla de Detalle de factura.

**Información mostrada:**
- **Estado** de la factura: pendiente, incompleta, validada, denegada o error.
- **Previsualización** de la imagen.
- **Campos detectados:** comercio, importe, fecha, etc.
- **Productos vinculados:** lista de productos asociados.

**Acciones disponibles:**
- **Validar factura:** marca la factura como correcta.
- **Denegar factura:** marca la factura como rechazada.
- **Añadir producto manual:** vincula un nuevo producto a la factura.

> El historial de estados y productos se mantiene en memoria mediante el servicio `src/services/facturas.ts`. Los cambios se pierden al recargar la aplicación.

---

## 8.7. Configuración

La pestaña **Configuración** agrupa varias secciones de gestión del perfil y preferencias de la aplicación.

Pendiente de insertar captura de pantalla de Configuración.

**Secciones disponibles:**

| Sección | Descripción |
|---------|-------------|
| Perfil | Datos personales del usuario |
| Preferencias | Idioma, moneda y tema visual |
| Notificaciones | Activación de recordatorios y alertas |
| Categorías | Gestión de categorías de gasto |
| Datos | Importación, sincronización y exportación |
| Información | Versión y datos legales de la aplicación |

---

### 8.7.1. Perfil

Pendiente de insertar captura de pantalla de Perfil.

Permite modificar datos locales del usuario:
- **Nombre**
- **Correo electrónico**
- **Avatar** (selector visual)

Los cambios se aplican localmente y se reflejan en la interfaz.

---

### 8.7.2. Preferencias

Pendiente de insertar captura de pantalla de Preferencias.

Configuración general de la aplicación:
- **Idioma:** selector de idioma de la interfaz.
- **Moneda:** selector de moneda para mostrar importes.
- **Tema oscuro:** alternador para cambiar entre tema claro y oscuro.

---

### 8.7.3. Notificaciones

Pendiente de insertar captura de pantalla de Notificaciones.

Interruptores para activar o desactivar distintos tipos de notificaciones:
- **Recordatorios de escaneo:** aviso periódico para escanear facturas.
- **Resumen semanal:** notificación con resumen de la semana.
- **Notificaciones push:** activación global de notificaciones push.

> En el estado actual, los interruptores modifican estado local pero no están conectados a un servicio de notificaciones real.

---

### 8.7.4. Categorías

Pendiente de insertar captura de pantalla de Categorías.

Gestión local de categorías de gasto:

**Acciones disponibles:**
- **Listar:** todas las categorías existentes mostradas en orden.
- **Crear:** nueva categoría indicando nombre y tipo (ingreso/gasto).
- **Editar:** modificar nombre o tipo de una categoría existente.
- **Eliminar:** borrar una categoría no base (las categorías base no se pueden eliminar).

> Las categorías base vienen predefinidas. Las creadas por el usuario se almacenan en memoria local.

---

### 8.7.5. Datos

Pendiente de insertar captura de pantalla de Datos.

Acciones de gestión de datos del usuario:

| Acción | Descripción | Estado actual |
|--------|-------------|---------------|
| **Importar datos** | Importar datos desde un archivo CSV | Pendiente — muestra aviso |
| **Sincronizar datos** | Sincronizar con el backend | Pendiente — muestra aviso |
| **Exportar datos** | Exportar datos a formato CSV | Pendiente — muestra aviso |

> Las acciones de importar, sincronizar y exportar están preparadas en la interfaz pero muestran un aviso indicando que la funcionalidad CSV está pendiente de implementar.

---

### 8.7.6. Información

Pendiente de insertar captura de pantalla de Información.

Muestra información estática de la aplicación:
- **Nombre de la aplicación:** Lumen
- **Versión:** número de versión
- **Descripción breve:** propósito de la aplicación
- **Enlaces legales:** avisos y políticas (si aplica)

---

## 8.8. Cierre de sesión

Desde la pantalla de Configuración, el usuario puede cerrar la sesión. Al hacerlo:

1. Firebase Auth cierra la sesión mediante `signOut`.
2. El usuario es redirigido a la pantalla de login.
3. Para volver a acceder debe introducir sus credenciales de nuevo.

---

## 8.9. Resumen de pantallas

| Pantalla | Ruta | Función principal |
|----------|------|-------------------|
| Login | `app/login.tsx` | Autenticación con Firebase |
| Home | `(tabs)/index.tsx` | Resumen financiero |
| Productos | `(tabs)/productos/index.tsx` | Listado y filtros |
| Detalle producto | `(tabs)/productos/[id].tsx` | Información individual |
| Scan | `(tabs)/scan/index.tsx` | Captura de facturas |
| Detalle factura | `app/facturas/[id].tsx` | Revisión y validación |
| Estadísticas | `app/stats.tsx` | Métricas demostrativas |
| Configuración | `(tabs)/config/index.tsx` | Opciones de usuario |
| Perfil | `(tabs)/config/perfil.tsx` | Edición de datos locales |
| Preferencias | `(tabs)/config/preferencias.tsx` | Idioma, moneda, tema |
| Notificaciones | `(tabs)/config/notificaciones.tsx` | Recordatorios y alertas |
| Categorías | `(tabs)/config/categorias.tsx` | Gestión local de categorías |
| Datos | `(tabs)/config/datos.tsx` | Importar, sincronizar, exportar |
| Información | `(tabs)/config/informacion.tsx` | Versión y datos legales |
