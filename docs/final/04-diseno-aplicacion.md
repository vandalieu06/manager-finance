# 4. Diseño aplicación móvil

## 4.1. Especificación funcional del sistema

Lumen es una aplicación móvil de gestión financiera personal. La versión revisada se centra en la experiencia de usuario móvil y en la construcción de los principales flujos de navegación: acceso a la aplicación, consulta de resumen financiero, listado de productos, simulación de escaneo de facturas, revisión de facturas y configuración de preferencias.

El sistema está desarrollado con Expo y React Native, utilizando Expo Router para organizar la navegación mediante rutas basadas en archivos. La aplicación dispone de una navegación inferior con cuatro secciones principales: Home, Productos, Scan y Configuración. Además, incluye pantallas auxiliares para login, estadísticas, detalle de producto y detalle de factura.

En el estado actual, la app móvil implementa parte importante de la interfaz y de la lógica de interacción. Algunos procesos funcionan con datos de demostración o servicios simulados. El login está integrado con Firebase Auth mediante `signInWithEmailAndPassword`; los productos se cargan desde datos estáticos y las facturas se gestionan con un servicio mock en memoria.

## 4.1.1. Especificación del sistema propuesto

El sistema propuesto se organiza alrededor de la actividad del usuario y de sus gastos cotidianos. La aplicación debe permitir consultar información financiera, registrar productos, clasificar gastos y revisar facturas.

En el prototipo móvil actual, las funcionalidades verificadas son:

- Inicio de sesión con Firebase Auth.
- Navegación principal por pestañas.
- Dashboard con tarjetas resumen.
- Pantalla de estadísticas con métricas demostrativas.
- Listado y filtrado de productos.
- Detalle de producto.
- Simulación de captura y subida de factura.
- Revisión de factura con campos detectados y productos asociados.
- Validación o denegación de facturas en memoria.
- Entrada manual de productos vinculados a una factura.
- Configuración básica de perfil y preferencias en estado local.

Las funcionalidades previstas pero no verificadas como implementación final son:

- Registro de nuevos usuarios.
- Recuperación de contraseña.
- Cierre de sesión desde interfaz.
- Sincronización real con backend.
- Persistencia local offline.
- Procesamiento OCR real.
- Integración real de IA para extracción de productos.
- Exportación de datos.
- Gestión de presupuestos.
- Área de administración.
- Suscripciones o pagos.

## 4.1.1.1. Descripción de los actores

**Usuario de la aplicación**

Es el actor principal. Accede a la app, consulta información financiera, revisa productos, utiliza el flujo simulado de facturas, añade productos manualmente y modifica preferencias locales.

**Servicio de autenticación externo**

Firebase Auth se encarga de validar las credenciales introducidas en la pantalla de login.

**Servicio simulado de facturas**

El servicio `src/services/receipts.ts` simula el comportamiento esperado del procesamiento de facturas. Permite listar facturas, obtener una factura por identificador, simular una subida, añadir productos manuales y cambiar el estado de una factura.

[diagrama de actores]

## 4.1.1.2. Modelo de casos de uso

Los principales casos de uso del prototipo móvil son:

| Caso de uso | Estado | Descripción |
| --- | --- | --- |
| Iniciar sesión | Implementado | El usuario accede mediante email y contraseña. |
| Consultar dashboard | Implementado con datos demo | Muestra tarjetas resumen y análisis. |
| Ver estadísticas | Implementado con datos demo | Presenta ingresos, beneficios y variación. |
| Listar productos | Implementado con datos demo | Muestra productos definidos en datos estáticos. |
| Buscar productos | Implementado | Permite buscar por nombre, marca, precio, categoría o fecha. |
| Filtrar productos | Implementado | Permite filtrar por categoría, marca y rango de precio. |
| Ver detalle de producto | Implementado | Muestra datos individuales de un producto. |
| Simular flujo de factura | Implementado como mock | Muestra previsualización y simula subida. |
| Revisar factura | Implementado con datos mock | Muestra campos detectados, productos y estado. |
| Validar o denegar factura | Implementado en memoria | Cambia el estado de la factura. |
| Añadir producto manual | Implementado en memoria | Vincula un producto a una factura existente. |
| Configurar perfil | Implementado localmente | Modifica datos dentro del estado de pantalla. |
| Cambiar preferencias | Implementado localmente | Cambia idioma y controles de preferencias. |

[diagrama de casos de uso]

## 4.1.2. Diseño del sistema

El diseño del sistema se apoya en una separación entre rutas, componentes reutilizables, servicios, datos estáticos, constantes y assets. La carpeta `app/` contiene las pantallas gestionadas por Expo Router, mientras que `src/` agrupa componentes, servicios, dominio, assets y constantes.

[diagrama de arquitectura frontend]

## 4.1.2.1. Diagramas de secuencia de los casos de uso más relevantes

**Flujo de inicio de sesión**

1. El usuario introduce email y contraseña.
2. La pantalla de login llama a Firebase Auth.
3. Firebase valida las credenciales.
4. Si la autenticación es correcta, la app redirige a la zona principal.
5. Si falla, se muestra un mensaje de error.

[diagrama de secuencia: inicio de sesión]

**Flujo de revisión de factura simulada**

1. El usuario accede a la pestaña Scan.
2. Selecciona el modo foto.
3. La app muestra una previsualización dibujada.
4. El usuario confirma la subida.
5. El servicio mock devuelve éxito, incompleto o error.
6. Si existe factura, el usuario puede abrir el detalle.
7. En el detalle, puede validar o denegar la factura.

[diagrama de secuencia: escaneo de factura]

**Flujo de filtrado de productos**

1. El usuario accede a Productos.
2. La app carga productos de demostración.
3. El usuario aplica filtros o búsqueda.
4. La lista se recalcula en cliente.
5. El usuario puede abrir el detalle de un producto.

[diagrama de secuencia: filtrado de productos]

## 4.1.2.2. Diagrama de clases de diseño

Desde el frontend revisado se identifican las siguientes entidades funcionales:

- Producto o gasto registrado.
- Factura.
- Campo detectado de factura.
- Línea de producto de factura.
- Notificación de factura.
- Usuario autenticado.

[diagrama de clases]

## 4.1.2.3. Diagramas de estado

El caso más representativo es el estado de una factura dentro del flujo simulado. Una factura puede estar pendiente de revisión, incompleta, validada, denegada o en error.

[diagrama de estados: factura]

## 4.1.3. Interfaces de usuario: mapa de formularios

El mapa de pantallas actual es:

| Pantalla | Ruta | Función |
| --- | --- | --- |
| Entrada inicial | `app/index.tsx` | Redirección inicial. |
| Login | `app/login.tsx` | Autenticación. |
| Home | `app/(tabs)/index.tsx` | Resumen financiero. |
| Productos | `app/(tabs)/productos/index.tsx` | Listado y filtros. |
| Detalle de producto | `app/(tabs)/productos/[id].tsx` | Información individual. |
| Scan | `app/(tabs)/scan.tsx` | Flujo de factura y entrada manual. |
| Detalle de factura | `app/receipts/[id].tsx` | Revisión y validación. |
| Stats | `app/stats.tsx` | Estadísticas. |
| Configuración | `app/(tabs)/config/index.tsx` | Opciones de usuario. |
| Perfil | `app/(tabs)/config/perfil.tsx` | Edición local de perfil. |
| Preferencias | `app/(tabs)/config/preferencias.tsx` | Idioma, moneda y tema. |

[mapa de navegación de la app]

## 4.2. Bases de datos

En la aplicación móvil revisada no se ha identificado una base de datos local ni un esquema relacional implementado. El frontend utiliza datos estáticos y stores en memoria para simular productos, facturas y notificaciones.

La base de datos final debe completarse a partir de la revisión del backend. Desde el frontend se puede deducir qué información necesita almacenar el sistema, pero no se puede afirmar todavía el modelo físico definitivo.

## 4.2.1. Qué información se desea almacenar

El sistema necesita almacenar:

- Usuarios y datos básicos de autenticación/perfil.
- Productos o gastos registrados.
- Categorías de gasto.
- Facturas o tickets procesados.
- Campos detectados en facturas.
- Líneas de producto asociadas a facturas.
- Estados de revisión de facturas.
- Notificaciones relacionadas con facturas.

## 4.2.2. Modelo E/R

[diagrama entidad-relación]

## 4.2.3. Esquema lógico normalizado hasta tercera forma normal

[esquema lógico base de datos]

## 4.3. Diseño de la interfaz

La interfaz de Lumen aplica una estética de alto contraste, con influencia brutalista. Los elementos se presentan como bloques sólidos, con bordes negros marcados y sombras duras. Esta decisión visual conecta con el concepto de marca: aportar claridad sobre el comportamiento financiero del usuario.

## 4.3.1. Prototipado

El prototipado en Figma incluye pantallas de Home Dashboard y Productos. También se han definido tokens de diseño, componentes base y especificaciones para futuras pantallas como Configuración y Escanear Facturas.

[prototipo Figma: home]

[prototipo Figma: productos]

[prototipo Figma: scan]

[prototipo Figma: configuración]

## 4.3.2. Guía de estilo

La guía visual se basa en los siguientes elementos:

- Tipografía principal: Red Hat Mono.
- Tipografía secundaria: Inter para navegación o gráficos cuando sea necesario.
- Bordes negros de 3px o 4px.
- Sombras duras sin desenfoque decorativo.
- Paleta centralizada en tokens de color.
- Categorías principales: obligación, ahorro y ocio.

| Grupo | Uso | Colores principales |
| --- | --- | --- |
| Primary | Acciones principales | `#4ECDC4` |
| Secondary | Contraste y acciones secundarias | `#F76132` |
| Accent | Destacados visuales | `#FFE66D`, `#FF6B6B`, `#F7FFF7` |
| Feedback | Estados | `#22C55E`, `#EF4444`, `#F59E0B`, `#0EA5E9` |
| Category | Clasificación de gastos | `#4F46E5`, `#10B981`, `#A855F7` |
| Base | Fondo y contraste | `#FFFFFF`, `#000000` |

[captura sistema de diseño]
