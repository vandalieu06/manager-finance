# 5. Desarrollo aplicación móvil

El desarrollo de la aplicación móvil se ha realizado con Expo y React Native, utilizando TypeScript como lenguaje principal. El proyecto está organizado para separar claramente las pantallas, los componentes reutilizables, los servicios, los datos de demostración, las constantes de diseño y los recursos gráficos.

La estructura principal del frontend móvil es:

- `app/`: rutas y pantallas gestionadas por Expo Router.
- `src/components/`: componentes reutilizables de interfaz, layout y navegación.
- `src/services/`: integración con servicios externos o servicios simulados.
- `src/assets/`: imágenes, iconos y datos de demostración.
- `src/constants/`: valores compartidos como la paleta de colores.
- `src/lib/`: utilidades generales, como internacionalización.
- `src/domain/`: tipos de dominio para productos y facturas.

[estructura de carpetas frontend]

## 5.1. Elementos gráficos y multimedia

La aplicación utiliza elementos visuales propios del sistema de diseño de Lumen. Entre los recursos principales se encuentran:

- Logotipo de Lumen en formato SVG.
- Iconos de categorías para obligación, ahorro y ocio.
- Imagen de fondo para la pantalla de login.
- Iconos de aplicación y splash screen.
- Elementos decorativos exportados de Figma.
- Iconografía de Material Icons para navegación y acciones.

Los recursos se encuentran principalmente en `src/assets/images`. Además, la aplicación utiliza una paleta de colores centralizada en `src/constants/colors.js`, lo que permite reutilizar los mismos valores desde los estilos de NativeWind y desde componentes React Native.

[captura recursos gráficos]

## 5.2. Área clientes

El área de cliente corresponde a la aplicación móvil accesible tras el login. Está organizada en cuatro pestañas principales: Home, Productos, Scan y Configuración.

**Home**

La pantalla Home muestra una vista de resumen con tarjetas estadísticas, últimas actualizaciones y una tarjeta de análisis. Actualmente utiliza datos de demostración, por lo que funciona como maqueta funcional del dashboard.

[captura pantalla home]

**Productos**

La pantalla Productos permite consultar una lista de productos de demostración. Incluye búsqueda textual, filtros por categoría y filtros avanzados por marca y rango de precio. También permite abrir el detalle individual de cada producto.

[captura pantalla productos]

**Detalle de producto**

El detalle de producto muestra información como marca, nombre, precio, categoría, fecha e identificador. Esta pantalla permite comprobar la navegación dinámica mediante rutas con parámetro `id`.

[captura pantalla detalle producto]

**Scan**

La pantalla Scan representa el flujo de captura y revisión de facturas. Tiene dos modos: foto y manual. En el modo foto se simula la captura mediante una previsualización dibujada y un servicio mock que devuelve estados de éxito, incompleto o error. En el modo manual, el usuario puede vincular productos a una factura existente.

[captura pantalla scan]

**Detalle de factura**

La pantalla de detalle de factura muestra el estado de revisión, los campos detectados, los productos asociados y las acciones de validar o denegar. El estado se modifica en memoria mediante el servicio simulado de facturas.

[captura pantalla detalle factura]

**Stats**

La pantalla Stats presenta métricas de ingresos, beneficios y variación. En la versión actual estos datos son demostrativos y sirven para validar la presentación visual de estadísticas.

[captura pantalla stats]

**Configuración**

La pantalla Configuración agrupa accesos a perfil, preferencias, notificaciones, categorías, datos e información. Perfil y preferencias tienen interacción local; otras subpantallas funcionan como estructura inicial.

[captura pantalla configuración]

### Componentes reutilizables

El proyecto incluye componentes reutilizables para mantener consistencia visual:

- `Header`: cabecera común de la aplicación.
- `BottomNavBar`: navegación inferior personalizada.
- `Button`: botón reutilizable.
- `FormInput`: campo de formulario.
- `ItemLista`: elemento de lista.
- `StatCard`: tarjeta de estadística.

[captura componentes UI]

### Servicios

El frontend incluye dos servicios principales:

- `firebase.ts`: inicializa Firebase y exporta `auth` para el login.
- `receipts.ts`: simula operaciones de facturas, productos manuales, validación, denegación y notificaciones.

El servicio de facturas no realiza llamadas reales a una API. Su función es permitir probar el flujo de interfaz antes de integrar backend, OCR e IA reales.

## 5.3. Área administración

No se ha identificado un área de administración implementada en la aplicación móvil revisada. El alcance actual del frontend corresponde al usuario final. Si el proyecto incorpora una zona administrativa, deberá documentarse a partir del backend o de un panel externo cuando exista.

Como mejora futura, un área de administración podría incluir:

- Gestión de usuarios.
- Consulta de métricas globales.
- Revisión de incidencias de facturas.
- Gestión de categorías base.
- Supervisión de servicios OCR/IA.

[pantalla administración futura]
