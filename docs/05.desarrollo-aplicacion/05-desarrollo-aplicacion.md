# 5. Desarrollo aplicación móvil

El desarrollo de la aplicación móvil se ha realizado con **Expo ~55** y **React Native 0.83** (React 19), utilizando **TypeScript** como lenguaje principal. La navegación se organiza mediante **Expo Router** con rutas basadas en archivos y el estilo se apoya en **NativeWind** (TailwindCSS para React Native).

El proyecto está estructurado para separar claramente pantallas, componentes reutilizables, servicios, datos de demostración y constantes de diseño.

---

## 5.1. Estructura del proyecto

```
mobile-app/
├── app/                          # Rutas y pantallas (Expo Router)
│   ├── _layout.tsx               # Layout raíz y providers globales
│   ├── index.tsx                 # Redirección inicial
│   ├── login.tsx                 # Pantalla de autenticación
│   ├── stats.tsx                 # Estadísticas
│   ├── facturas/
│   │   └── [id].tsx              # Detalle de factura
│   └── (tabs)/                   # Navegación inferior (4 tabs)
│       ├── _layout.tsx           # Layout de pestañas
│       ├── index.tsx             # Home / Dashboard
│       ├── explore.tsx           # Ruta auxiliar no incluida en la tab bar final
│       ├── productos/
│       │   ├── _layout.tsx       # Layout de sección productos
│       │   ├── index.tsx         # Listado de productos
│       │   └── [id].tsx          # Detalle de producto
│       ├── scan/
│       │   ├── _layout.tsx       # Layout de sección scan
│       │   ├── index.tsx         # Escaneo de facturas
│       │   └── components/       # Componentes internos de scan
│       │       ├── ScanCaptureButton.tsx
│       │       ├── BrowserTabs.tsx
│       │       └── ManualEntryPanel.tsx
│       └── config/
│           ├── _layout.tsx       # Layout de sección configuración
│           ├── index.tsx         # Menú de configuración
│           ├── perfil.tsx        # Edición de perfil
│           ├── preferencias.tsx  # Idioma, moneda, tema
│           ├── notificaciones.tsx # Recordatorios y alertas
│           ├── categorias.tsx    # Gestión de categorías
│           ├── datos.tsx         # Importar/sincronizar/exportar
│           └── informacion.tsx   # Versión de la app
│
├── src/
│   ├── components/               # Componentes reutilizables
│   │   ├── ui/                   # Botones, inputs, tarjetas
│   │   ├── layout/               # Header
│   │   └── navigation/           # BottomNavBar
│   ├── services/                 # Servicios
│   │   ├── firebase.ts           # Inicialización Firebase Auth
│   │   ├── api.ts                # authenticatedFetch
│   │   ├── facturas.ts           # Store local de facturas
│   │   └── categories.ts         # Store local de categorías
│   ├── hooks/
│   │   ├── useScanCamera.tsx     # Hook de cámara y envío HTTP
│   │   └── useFacturaManagement.ts # Hook de gestión de facturas
│   ├── assets/
│   │   ├── data/
│   │   │   ├── productData.ts    # Productos de demostración
│   │   │   ├── facturaData.ts    # Facturas y notificaciones demo
│   │   │   └── dataFigma.json    # Datos de apoyo de diseño
│   │   └── images/               # Logos, iconos, splash
│   ├── domain/
│   │   ├── types.ts              # Tipos TypeScript
│   │   └── factura/              # Tipos específicos de factura
│   │       └── factura.types.ts
│   ├── constants/
│   │   └── colors.js             # Paleta de colores
│   ├── lib/
│   │   ├── i18n.ts               # Internacionalización
│   │   └── auth.tsx              # useAuth, AuthProvider y contexto
│
├── app.json                      # Configuración Expo
├── package.json
├── tsconfig.json
├── tailwind.config.js            # Configuración NativeWind
└── babel.config.js
```

La estructura de carpetas queda representada en el árbol anterior. Si se requiere una versión visual para la memoria, puede exportarse como imagen a partir de este esquema.

---

## 5.2. Navegación y autenticación

### 5.2.1. Control de acceso

La aplicación usa el hook `useAuth` (definido en `src/lib/auth.tsx` junto con `AuthProvider` y el contexto) que envuelve a Firebase Auth. Proporciona:

- `user`: el usuario autenticado o `null`.
- `idToken`: el token JWT de Firebase (se actualiza automáticamente con `onIdTokenChanged`).
- `isInitializing`: `true` mientras se restaura la sesión al iniciar la app.
- `signIn(email, password)`: inicia sesión con email y contraseña.
- `logout`: cierra la sesión.
- `getIdToken(forceRefresh?)`: obtiene o refresca el token JWT actual.

Los providers globales se montan en `app/_layout.tsx`: `I18nProvider`, `AuthProvider`, `BottomSheetModalProvider`, `GestureHandlerRootView` y carga de la fuente Red Hat Mono. La protección de las rutas principales se aplica en `app/(tabs)/_layout.tsx`: mientras se restaura la sesión se renderiza una vista vacía y, si no hay usuario autenticado, se redirige a `/login`.

### 5.2.2. Navegación inferior

La zona principal usa `(tabs)/_layout.tsx` con cuatro pestañas:

| Pestaña | Icono | Ruta |
|---------|-------|------|
| Home | house | `(tabs)/index.tsx` |
| Productos | list | `(tabs)/productos/` |
| Scan | camera | `(tabs)/scan/` |
| Config | gear | `(tabs)/config/` |

---

## 5.3. Pantallas del área cliente

### 5.3.1. Login (`app/login.tsx`)

Pantalla de inicio de sesión con Firebase Auth mediante `signInWithEmailAndPassword`. Incluye campos de email y contraseña, validación básica y muestra errores de autenticación. No incluye registro de nuevos usuarios.

Pendiente de insertar captura de pantalla de Login.

### 5.3.2. Home (`(tabs)/index.tsx`)

Dashboard con resumen financiero. Muestra tarjetas estadísticas con datos de demostración, una sección de últimas actualizaciones y un acceso a la pantalla de estadísticas. Los valores se cargan desde datos estáticos.

Pendiente de insertar captura de pantalla de Home.

### 5.3.3. Productos (`(tabs)/productos/index.tsx`)

Listado de productos con datos de demostración (`src/assets/data/productData.ts`). Incluye:

- **Búsqueda textual:** filtra por nombre, marca, precio, categoría o fecha.
- **Filtros:** por categoría, marca y rango de precio.
- Los filtros se aplican en cliente sobre el array de datos estáticos.

Pendiente de insertar captura de pantalla de Productos.

### 5.3.4. Detalle de producto (`(tabs)/productos/[id].tsx`)

Pantalla dinámica que recibe el `id` como parámetro de ruta. Muestra nombre, marca, precio, categoría, fecha e identificador del producto.

Pendiente de insertar captura de pantalla de Detalle de producto.

### 5.3.5. Scan (`(tabs)/scan/index.tsx`)

Flujo de captura de facturas con dos modos:

**Modo foto:**
1. Solicita permiso de cámara mediante `expo-camera`.
2. Abre el visor y permite capturar una imagen.
3. Muestra previsualización y botones de confirmar o repetir.
4. Al confirmar, construye un `FormData` con el campo `factura` y envía la imagen a `http://10.196.17.218:3000/api/factura`.
5. Si el envío HTTP responde correctamente, se ejecuta `handleUploadFactura`, que simula el resultado de procesamiento en el store local de facturas mediante `subirFacturaMock`.
6. El estado mostrado en la interfaz procede del store local; no se persiste todavía en el backend Go.

**Modo manual:**
1. Selecciona una factura existente.
2. Añade un producto con nombre, importe, comercio y categoría.

Pendiente de insertar captura de pantalla de Scan.

### 5.3.6. Detalle de factura (`app/facturas/[id].tsx`)

Muestra el estado de revisión de la factura (pendiente, incompleta, validada, denegada o error), los campos detectados y los productos vinculados. Permite validar, denegar o añadir productos manualmente.

El estado se gestiona en memoria mediante `src/services/facturas.ts`.

Pendiente de insertar captura de pantalla de Detalle de factura.

### 5.3.7. Estadísticas (`app/stats.tsx`)

Presenta métricas demostrativas de ingresos, beneficios y variación. Los datos son fijos y sirven para validar el diseño visual.

Pendiente de insertar captura de pantalla de Estadísticas.

### 5.3.8. Configuración (`(tabs)/config/`)

Agrupa seis subpantallas accesibles desde un menú:

- **Perfil:** edición local de nombre, email y avatar.
- **Preferencias:** selector de idioma, moneda y alternador de tema oscuro.
- **Notificaciones:** interruptores para recordatorios y push (estado local).
- **Categorías:** listado, creación, edición y eliminación de categorías. Las categorías base no se pueden eliminar. Los cambios se almacenan en memoria mediante `src/services/categories.ts`.
- **Datos:** acciones de importar, sincronizar y exportar con aviso de funcionalidad CSV pendiente.
- **Información:** versión y datos legales de la aplicación.

También incluye la acción de **cerrar sesión**, que llama a `signOut` de Firebase Auth y redirige al login.

Pendiente de insertar captura de pantalla de Configuración.

---

## 5.4. Servicios

### 5.4.1. Firebase (`src/services/firebase.ts`)

Inicializa la aplicación de Firebase con la configuración del proyecto. Exporta el objeto `auth` para ser usado en login y en el hook `useAuth`.

### 5.4.2. API (`src/services/api.ts`)

Define `authenticatedFetch`, una utilidad que:

1. Lee `EXPO_PUBLIC_API_BASE_URL` como URL base (sin fallback; lanza error si no está definida).
2. Obtiene el token JWT de Firebase del usuario autenticado.
3. Añade `Authorization: Bearer <token>` a la cabecera usando `Headers`.
4. Realiza la petición HTTP, con soporte para rutas absolutas.

> En el estado actual esta utilidad está definida pero **no se usa** en las pantallas principales. Está preparada para cuando se integre con el backend Go. El flujo de cámara usa todavía un `fetch` directo con una IP local.

### 5.4.3. Facturas (`src/services/facturas.ts`)

Store local en memoria que gestiona:

- Listado de facturas.
- Obtención de factura por ID.
- Simulación de resultado de procesamiento.
- Adición de productos manuales a una factura.
- Cambio de estado (validar/denegar).
- Notificaciones asociadas a facturas.

### 5.4.4. Categorías (`src/services/categories.ts`)

Store local en memoria que gestiona:

- Listado de categorías (incluye categorías base predefinidas).
- Creación de nuevas categorías.
- Edición de categorías existentes.
- Eliminación de categorías no base.

### 5.4.5. useScanCamera (`src/hooks/useScanCamera.tsx`)

Hook que encapsula el flujo completo de captura:

1. Solicita permiso de cámara (`expo-camera`).
2. Toma la fotografía.
3. Construye `FormData` con el campo `factura` (nombre del archivo: `factura.jpg`).
4. Envía mediante `fetch` a `http://10.196.17.218:3000/api/factura`.
5. Devuelve el estado del envío (`sending`, `message`) y ejecuta un callback de éxito.

Este contrato no coincide todavía con el backend Go documentado en el capítulo 9. El backend espera `POST /api/transactions` con `data`, `image` y `process_ocr`; por tanto, el hook debe considerarse una integración provisional de prototipo.

### 5.4.6. useFacturaManagement (`src/hooks/useFacturaManagement.ts`)

Hook que gestiona el estado de las facturas y la subida de imágenes:

1. Carga las últimas 5 facturas al iniciar mediante `listarFacturas()`.
2. `handleUploadFactura`: simula la subida de una factura (usa `subirFacturaMock`) y actualiza el listado.
3. `handleManualSubmit`: añade un producto manual a una factura con nombre, categoría, importe y comercio.
4. Expone estados de subida (`uploadStatus`), factura seleccionada, visibilidad de previsualización y errores.

---

## 5.5. Componentes reutilizables

| Componente | Ubicación | Función |
|-----------|-----------|---------|
| `Header` | `src/components/layout/` | Cabecera común con título |
| `BottomNavBar` | `src/components/navigation/` | Barra de navegación inferior |
| `Button` | `src/components/ui/` | Botón reutilizable (primario, secundario, ghost) |
| `BrutalButton` | `src/components/ui/` | Botón visual de estilo brutalista usado en acciones destacadas |
| `FormInput` | `src/components/ui/` | Campo de formulario con etiqueta |
| `ItemLista` | `src/components/ui/` | Elemento de lista genérico |
| `StatCard` | `src/components/ui/` | Tarjeta de estadística |
| `StatusCard` | `src/components/ui/` | Estado de subida/procesamiento de factura |
| `FacturaPreviewModal` | `src/components/ui/` | Modal de previsualización de imagen capturada |
| `FacturaPickerSheet` | `src/components/ui/` | Selector inferior de facturas existentes |
| `CategorySelect` | `src/components/ui/` | Selector de categoría de producto |

Pendiente de insertar captura del conjunto de componentes UI.

---

## 5.6. Datos de demostración

Los productos de demostración se definen en `src/assets/data/productData.ts`. Contienen una lista estática de productos con nombre, marca, precio, categoría, fecha e identificador. Estos datos alimentan la pantalla de Productos y los filtros.

Las facturas y notificaciones de ejemplo se definen en `src/assets/data/facturaData.ts`. El resto de datos mutables (facturas creadas durante la sesión y categorías personalizadas) se gestionan en memoria a través de los stores locales `src/services/facturas.ts` y `src/services/categories.ts`, sin persistencia entre sesiones.

---

## 5.7. Internacionalización

El proyecto incluye un sistema básico de internacionalización en `src/lib/i18n.tsx` que permite cambiar el idioma de la interfaz. Actualmente soporta configuración de idioma desde la pantalla de Preferencias y define traducciones para español, inglés, catalán, francés, alemán, italiano y portugués. La cobertura se concentra en navegación, configuración, permisos, perfil, preferencias, notificaciones y acciones de datos; no todo el texto de todas las pantallas está internacionalizado todavía.

---

## 5.8. Paleta de colores

Los colores de la aplicación se centralizan en `src/constants/colors.js` y se utilizan tanto desde NativeWind como desde componentes React Native directos. Los valores principales siguen el sistema de diseño de Lumen:

| Grupo | Color principal | Uso |
|-------|----------------|-----|
| Primary | `#4ECDC4` | Acciones principales |
| Secondary | `#F76132` | Contraste |
| Accent | `#FFE66D`, `#FF6B6B` | Destacados |
| Category | `#4F46E5`, `#10B981`, `#A855F7` | Obligación, ahorro, ocio |

---

## 5.9. Limitaciones del estado actual

- **Sin persistencia:** todos los datos locales (facturas, categorías, preferencias) se pierden al recargar la aplicación.
- **Backend no conectado a pantallas principales:** las pantallas funcionan con datos demo; `authenticatedFetch` está preparada pero no conectada.
- **Contrato de factura provisional:** el envío de facturas apunta a una URL local `/api/factura` con campo `factura`; no pasa por autenticación ni por el endpoint real del backend Go.
- **Tarea pendiente: integración app-backend-OCR:** cerrar el flujo completo para que la app envíe la factura al backend, el backend llame al OCR y la app reciba de vuelta los campos normalizados extraídos de la factura. La tarea se considerará completada cuando la pantalla de revisión muestre productos, importes, comercio y estado de la factura recibidos desde backend, sin depender de datos simulados en memoria.
- **Sin pruebas automatizadas:** no hay tests unitarios ni de integración en la app móvil.
- **Registro no implementado:** el login funciona con Firebase Auth, pero el alta de usuarios se gestiona fuera de la app.
- **Funciones CSV y sincronización no implementadas:** las acciones de importar, sincronizar y exportar muestran avisos, pero no ejecutan integración real.
