# Memoria TFG - Textos actualizados desde la app móvil

Este documento reúne textos preparados para incorporar a la memoria del TFG a partir de la revisión del proyecto móvil ubicado en `/home/adri/dev/github/manager-finance-repos/mobile-app`. La documentación se mantiene en este repositorio de docs, mientras que el código móvil revisado está en el repositorio indicado.

La revisión se ha realizado sobre el prototipo móvil actual desarrollado con Expo/React Native. La parte de backend queda pendiente de una revisión específica para completar los apartados de API, persistencia real, OCR productivo y despliegue.

---

## 1. Estado actual frente al índice del proyecto

| Apartado del índice | Estado actual | Observaciones |
| --- | --- | --- |
| 1. Definición del proyecto | Cumplido parcialmente | La definición general de Lumen sigue siendo válida, pero debe matizarse que la app móvil actual funciona con datos de demostración y servicios simulados para productos y facturas. |
| 2. Planificación del proyecto | Cumplido parcialmente | La planificación describe tecnologías previstas como Go, PostgreSQL, OCR e IA. En la app móvil sí se verifica Expo, React Native, Firebase Auth, NativeWind y Expo Router. El resto debe contrastarse con backend. |
| 3. Empresa | No evaluado en la app móvil | Este apartado depende de documentación empresarial, no del código de la aplicación. |
| 4. Diseño aplicación móvil | Cumplido parcialmente | El prototipo móvil implementa navegación principal, login, home, productos, escaneo simulado, detalle de factura, estadísticas y configuración. Algunos casos de uso documentados siguen siendo previstos: registro, recuperación de contraseña, exportación, presupuestos, sincronización real, administración y suscripciones. |
| 4.2. Bases de datos | Pendiente de backend | En el frontend revisado no hay base de datos local ni modelo relacional. Hay datos estáticos y stores en memoria para simular productos y facturas. |
| 4.3. Diseño de interfaz | Cumplido parcialmente | Existe una identidad visual consistente basada en estilo brutalista, tipografía monoespaciada, sombras duras, paleta propia y componentes reutilizables. |
| 5. Desarrollo aplicación | Cumplido parcialmente | El área de cliente móvil está implementada a nivel de interfaz y flujos simulados. No se ha identificado área de administración en la app móvil. |
| 6. Pruebas | Pendiente | El proyecto dispone de script de lint, pero no se han localizado pruebas unitarias, de integración ni documentación formal de pruebas de usabilidad/accesibilidad. |
| 7. Manual de instalación | Cumplido parcialmente | Puede documentarse la instalación móvil con `npm install` y ejecución con Expo. Backend pendiente. |
| 8. Guía de usuario | Cumplido parcialmente | Puede redactarse para las pantallas actuales: login, home, productos, scan, facturas, stats y configuración. |
| 9. Documentación API | Pendiente de backend | Solo existe una nota conceptual sobre rutas protegidas con Firebase Auth. Falta documentar endpoints reales. |
| 10. Conclusiones | Debe ajustarse | Las conclusiones actuales afirman integración completa de backend, base de datos, OCR e IA. Conviene reformularlas como objetivos parciales o pendientes hasta revisar backend. |
| 11. Bibliografía | Debe ampliarse | Faltan referencias técnicas de Expo, React Native, Firebase, Expo Router, NativeWind y React Navigation. |
| 12. Anexos | Pendiente | Se pueden incluir capturas de Figma/app, estructura de carpetas, diagramas y scripts de ejecución. |

---

## 4. Diseño de la aplicación móvil

### 4.1. Especificación funcional del sistema

Lumen es una aplicación móvil de gestión financiera personal orientada a reducir el esfuerzo de registrar compras y consultar gastos cotidianos. La versión revisada se centra en la experiencia de usuario móvil y en la construcción de los principales flujos de navegación: acceso a la aplicación, consulta de resumen financiero, listado de productos, simulación de escaneo de facturas, revisión de facturas y configuración de preferencias.

El sistema está desarrollado con Expo y React Native, utilizando Expo Router para organizar la navegación mediante rutas basadas en archivos. La aplicación dispone de una navegación inferior con cuatro secciones principales: Home, Productos, Scan y Configuración. Además, incluye pantallas auxiliares para login, estadísticas, detalle de producto y detalle de factura.

En el estado actual, la app móvil implementa una parte importante de la interfaz y de la lógica de interacción, aunque varios procesos funcionan con datos de demostración o servicios simulados. El código de login está integrado con Firebase Auth mediante `signInWithEmailAndPassword`; para una memoria final conviene añadir credenciales o evidencias de prueba si se quiere presentar como autenticación validada. Los productos se cargan desde datos estáticos y las facturas se gestionan mediante un servicio mock en memoria que simula estados de subida, revisión y validación.

### 4.1.1. Actores del sistema

**Usuario de la aplicación**

Es el actor principal del sistema. Accede a la app mediante email y contraseña, consulta información financiera, revisa productos de demostración, utiliza el flujo simulado de facturas, añade productos manualmente a una factura y modifica opciones de configuración local.

Funciones disponibles para este actor en la versión móvil revisada:

- Iniciar sesión con Firebase Auth.
- Consultar una pantalla inicial con tarjetas resumen.
- Acceder a una pantalla de estadísticas con ingresos, beneficio y variación.
- Consultar productos registrados en datos de demostración.
- Filtrar productos por categoría, marca, precio mínimo, precio máximo y búsqueda textual.
- Abrir el detalle de un producto.
- Simular la captura y subida de una factura.
- Revisar el detalle de una factura simulada.
- Validar o denegar una factura pendiente.
- Añadir manualmente un producto a una factura existente.
- Modificar datos locales de perfil dentro de la pantalla de configuración.
- Cambiar preferencias visuales, idioma y moneda dentro del estado local de la app. El cambio de idioma afecta a los textos internacionalizados disponibles; la moneda y el tema quedan planteados como controles locales pendientes de integración completa.

**Servicio de autenticación externo**

Firebase Auth actúa como servicio externo encargado de validar las credenciales del usuario. En la versión actual, la pantalla de login utiliza `signInWithEmailAndPassword` para autenticar al usuario y, si el acceso es correcto, redirigirlo a la zona principal de la aplicación.

**Servicio simulado de facturas**

El servicio `src/services/receipts.ts` simula el comportamiento esperado del procesamiento de facturas. Permite listar facturas, obtener una factura por identificador, simular la subida de una factura, añadir productos manuales y cambiar el estado de una factura a validada o denegada. Este servicio permite probar el flujo de interfaz antes de integrarlo con un backend real.

### 4.1.2. Casos de uso implementados o parcialmente implementados

| Caso de uso | Estado | Descripción |
| --- | --- | --- |
| Iniciar sesión | Implementado | La pantalla de login autentica con Firebase Auth mediante email y contraseña. |
| Consultar dashboard | Implementado con datos demo | La pantalla Home muestra tarjetas de resumen, últimas actualizaciones y una tarjeta de análisis. |
| Ver estadísticas | Implementado con datos demo | La pantalla Stats muestra métricas de ingresos, beneficio neto y variación. |
| Listar productos | Implementado con datos demo | La pantalla Productos lista productos definidos en datos estáticos. |
| Buscar productos | Implementado | Permite buscar por nombre, marca, precio, categoría o fecha formateada. |
| Filtrar productos | Implementado | Permite filtrar por categoría, marca y rango de precio. |
| Ver detalle de producto | Implementado | La ruta `productos/[id]` muestra marca, nombre, precio, categoría, fecha e identificador. |
| Simular flujo de captura de factura | Implementado como mock | La pantalla Scan muestra una previsualización dibujada y simula la subida sin abrir la cámara real. |
| Simular procesamiento OCR | Implementado como mock | El servicio mock devuelve aleatoriamente éxito, factura incompleta o error. |
| Revisar factura | Implementado con datos mock | La pantalla de detalle muestra campos detectados, productos vinculados y estado de revisión. |
| Validar o denegar factura | Implementado en memoria | La factura puede pasar a estado validada o denegada dentro del store simulado. |
| Añadir producto manual a factura | Implementado en memoria | El usuario puede introducir nombre, importe, mercado y categoría para vincular un producto. |
| Configurar perfil | Implementado localmente | Permite modificar nombre, email y contraseña dentro del estado local de la pantalla. |
| Cambiar preferencias | Implementado localmente | Permite seleccionar idioma, moneda y alternar tema oscuro/claro en estado local. |
| Gestionar permisos | Implementado visualmente | La pantalla de configuración muestra interruptores de cámara, almacenamiento y ubicación, sin integrarse con permisos reales del sistema. |

### 4.1.3. Funcionalidades previstas no verificadas en la app móvil

Las siguientes funcionalidades aparecen en la documentación previa o forman parte del alcance esperado, pero no se han verificado como funcionalidad real en el frontend móvil revisado:

- Registro de nuevos usuarios.
- Recuperación de contraseña.
- Cierre de sesión desde la interfaz.
- Sincronización real con backend.
- Persistencia local offline con SQLite u otra base de datos local.
- Procesamiento OCR real con cámara o subida de imagen real.
- Integración real con IA para extracción de productos.
- Exportación de datos a CSV o PDF.
- Gestión de presupuestos.
- Área de administración.
- Suscripciones o pagos con Stripe.
- Gestión real de notificaciones push.
- Gestión real de permisos nativos de cámara, almacenamiento o ubicación.

---

## 4.2. Diseño de datos

En la aplicación móvil revisada no se ha identificado una base de datos local ni un esquema relacional implementado. El estado actual utiliza dos estrategias de datos:

- Datos estáticos para productos, definidos en `src/assets/data/productData.ts`.
- Stores en memoria para facturas y notificaciones, definidos en `src/services/receipts.ts` a partir de `src/assets/data/receiptData.ts`.

Este enfoque permite validar el diseño de pantallas y flujos sin depender todavía de una API real. Para la memoria, la parte de base de datos debe completarse revisando el backend, ya que ahí deberían definirse las entidades persistentes, las relaciones, el modelo E/R y el esquema lógico normalizado.

### Entidades funcionales detectadas desde el frontend

Aunque no exista persistencia real en la app móvil, el código permite identificar las siguientes entidades de dominio:

**Producto o gasto registrado**

Representa un producto comprado tratado como gasto individual dentro de la app. Contiene identificador, nombre, marca, precio, fecha y categoría. Las categorías utilizadas actualmente son obligación, ahorro y ocio.

**Factura**

Representa un ticket o factura procesada. Contiene identificador, nombre visible, estado, fecha de creación, campos detectados, productos asociados y posibles errores.

**Campo detectado de factura**

Representa un dato extraído durante el procesamiento de una factura, como mercado o total. Incluye valor, confianza, obligatoriedad y estado de completitud.

**Línea de producto de factura**

Representa un producto vinculado a una factura. Puede proceder del mock de OCR o de entrada manual. Incluye nombre, categoría, importe, mercado, fecha y origen.

**Notificación de factura**

Representa un aviso generado cuando una factura queda lista para revisar. En el estado actual se gestiona como dato simulado.

---

## 4.3. Diseño de la interfaz

La interfaz de Lumen aplica una identidad visual reconocible en las pantallas revisadas. El diseño se basa en una estética de alto contraste, con influencia brutalista, donde los elementos se presentan como bloques sólidos, bordes negros marcados y sombras duras. Esta decisión visual conecta con el concepto de marca definido en la documentación previa: aportar claridad sobre el comportamiento financiero del usuario.

### Principios visuales aplicados

- Uso de tarjetas con borde negro grueso y sombra desplazada.
- Tipografía monoespaciada Red Hat Mono para reforzar una apariencia técnica y directa.
- Paleta de colores definida en `src/constants/colors.js` y reutilizada desde Tailwind/NativeWind.
- Navegación inferior personalizada para las secciones principales.
- Pantallas compactas y orientadas a móvil, con scroll vertical y jerarquía visual basada en tarjetas.
- Componentes reutilizables para cabecera, botones, inputs, tarjetas estadísticas e ítems de lista.

### Paleta de color principal

| Grupo | Uso | Colores principales |
| --- | --- | --- |
| Primary | Acciones principales y elementos destacados | Turquesa `#4ECDC4` y variantes claras |
| Secondary | Elementos secundarios y contrastes | Naranja `#F76132` y variantes |
| Accent | Apoyos visuales | Amarillo `#FFE66D`, rojo `#FF6B6B` y verde claro `#F7FFF7` |
| Feedback | Estados de éxito, error, aviso e información | Verde `#22C55E`, rojo `#EF4444`, amarillo `#F59E0B` y azul `#0EA5E9` |
| Category | Categorías de producto | Obligación `#4F46E5`, ahorro `#10B981` y ocio `#A855F7` |
| Base | Fondo y contraste | Blanco `#FFFFFF` y negro `#000000` |

### Mapa de pantallas actual

| Pantalla | Ruta | Función |
| --- | --- | --- |
| Entrada inicial | `app/index.tsx` | Redirección inicial hacia login o zona correspondiente. |
| Login | `app/login.tsx` | Autenticación con Firebase Auth mediante email y contraseña. |
| Home | `app/(tabs)/index.tsx` | Resumen financiero con tarjetas de estado y acceso a estadísticas. |
| Productos | `app/(tabs)/productos/index.tsx` | Listado, búsqueda y filtrado de productos. |
| Detalle de producto | `app/(tabs)/productos/[id].tsx` | Información individual de un producto. |
| Scan | `app/(tabs)/scan.tsx` | Simulación de captura/subida de factura y entrada manual de productos. |
| Detalle de factura | `app/receipts/[id].tsx` | Revisión de campos detectados, productos y validación de factura. |
| Stats | `app/stats.tsx` | Resumen de ingresos, beneficio y variación. |
| Configuración | `app/(tabs)/config/index.tsx` | Acceso a perfil, preferencias, notificaciones, categorías, datos e información. |
| Perfil | `app/(tabs)/config/perfil.tsx` | Edición local de datos de usuario. |
| Preferencias | `app/(tabs)/config/preferencias.tsx` | Selección de idioma, moneda y tema. |
| Categorías | `app/(tabs)/config/categorias.tsx` | Pantalla placeholder con título. |
| Datos | `app/(tabs)/config/datos.tsx` | Pantalla placeholder con título. |
| Notificaciones | `app/(tabs)/config/notificaciones.tsx` | Pantalla placeholder con título. |
| Información | `app/(tabs)/config/informacion.tsx` | Pantalla auxiliar de configuración. |

---

## 5. Desarrollo de la aplicación móvil

La aplicación móvil se ha desarrollado con Expo y React Native, utilizando TypeScript como lenguaje principal. La estructura del proyecto separa las rutas de la aplicación (`app/`), los componentes reutilizables (`src/components/`), los servicios (`src/services/`), los datos estáticos (`src/assets/data/`), los recursos visuales (`src/assets/images/`) y las constantes de diseño (`src/constants/`).

### 5.1. Elementos gráficos y multimedia

El proyecto incluye recursos visuales en `src/assets/images`, como logotipo, iconos de categoría, icono de aplicación, splash screen y elementos decorativos. La interfaz utiliza SVG para algunos elementos gráficos y recursos webp/png para iconos e imagen de fondo.

Los principales elementos gráficos implementados son:

- Logotipo de Lumen en formato SVG.
- Iconos de categorías para obligación, ahorro y ocio.
- Imagen de fondo en la pantalla de login.
- Iconos de Material Icons para navegación, acciones y estados.
- Tarjetas visuales con sombras sólidas y bordes gruesos.

### 5.2. Área de cliente

El área de cliente corresponde a toda la aplicación móvil accesible tras el login. Está organizada en cuatro pestañas principales:

**Home**

Muestra una vista inicial con tarjetas resumen, último recibo, total gastado, dinero restante, últimas actualizaciones y una tarjeta de análisis. Actualmente los valores son estáticos y sirven como maqueta funcional de la composición visual de la pantalla.

**Productos**

Permite consultar productos de demostración. La pantalla incluye filtros por categoría, búsqueda textual y filtros avanzados por marca y rango de precio. El usuario puede abrir el detalle de cada producto para ver información individual.

**Scan**

Permite simular el flujo de captura de facturas. La pantalla ofrece dos modos: foto y entrada manual. En el modo foto se muestra una previsualización dibujada antes de simular la subida de la factura. En el modo manual se puede vincular un producto a una factura existente introduciendo nombre, importe, mercado y categoría.

**Configuración**

Agrupa las opciones de perfil, preferencias, notificaciones, categorías, datos e información. Perfil y preferencias tienen interacción local. El resto de subpantallas existen como estructura inicial, pero todavía no contienen funcionalidad completa.

### 5.3. Área de administración

No se ha identificado un área de administración implementada en la aplicación móvil revisada. Si el proyecto requiere una zona administrativa, deberá documentarse desde el backend o desde un panel externo si existe. En caso contrario, conviene indicar en la memoria que el alcance actual del frontend corresponde únicamente al área de usuario final.

---

## 6. Pruebas

El proyecto móvil dispone de configuración de lint mediante el script `npm run lint`, basado en Expo. No se han localizado scripts de pruebas unitarias o de integración en `package.json`, ni documentación formal de pruebas de usabilidad o accesibilidad.

Para la memoria se puede documentar el estado actual de pruebas de la siguiente manera, diferenciando las comprobaciones ya soportadas por el proyecto de las pruebas que todavía deben ejecutarse formalmente:

### 6.1. Pruebas de usabilidad

La propuesta de pruebas de usabilidad debe centrarse en comprobar si el usuario entiende los flujos principales de la aplicación:

- Iniciar sesión.
- Interpretar el resumen de Home.
- Buscar y filtrar productos.
- Acceder al detalle de un producto.
- Simular la subida de una factura.
- Añadir manualmente un producto a una factura.
- Validar o denegar una factura.
- Cambiar idioma o moneda desde preferencias.

Para cerrar este apartado en la memoria final, será necesario realizar sesiones con usuarios y recoger resultados observables.

### 6.2. Pruebas de accesibilidad

El código incluye algunas propiedades de accesibilidad como `accessibilityRole`, `accessibilityLabel` y `accessibilityState` en botones, enlaces, pestañas, switches y acciones principales. Estas propiedades ayudan a describir el propósito de los elementos interactivos y son una base inicial para una revisión de accesibilidad.

Para cerrar este apartado en la memoria final, falta ejecutar una revisión completa con lector de pantalla, contraste visual, tamaños táctiles y navegación por teclado cuando aplique.

### 6.3. Pruebas técnicas

En la app móvil existen los siguientes comandos de verificación y ejecución:

- Lint del proyecto: `npm run lint`.
- Arranque de la app: `npm run start`.
- Ejecución en Android: `npm run android`.
- Ejecución en iOS: `npm run ios`.
- Ejecución web: `npm run web`.

La memoria final debería incluir el resultado de estos comandos y, si se amplía la cobertura técnica, pruebas unitarias para funciones de filtrado, servicios mock, componentes reutilizables y flujos principales.

---

## 7. Manual de instalación y configuración de la app móvil

### Requisitos previos

Para ejecutar la aplicación móvil es necesario disponer de:

- Node.js instalado.
- npm como gestor de paquetes.
- Expo CLI o uso de los scripts de Expo incluidos en el proyecto.
- Un emulador Android, simulador iOS o la aplicación Expo Go en un dispositivo físico.

### Instalación

Desde la carpeta del proyecto móvil:

```bash
cd /home/adri/dev/github/manager-finance-repos/mobile-app
npm install
```

### Ejecución en desarrollo

Para iniciar el servidor de desarrollo:

```bash
npm run start
```

Para abrir la aplicación directamente en Android:

```bash
npm run android
```

Para abrir la aplicación directamente en iOS:

```bash
npm run ios
```

Para ejecutar la versión web:

```bash
npm run web
```

### Comprobación de calidad

Para revisar errores de lint:

```bash
npm run lint
```

### Configuración de Firebase

La aplicación inicializa Firebase desde `src/services/firebase.ts`. En la versión revisada, la configuración está incluida directamente en el archivo y se utiliza para obtener el objeto `auth`, que posteriormente se usa en el login.

Esta es la situación actual del prototipo. En una versión productiva, las claves y configuración deberían gestionarse mediante variables de entorno o configuración segura del proyecto.

---

## 8. Guía de usuario

### Inicio de sesión

Al abrir la aplicación, el usuario accede a una pantalla de login. Debe introducir su email y contraseña. Si las credenciales son correctas, la aplicación redirige a la zona principal con pestañas.

### Pantalla Home

La pantalla Home muestra un resumen general del estado financiero. Incluye tarjetas con datos destacados, una sección de últimas actualizaciones y un acceso a estadísticas ampliadas.

### Consulta de productos

En la pestaña Productos, el usuario puede consultar una lista de productos registrados. Puede utilizar filtros por categoría, buscar texto y aplicar filtros avanzados por marca o precio. Al seleccionar un producto se abre una pantalla de detalle con su información principal.

### Escaneo y registro de facturas

En la pestaña Scan, el usuario puede elegir entre modo foto y modo manual. En el modo foto se simula el flujo de captura de una factura mediante una previsualización dibujada antes de subirla. El sistema devuelve un estado de éxito, incompleto o error. Si la factura queda disponible, el usuario puede abrir su detalle.

En el modo manual, el usuario puede seleccionar una factura existente y añadir un producto indicando nombre, importe, mercado y categoría.

### Revisión de facturas

La pantalla de detalle de factura muestra el estado de la factura, una previsualización, los campos detectados y los productos vinculados. Si la factura está pendiente o incompleta, el usuario puede validarla o denegarla.

### Estadísticas

La pantalla Stats presenta un resumen de ingresos, beneficios y variación. En la versión actual, estos datos son demostrativos y sirven para validar la presentación visual.

### Configuración

Desde Configuración, el usuario puede acceder a varias secciones. Perfil permite modificar datos locales de usuario. Preferencias permite cambiar idioma, moneda y alternar el estado visual del tema oscuro/claro. También se muestran accesos a notificaciones, categorías, datos e información, que actualmente están como pantallas base.

---

## 9. Documentación API

La documentación de API debe completarse tras revisar el backend real. En la app móvil revisada no hay llamadas HTTP a una API propia para productos, facturas o estadísticas. La única integración externa funcional identificada es Firebase Auth para el inicio de sesión.

Existe una nota técnica en `mobile-app/docs/api.md` que propone un patrón de API protegido por Firebase Auth:

```http
GET /api/user/me
GET /api/user/me/stats
GET /api/user/me/products
```

El patrón recomendado en esa nota consiste en enviar el token de Firebase en la cabecera `Authorization` y dejar que el backend resuelva el usuario real a partir del token, evitando rutas privadas basadas en identificadores manipulables como `/api/user/:id`. Esta recomendación todavía debe contrastarse con la implementación real del backend.

Texto pendiente para completar tras revisar backend:

- Listado real de endpoints.
- Métodos HTTP.
- Parámetros de entrada.
- Formato de respuestas.
- Códigos de error.
- Autenticación y autorización.
- Relación entre endpoints y pantallas móviles.

---

## 10. Conclusiones ajustadas al estado verificado

El desarrollo actual de Lumen permite considerar cumplido de forma parcial el objetivo de construir una aplicación móvil de gestión financiera personal. Se ha implementado una interfaz funcional con navegación, autenticación mediante Firebase, consulta de productos, simulación de escaneo de facturas, revisión de facturas y configuración básica de usuario.

El proyecto también ha permitido aplicar y contrastar decisiones importantes de diseño en el prototipo móvil, como el uso de Expo Router para estructurar la navegación, NativeWind para aplicar estilos, una paleta de colores centralizada y componentes reutilizables para mantener una interfaz coherente.

No obstante, varios objetivos del alcance inicial siguen dependiendo de la integración con backend y servicios reales. Entre ellos destacan la persistencia de datos, la sincronización, el procesamiento OCR real, la extracción mediante IA, la documentación formal de la API, el modelo de base de datos definitivo, las pruebas automatizadas y las funcionalidades avanzadas como presupuestos, exportación o suscripciones.

Por tanto, el estado actual debe describirse como un prototipo móvil avanzado a nivel de interfaz y flujos de usuario. Para considerarlo un sistema completo todavía falta integrar persistencia real, API propia, procesamiento OCR/IA productivo, pruebas formales y documentación técnica del backend.

---

## 11. Referencias técnicas a añadir a bibliografía

- Expo Documentation: https://docs.expo.dev/
- Expo Router: https://docs.expo.dev/router/introduction/
- React Native: https://reactnative.dev/
- Firebase Authentication: https://firebase.google.com/docs/auth
- NativeWind: https://www.nativewind.dev/
- React Navigation: https://reactnavigation.org/
- TypeScript: https://www.typescriptlang.org/docs/
- Tailwind CSS: https://tailwindcss.com/docs
- Gorhom Bottom Sheet: https://gorhom.dev/react-native-bottom-sheet/

---

## 12. Anexos recomendados

Para completar la memoria, los anexos más útiles serían:

- Capturas de las pantallas principales de la app.
- Capturas del prototipo de Figma.
- Estructura de carpetas del proyecto móvil.
- Tabla de rutas de Expo Router.
- Diagrama de navegación entre pantallas.
- Diagrama de entidades detectadas desde frontend.
- Resultado de `npm run lint` cuando se ejecute la verificación final.
- Documentación del backend cuando se revise.
